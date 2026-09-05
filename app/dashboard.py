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

"""Dashboard HTML and template rendering for 4-Domain Investment Agent."""


def get_dashboard_html() -> str:
    """Returns the complete HTML/JS/CSS for the modern 4-tab investment dashboard."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Autonomous Investment Agent | Stocks, ETFs, Crypto, Commodities</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    :root {
      --bg: #090d16;
      --card-bg: #111827;
      --card-border: #1f293d;
      --card-hover: #172136;
      --primary: #3b82f6;
      --primary-glow: rgba(59, 130, 246, 0.25);
      --accent: #6366f1;
      --success: #10b981;
      --success-glow: rgba(16, 185, 129, 0.2);
      --danger: #ef4444;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --text-dim: #6b7280;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      z-index: 50;
    }

    .header-container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 1rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .brand-icon {
      width: 42px;
      height: 42px;
      background: linear-gradient(135deg, #2563eb, #7c3aed);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.4rem;
      box-shadow: 0 4px 14px var(--primary-glow);
    }

    .brand-title h1 {
      font-size: 1.25rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      background: linear-gradient(90deg, #ffffff, #93c5fd);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-title p {
      font-size: 0.78rem;
      color: var(--text-muted);
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.35rem 0.75rem;
      border-radius: 9999px;
      background: rgba(16, 185, 129, 0.12);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.25);
    }

    .badge-pill.cloud {
      background: rgba(59, 130, 246, 0.12);
      color: #60a5fa;
      border-color: rgba(59, 130, 246, 0.25);
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.55rem 1.1rem;
      font-size: 0.82rem;
      font-weight: 600;
      border-radius: 8px;
      border: none;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: inherit;
    }

    .btn-primary {
      background: linear-gradient(135deg, #2563eb, #3b82f6);
      color: #fff;
      box-shadow: 0 2px 10px var(--primary-glow);
    }

    .btn-primary:hover {
      background: linear-gradient(135deg, #1d4ed8, #2563eb);
      transform: translateY(-1px);
    }

    .btn-secondary {
      background: var(--card-hover);
      color: var(--text-main);
      border: 1px solid var(--card-border);
    }

    .btn-secondary:hover {
      background: #232f48;
    }

    /* Main Container */
    main {
      max-width: 1400px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
      flex: 1;
      width: 100%;
    }

    /* Tabs Bar */
    .tabs-bar {
      display: flex;
      gap: 0.5rem;
      background: #0d1322;
      padding: 0.35rem;
      border-radius: 12px;
      border: 1px solid var(--card-border);
      margin-bottom: 2rem;
      overflow-x: auto;
    }

    .tab-btn {
      flex: 1;
      min-width: 140px;
      padding: 0.85rem 1.25rem;
      background: transparent;
      border: none;
      border-radius: 9px;
      color: var(--text-muted);
      font-size: 0.92rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.6rem;
      transition: all 0.2s ease;
      font-family: inherit;
    }

    .tab-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.03);
    }

    .tab-btn.active {
      background: linear-gradient(135deg, #1e293b, #1e3a8a);
      color: #ffffff;
      border: 1px solid #3b82f6;
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }

    .tab-icon {
      font-size: 1.25rem;
    }

    /* Subagent Info Banner */
    .agent-banner {
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
      border: 1px solid var(--card-border);
      border-left: 4px solid var(--primary);
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .agent-banner-info h3 {
      font-size: 1.05rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 0.3rem;
    }

    .agent-banner-info p {
      font-size: 0.85rem;
      color: var(--text-muted);
      max-width: 850px;
    }

    /* Cards Grid */
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 1.5rem;
      margin-bottom: 3rem;
    }

    @media (max-width: 640px) {
      .cards-grid { grid-template-columns: 1fr; }
    }

    .asset-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 1.5rem;
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    .asset-card:hover {
      border-color: #3b82f6;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      transform: translateY(-2px);
    }

    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }

    .asset-header {
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
    }

    .asset-ticker-row {
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }

    .asset-symbol {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.35rem;
      font-weight: 800;
      letter-spacing: -0.01em;
      color: #fff;
    }

    .asset-category {
      font-size: 0.7rem;
      font-weight: 600;
      padding: 0.2rem 0.55rem;
      border-radius: 6px;
      background: #1f293d;
      color: #94a3b8;
    }

    .asset-name {
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    .price-box {
      text-align: right;
    }

    .current-price {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.4rem;
      font-weight: 700;
    }

    .change-pill {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.78rem;
      font-weight: 600;
      padding: 0.2rem 0.5rem;
      border-radius: 6px;
      display: inline-block;
      margin-top: 0.2rem;
    }

    .change-pill.positive {
      background: rgba(16, 185, 129, 0.15);
      color: #10b981;
    }

    .change-pill.negative {
      background: rgba(239, 68, 68, 0.15);
      color: #ef4444;
    }

    /* Forecast Highlight Box */
    .forecast-box {
      background: linear-gradient(135deg, rgba(37, 99, 235, 0.12), rgba(99, 102, 241, 0.08));
      border: 1px solid rgba(59, 130, 246, 0.25);
      border-radius: 10px;
      padding: 0.75rem 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .forecast-label {
      font-size: 0.75rem;
      color: #93c5fd;
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.05em;
    }

    .forecast-value {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.15rem;
      font-weight: 700;
      color: #60a5fa;
    }

    .forecast-target {
      font-size: 0.78rem;
      color: var(--text-dim);
    }

    /* Chart Container */
    .chart-container {
      position: relative;
      width: 100%;
      height: 140px;
    }

    /* Metrics Grid */
    .metrics-table {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.5rem;
      background: #0d1322;
      border-radius: 8px;
      padding: 0.65rem 0.85rem;
      border: 1px solid rgba(255, 255, 255, 0.04);
    }

    .metric-item {
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
    }

    .metric-label {
      font-size: 0.68rem;
      color: var(--text-dim);
      text-transform: uppercase;
      font-weight: 600;
    }

    .metric-val {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-main);
    }

    /* Thesis Box */
    .thesis-box {
      background: rgba(255, 255, 255, 0.02);
      border-left: 3px solid #6366f1;
      padding: 0.75rem 0.9rem;
      border-radius: 0 8px 8px 0;
      font-size: 0.82rem;
      line-height: 1.45;
      color: #cbd5e1;
    }

    /* News catalysts */
    .news-catalyst {
      font-size: 0.76rem;
      color: var(--text-muted);
      border-top: 1px dashed var(--card-border);
      padding-top: 0.65rem;
    }

    .news-catalyst a {
      color: #93c5fd;
      text-decoration: none;
    }
    .news-catalyst a:hover {
      text-decoration: underline;
    }

    /* Chat Section */
    .chat-section {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 1.5rem;
      margin-top: 1rem;
    }

    .chat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }

    .chat-messages {
      max-height: 260px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
      padding-right: 0.5rem;
      margin-bottom: 1rem;
    }

    .chat-bubble {
      padding: 0.75rem 1rem;
      border-radius: 10px;
      font-size: 0.85rem;
      line-height: 1.45;
      max-width: 80%;
    }

    .chat-bubble.agent {
      background: #1e293b;
      align-self: flex-start;
      border: 1px solid #334155;
    }

    .chat-bubble.user {
      background: #2563eb;
      color: #fff;
      align-self: flex-end;
    }

    .chat-input-row {
      display: flex;
      gap: 0.5rem;
    }

    .chat-input {
      flex: 1;
      background: #0d1322;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 0.75rem 1rem;
      color: #fff;
      font-family: inherit;
      font-size: 0.85rem;
      outline: none;
    }

    .chat-input:focus {
      border-color: #3b82f6;
    }

    /* Loading Spinner */
    .spinner {
      border: 3px solid rgba(255, 255, 255, 0.1);
      border-top: 3px solid #3b82f6;
      border-radius: 50%;
      width: 18px;
      height: 18px;
      animation: spin 0.8s linear infinite;
      display: inline-block;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    footer {
      border-top: 1px solid var(--card-border);
      padding: 1.5rem;
      text-align: center;
      font-size: 0.78rem;
      color: var(--text-dim);
    }
  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="header-container">
      <div class="brand">
        <div class="brand-icon">📈</div>
        <div class="brand-title">
          <h1>Autonomous Financial Investment Agent</h1>
          <p>Multi-Domain AI Intelligence: Stocks, ETFs, Crypto & Commodities</p>
        </div>
      </div>
      <div class="header-actions">
        <span class="badge-pill">● 4 Subagents Autonomous</span>
        <span class="badge-pill cloud">☁️ GCP: geapp-2026</span>
        <button id="refreshBtn" class="btn btn-primary" onclick="refreshAnalysis()">
          <span id="btnIcon">⚡</span>
          <span id="btnText">Refresh Live Analysis</span>
        </button>
      </div>
    </div>
  </header>

  <main>
    <!-- 4 Domain Tabs -->
    <div class="tabs-bar">
      <button class="tab-btn active" onclick="switchTab('stocks')">
        <span class="tab-icon">📈</span>
        <span>Stocks (Equities)</span>
      </button>
      <button class="tab-btn" onclick="switchTab('etfs')">
        <span class="tab-icon">🌐</span>
        <span>ETFs (Funds)</span>
      </button>
      <button class="tab-btn" onclick="switchTab('cryptos')">
        <span class="tab-icon">🪙</span>
        <span>Cryptos (Digital)</span>
      </button>
      <button class="tab-btn" onclick="switchTab('commodities')">
        <span class="tab-icon">🛢️</span>
        <span>Commodities (Macro)</span>
      </button>
    </div>

    <!-- Active Subagent Executive Summary Banner -->
    <div class="agent-banner" id="agentBanner">
      <div class="agent-banner-info">
        <h3 id="bannerTitle">🤖 Stock Research Subagent (Autonomous)</h3>
        <p id="bannerDesc">Autonomous screening of corporate balance sheets, P/E valuations, forward growth targets, and market news catalysts to select the Top 5 equity recommendations.</p>
      </div>
      <div id="bannerStats" class="badge-pill" style="font-size: 0.8rem;">
        Top 5 High-Conviction Picks
      </div>
    </div>

    <!-- Cards Grid -->
    <div class="cards-grid" id="cardsGrid">
      <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem;">
        <div class="spinner" style="width: 32px; height: 32px; margin-bottom: 1rem;"></div>
        <p style="color: var(--text-muted); font-size: 0.95rem;">Gathering live market data across 4 domains...</p>
      </div>
    </div>

    <!-- Direct Agent Chat Section -->
    <div class="chat-section">
      <div class="chat-header">
        <div>
          <h3 style="font-size: 1rem; font-weight: 700;">💬 Consult the Investment Agent</h3>
          <p style="font-size: 0.78rem; color: var(--text-muted);">Ask our autonomous agents about market trends, specific assets, or investment rationales.</p>
        </div>
        <a href="/dev-ui" target="_blank" class="btn btn-secondary" style="font-size: 0.75rem;">Open ADK Playground ↗</a>
      </div>
      <div class="chat-messages" id="chatMessages">
        <div class="chat-bubble agent">
          👋 Hello! I am your lead Investment Coordinator. My 4 specialized autonomous subagents have screened stocks, ETFs, cryptos, and commodities. How can I assist with your portfolio or asset research today?
        </div>
      </div>
      <div class="chat-input-row">
        <input type="text" id="chatInput" class="chat-input" placeholder="e.g. Why is NVDA forecasted higher than MSFT? Or what is the commodity thesis?" onkeydown="if(event.key==='Enter') sendChatMessage()">
        <button class="btn btn-primary" onclick="sendChatMessage()">Send</button>
      </div>
    </div>
  </main>

  <footer>
    Autonomous Investment Agent powered by Google ADK (Agent Development Kit) & Gemini 3.7 Flash • Google Cloud (geapp-2026)
  </footer>

  <script>
    let currentDomain = 'stocks';
    let cachedData = null;
    let chartInstances = {};

    const domainBanners = {
      stocks: {
        title: "🤖 Stock Research Subagent (Autonomous)",
        desc: "Autonomous screening of corporate balance sheets, P/E valuations, forward growth targets, and market news catalysts to select the Top 5 equity recommendations."
      },
      etfs: {
        title: "🌐 ETF & Index Research Subagent (Autonomous)",
        desc: "Autonomous screening of broad market indices and sector funds, evaluating expense ratios, asset allocation, and macro thematic rotation."
      },
      cryptos: {
        title: "🪙 Crypto & Digital Asset Subagent (Autonomous)",
        desc: "Autonomous analysis of leading blockchain networks, tracking 24h trading volume, volatility metrics, on-chain momentum, and digital asset catalysts."
      },
      commodities: {
        title: "🛢️ Commodity & Macro Subagent (Autonomous)",
        desc: "Autonomous analysis of precious metals, energy, and agriculture, evaluating supply/demand dynamics, geopolitical drivers, and inflation hedging."
      }
    };

    async function loadData(forceRefresh = false) {
      try {
        const url = forceRefresh ? '/api/refresh' : '/api/dashboard-data';
        const method = forceRefresh ? 'POST' : 'GET';
        const resp = await fetch(url, { method });
        cachedData = await resp.json();
        renderDomain(currentDomain);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
        document.getElementById('cardsGrid').innerHTML = `
          <div style="grid-column: 1 / -1; text-align: center; color: var(--danger); padding: 3rem;">
            Failed to load live data. Retrying shortly...
          </div>
        `;
      }
    }

    function switchTab(domain) {
      currentDomain = domain;
      document.querySelectorAll('.tab-btn').forEach((btn, idx) => {
        const domains = ['stocks', 'etfs', 'cryptos', 'commodities'];
        btn.classList.toggle('active', domains[idx] === domain);
      });

      // Update banner
      const banner = domainBanners[domain];
      if (banner) {
        document.getElementById('bannerTitle').innerText = banner.title;
        document.getElementById('bannerDesc').innerText = banner.desc;
      }

      renderDomain(domain);
    }

    function formatNumber(num) {
      if (!num) return 'N/A';
      if (num >= 1e12) return '$' + (num / 1e12).toFixed(2) + 'T';
      if (num >= 1e9) return '$' + (num / 1e9).toFixed(2) + 'B';
      if (num >= 1e6) return '$' + (num / 1e6).toFixed(2) + 'M';
      return num.toLocaleString();
    }

    function renderDomain(domain) {
      const grid = document.getElementById('cardsGrid');
      if (!cachedData || !cachedData[domain]) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:3rem;"><div class="spinner"></div></div>';
        return;
      }

      // Destroy old charts to prevent memory leaks
      Object.keys(chartInstances).forEach(id => {
        if (chartInstances[id]) chartInstances[id].destroy();
      });
      chartInstances = {};

      const assets = cachedData[domain];
      if (!assets || assets.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:3rem; color:var(--text-muted)">No assets found for this domain.</div>';
        return;
      }

      let html = '';
      assets.forEach((asset, idx) => {
        const isPos = asset.day_change >= 0;
        const changeClass = isPos ? 'positive' : 'negative';
        const changeSign = isPos ? '+' : '';
        const chartId = `chart_${domain}_${idx}`;

        const newsHtml = (asset.news && asset.news.length > 0)
          ? `<div class="news-catalyst">
              <strong>Recent Catalyst:</strong> <a href="${asset.news[0].link || '#'}" target="_blank">${asset.news[0].title}</a> (${asset.news[0].publisher})
             </div>`
          : '';

        html += `
          <div class="asset-card">
            <div class="card-top">
              <div class="asset-header">
                <div class="asset-ticker-row">
                  <span class="asset-symbol">${asset.symbol}</span>
                  <span class="asset-category">${asset.category || domain.toUpperCase()}</span>
                </div>
                <span class="asset-name">${asset.name}</span>
              </div>
              <div class="price-box">
                <div class="current-price">$${asset.current_price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                <span class="change-pill ${changeClass}">${changeSign}${asset.day_change_pct}%</span>
              </div>
            </div>

            <div class="forecast-box">
              <div>
                <div class="forecast-label">Forecasted Gain</div>
                <div class="forecast-value">+${asset.forecast_gain_pct}%</div>
              </div>
              <div style="text-align: right;">
                <div class="forecast-label">Target Price</div>
                <div class="forecast-value" style="font-size: 1rem; color: #cbd5e1;">$${asset.target_price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
              </div>
            </div>

            <div class="chart-container">
              <canvas id="${chartId}"></canvas>
            </div>

            <div class="metrics-table">
              <div class="metric-item">
                <span class="metric-label">52W Low / High</span>
                <span class="metric-val">$${asset.metrics.fifty_two_week_low || '—'} - $${asset.metrics.fifty_two_week_high || '—'}</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">${asset.metrics.pe_ratio ? 'P/E Ratio' : 'Volume'}</span>
                <span class="metric-val">${asset.metrics.pe_ratio ? asset.metrics.pe_ratio + 'x' : formatNumber(asset.metrics.volume)}</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">1-Mo Trend</span>
                <span class="metric-val" style="color: ${(asset.metrics.one_month_change_pct || 0) >= 0 ? '#10b981' : '#ef4444'}">
                  ${(asset.metrics.one_month_change_pct || 0) >= 0 ? '+' : ''}${asset.metrics.one_month_change_pct || 0}%
                </span>
              </div>
            </div>

            <div class="thesis-box">
              <strong>Subagent Recommendation:</strong> ${asset.thesis}
            </div>

            ${newsHtml}
          </div>
        `;
      });

      grid.innerHTML = html;

      // Render charts
      assets.forEach((asset, idx) => {
        const chartId = `chart_${domain}_${idx}`;
        const canvas = document.getElementById(chartId);
        if (!canvas) return;

        const history = asset.history || [];
        const labels = history.map(h => h.date);
        const prices = history.map(h => h.close);

        const isPositive = prices.length > 1 ? prices[prices.length - 1] >= prices[0] : true;
        const color = isPositive ? '#10b981' : '#ef4444';
        const ctx = canvas.getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 140);
        gradient.addColorStop(0, isPositive ? 'rgba(16, 185, 129, 0.25)' : 'rgba(239, 68, 68, 0.25)');
        gradient.addColorStop(1, 'rgba(16, 185, 129, 0.0)');

        chartInstances[chartId] = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              data: prices,
              borderColor: color,
              borderWidth: 2,
              pointRadius: 0,
              pointHoverRadius: 4,
              fill: true,
              backgroundColor: gradient,
              tension: 0.2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                  label: (ctx) => `$${ctx.parsed.y.toFixed(2)}`
                }
              }
            },
            scales: {
              x: { display: false },
              y: { display: false }
            }
          }
        });
      });
    }

    async function refreshAnalysis() {
      const btn = document.getElementById('refreshBtn');
      const icon = document.getElementById('btnIcon');
      const text = document.getElementById('btnText');

      btn.disabled = true;
      icon.innerHTML = '<span class="spinner"></span>';
      text.innerText = 'Scanning Markets...';

      await loadData(true);

      icon.innerHTML = '⚡';
      text.innerText = 'Refresh Live Analysis';
      btn.disabled = false;
    }

    async function sendChatMessage() {
      const input = document.getElementById('chatInput');
      const msg = input.value.trim();
      if (!msg) return;

      const container = document.getElementById('chatMessages');
      container.innerHTML += `<div class="chat-bubble user">${escapeHtml(msg)}</div>`;
      input.value = '';
      container.scrollTop = container.scrollHeight;

      // Temporary agent bubble
      const agentBubbleId = 'reply_' + Date.now();
      container.innerHTML += `<div id="${agentBubbleId}" class="chat-bubble agent"><span class="spinner" style="width:14px;height:14px;"></span> Consulting investment agent...</div>`;
      container.scrollTop = container.scrollHeight;

      try {
        const resp = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg, domain: currentDomain })
        });
        const data = await resp.json();
        document.getElementById(agentBubbleId).innerText = data.reply || "Agent responded with insights.";
      } catch (err) {
        document.getElementById(agentBubbleId).innerText = "Sorry, unable to get an answer from the agent at this moment.";
      }
      container.scrollTop = container.scrollHeight;
    }

    function escapeHtml(text) {
      const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
      return text.replace(/[&<>"']/g, m => map[m]);
    }

    // Initial load
    window.addEventListener('DOMContentLoaded', () => loadData());
  </script>
</body>
</html>"""
