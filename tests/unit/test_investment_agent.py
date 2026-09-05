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

"""Unit tests for the 4-Domain Investment Agent and Market Data tools."""

from unittest.mock import MagicMock, patch

import pandas as pd
from fastapi.testclient import TestClient

from app.agent import (
    commodity_agent,
    crypto_agent,
    etf_agent,
    root_agent,
    stock_agent,
)
from app.dashboard import get_dashboard_html
from app.fast_api_app import app
from app.tools.market_data import (
    DOMAIN_CANDIDATES,
    get_asset_details,
)


def test_domain_candidates_exist():
    """Verify that all 4 domains have defined candidate universes with at least 5 assets."""
    for domain in ["stocks", "etfs", "cryptos", "commodities"]:
        assert domain in DOMAIN_CANDIDATES
        assert len(DOMAIN_CANDIDATES[domain]) >= 5


def test_agent_hierarchy():
    """Verify multi-agent architecture: coordinator agent manages 4 domain subagents."""
    subagent_names = [s.name for s in root_agent.sub_agents]
    assert stock_agent.name in subagent_names
    assert etf_agent.name in subagent_names
    assert crypto_agent.name in subagent_names
    assert commodity_agent.name in subagent_names
    assert root_agent.name == "investment_agent"


def test_dashboard_html_structure():
    """Verify the generated dashboard HTML includes the 4 tabs and key UI elements."""
    html = get_dashboard_html()
    assert "Stocks (Equities)" in html
    assert "ETFs (Funds)" in html
    assert "Cryptos (Digital)" in html
    assert "Commodities (Macro)" in html
    assert "chart.js" in html.lower()
    assert "geapp-2026" in html


@patch("yfinance.Ticker")
def test_get_asset_details_mocked(mock_ticker):
    """Verify asset data parsing, forecast calculation, and thesis generation."""
    mock_inst = MagicMock()
    mock_ticker.return_value = mock_inst

    # Mock history dataframe
    dates = pd.date_range(start="2026-01-01", periods=35, freq="D")
    df = pd.DataFrame(
        {
            "Close": [100.0 + i for i in range(35)],
            "Volume": [1000000] * 35,
        },
        index=dates,
    )
    mock_inst.history.return_value = df
    mock_inst.info = {
        "shortName": "Test Asset",
        "currentPrice": 134.0,
        "regularMarketPreviousClose": 133.0,
        "targetMeanPrice": 160.0,
        "marketCap": 1000000000,
        "trailingPE": 25.4,
    }
    mock_inst.news = []

    res = get_asset_details("TEST", domain="stocks")
    assert res["symbol"] == "TEST"
    assert res["current_price"] == 134.0
    assert res["target_price"] == 160.0
    assert res["forecast_gain_pct"] > 0
    assert len(res["history"]) == 35
    assert "thesis" in res


def test_fast_api_routes():
    """Verify FastAPI routes for dashboard and data endpoints."""
    client = TestClient(app)

    # 1. Root dashboard route
    resp_root = client.get("/")
    assert resp_root.status_code == 200
    assert "Autonomous Financial Investment Agent" in resp_root.text

    # 2. Dashboard alias
    resp_dash = client.get("/dashboard")
    assert resp_dash.status_code == 200
    assert "Autonomous Financial Investment Agent" in resp_dash.text
