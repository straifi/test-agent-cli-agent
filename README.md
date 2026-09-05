# Autonomous Multi-Domain Investment Agent 📈

An autonomous AI agent platform powered by **Google ADK (Agent Development Kit)** and **Gemini 3.7 Flash** that conducts continuous financial investment research across 4 dedicated asset domains:
- 📈 **Stocks** (Equities & High-Conviction Growth)
- 🌐 **ETFs** (Index Tracking & Thematic Sector Funds)
- 🪙 **Cryptos** (Digital Assets & L1 Protocols)
- 🛢️ **Commodities** (Energy, Precious Metals & Agriculture)

The agent features 4 dedicated, autonomous subagents coordinated by a lead investment coordinator, coupled with a real-time 4-tab interactive web dashboard featuring live quotes, Chart.js interactive historical charts, forecasted gains %, valuation metrics, and news catalysts.

---

## 🏛️ Architecture

```
                      ┌───────────────────────────────────────┐
                      │   Investment Coordinator (Root Agent) │
                      │        (Gemini 3.7 Flash + ADK)       │
                      └──────────────────┬────────────────────┘
                                         │
        ┌──────────────────┬─────────────┴──────┬──────────────────┐
        ▼                  ▼                    ▼                  ▼
┌───────────────┐  ┌───────────────┐   ┌────────────────┐  ┌────────────────┐
│  Stock Agent  │  │   ETF Agent   │   │  Crypto Agent  │  │Commodity Agent │
│ (Autonomous)  │  │ (Autonomous)  │   │  (Autonomous)  │  │  (Autonomous)  │
└───────┬───────┘  └───────┬───────┘   └────────┬───────┘  └────────┬───────┘
        └──────────────────┼────────────────────┴───────────────────┘
                           ▼
          ┌───────────────────────────────────┐
          │     Yahoo Finance Market Engine   │
          │  (Quotes, 3M History, Forecasts)  │
          └────────────────┬──────────────────┘
                           ▼
          ┌───────────────────────────────────┐
          │  FastAPI + 4-Tab Web Dashboard    │
          │   (Chart.js, Live Metrics, Chat)  │
          └───────────────────────────────────┘
```

### Dedicated Autonomous Subagents
1. **`StockResearchAgent`**: Scans mega-cap and growth equities, evaluates P/E ratios, forward guidance, and market news to select top 5 equity picks.
2. **`ETFResearchAgent`**: Analyzes market index funds and thematic ETFs, evaluating expense ratios, diversification, and sector momentum.
3. **`CryptoResearchAgent`**: Screens leading blockchain assets, analyzing 24h trading volume, volatility metrics, and crypto catalysts.
4. **`CommodityResearchAgent`**: Analyzes precious metals, energy, and agriculture, evaluating supply/demand dynamics and inflation hedging.

---

## 🖥️ 4-Tab Interactive Web Dashboard

The web dashboard is served directly by the FastAPI application:
- **Tabs**: Dedicated tab views for **Stocks**, **ETFs**, **Cryptos**, and **Commodities**.
- **Top 5 Picks**: Card layout with ticker symbol, company name, current price, and 24h % change.
- **Forecast Gain & Target Price**: Projected returns (e.g. `+42.01% Expected Gain`, target `$327.15`).
- **Interactive Charts**: Responsive line charts powered by Chart.js displaying 3-month daily closing trends.
- **Key Metrics**: 52-week high/low range, P/E ratio, trading volume, and 1-month return trend.
- **Subagent Rationale & News**: AI thesis explaining the selection and linked market news catalysts.
- **Interactive Chat**: Query the investment agent or subagents directly from the web interface.

---

## 🚀 Quick Start (Local)

### 1. Install Dependencies
```bash
# Install uv tool and dependencies
uv tool install google-agents-cli
agents-cli install
```

### 2. Run the Web Dashboard
```bash
uv run python -m app.fast_api_app
```
Open your browser at:
- **Interactive 4-Tab Dashboard**: [http://localhost:8000/](http://localhost:8000/) or [http://localhost:8000/dashboard](http://localhost:8000/dashboard)
- **ADK Developer Playground**: [http://localhost:8000/dev-ui](http://localhost:8000/dev-ui)
- **FastAPI OpenAPI Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Run Quality & Unit Tests
```bash
# Code quality checks (ruff, codespell, ty type checker)
agents-cli lint

# Run unit tests
uv run pytest tests/unit
```

---

## 🐙 Push to GitHub Repository

The repository has been initialized with the `main` branch and the remote set to:
`https://github.com/straifi/investment-agent.git`

To push the codebase to your public GitHub repository:

1. Ensure you have created a public repository named `investment-agent` on [GitHub](https://github.com/new).
2. Authenticate and push:
```bash
git push -u origin main
```
*(You will be prompted for your GitHub username `straifi` and your GitHub Personal Access Token or SSH key).*

---

## ☁️ Google Cloud Deployment

The agent is pre-configured to deploy on Google Cloud project **`geapp-2026`** using Google Cloud Agent Engine / Cloud Run.

### 1. Set Google Cloud Project
```bash
gcloud config set project geapp-2026
```

### 2. Deploy the Agent
```bash
agents-cli deploy
```

---

## 🛠️ API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | `GET` | Main 4-tab interactive investment dashboard |
| `/dashboard` | `GET` | Dashboard alias |
| `/api/dashboard-data` | `GET` | Returns top 5 recommendations for all 4 domains (cached for speed) |
| `/api/refresh` | `POST` | Triggers a fresh live scan of all asset domains |
| `/api/chat` | `POST` | Chat with the investment coordinator or domain subagents |
| `/dev-ui` | `GET` | ADK Developer Playground |
| `/a2a/app/*` | `POST` | A2A Protocol endpoints for multi-agent interoperability |
| `/api/reasoning_engine` | `POST` | Vertex AI Reasoning Engine contract endpoint |
