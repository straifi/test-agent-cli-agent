# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib
import os
import time
from collections.abc import AsyncIterator
from typing import Any

from a2a.server.tasks import InMemoryTaskStore
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from google.adk.cli.fast_api import get_fast_api_app
from google.adk.runners import Runner
from google.genai import types as genai_types
from pydantic import BaseModel

from app.app_utils import services
from app.app_utils.a2a import attach_a2a_routes
from app.app_utils.reasoning_engine_adapter import (
    attach_reasoning_engine_routes,
)
from app.dashboard import get_dashboard_html
from app.tools.market_data import get_all_domains_recommendations

load_dotenv()
allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)
otel_to_cloud = os.environ.get(
    "GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY", ""
).lower() in ("true", "1")

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    from app.agent import app as adk_app
    from app.agent import root_agent

    runner = Runner(
        app=adk_app,
        session_service=services.get_session_service(),
        artifact_service=services.get_artifact_service(),
        auto_create_session=True,
    )
    app.state.runner = runner
    app.state.agent_app_name = adk_app.name
    await attach_a2a_routes(
        app,
        agent=root_agent,
        runner=runner,
        task_store=InMemoryTaskStore(),
        rpc_path=f"/a2a/{adk_app.name}",
    )
    yield


app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=services.ARTIFACT_SERVICE_URI,
    allow_origins=allow_origins,
    session_service_uri=services.SESSION_SERVICE_URI,
    otel_to_cloud=otel_to_cloud,
    lifespan=lifespan,
)
app.title = "investment-agent"
app.description = "API for interacting with the Autonomous Investment Agent"

# Proxy routes so Vertex AI Console Playground can talk to this agent
attach_reasoning_engine_routes(app)

# In-memory cache for dashboard performance
_data_cache: dict[str, Any] = {
    "data": None,
    "timestamp": 0.0,
}


class ChatRequest(BaseModel):
    message: str
    domain: str = "stocks"


# Mount dashboard on root / and /dashboard
# Filter out conflicting default root redirects so dashboard loads directly
app.router.routes = [r for r in app.router.routes if getattr(r, "path", None) != "/"]


@app.get("/", response_class=HTMLResponse)
async def serve_root():
    return get_dashboard_html()


@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    return get_dashboard_html()


@app.get("/api/dashboard-data")
async def get_dashboard_data():
    now = time.time()
    # Cache for 10 minutes to guarantee sub-second page switches
    if _data_cache["data"] is None or (now - _data_cache["timestamp"]) > 600:
        _data_cache["data"] = get_all_domains_recommendations()
        _data_cache["timestamp"] = now
    return JSONResponse(content=_data_cache["data"])


@app.post("/api/refresh")
async def refresh_dashboard_data():
    data = get_all_domains_recommendations()
    _data_cache["data"] = data
    _data_cache["timestamp"] = time.time()
    return JSONResponse(content=_data_cache["data"])


@app.post("/api/chat")
async def handle_chat(req: ChatRequest):
    """Processes questions using the investment agent runner or structured domain intelligence."""
    user_prompt = req.message.strip()
    runner: Runner | None = getattr(app.state, "runner", None)

    if runner:
        try:
            session_svc = services.get_session_service()
            session = await session_svc.create_session(
                app_name=app.state.agent_app_name, user_id="web_user"
            )
            content = genai_types.Content(
                role="user",
                parts=[
                    genai_types.Part.from_text(
                        text=f"[Context Domain: {req.domain.upper()}] {user_prompt}"
                    )
                ],
            )
            response_text = ""
            async for event in runner.run_async(
                user_id="web_user",
                session_id=session.id,
                new_message=content,
            ):
                content_obj = getattr(event, "content", None)
                if content_obj:
                    parts = getattr(content_obj, "parts", None)
                    if parts:
                        for part in parts:
                            text_val = getattr(part, "text", None)
                            if text_val:
                                response_text += text_val

            if response_text.strip():
                return {"reply": response_text.strip()}
        except Exception as e:
            # Fall back to domain intelligence note if runner execution encountered an auth/network glitch
            print(f"Chat runner error: {e}")

    # Fallback contextual response based on current data
    domain = req.domain.lower()
    return {
        "reply": (
            f"Based on our autonomous {domain.upper()} research, the top recommended assets are prioritized "
            f"using technical momentum, valuation metrics, and recent market catalysts. "
            f"Check the {domain.capitalize()} tab to review detailed target gains and 3-month price histories."
        )
    }


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
