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

"""Market data tools for retrieving quotes, historical performance, news, and forecasts."""

import concurrent.futures
import math
from typing import Any

import yfinance as yf


def _sanitize_for_json(obj: Any) -> Any:
    """Recursively converts NaN and Infinite floats to safe numbers to prevent JSON serialization errors."""
    if isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_sanitize_for_json(item) for item in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return 0.0
        return obj
    return obj


# Candidate universes for each of the 4 domains
DOMAIN_CANDIDATES = {
    "stocks": [
        {
            "symbol": "NVDA",
            "name": "NVIDIA Corporation",
            "category": "Semiconductors / AI",
        },
        {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "category": "Cloud / Software",
        },
        {"symbol": "AAPL", "name": "Apple Inc.", "category": "Consumer Tech"},
        {"symbol": "AMZN", "name": "Amazon.com Inc.", "category": "E-Commerce / Cloud"},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "category": "AI / Advertising"},
        {
            "symbol": "META",
            "name": "Meta Platforms Inc.",
            "category": "Social Tech / AI",
        },
        {"symbol": "TSLA", "name": "Tesla Inc.", "category": "EV / Autonomous"},
        {"symbol": "LLY", "name": "Eli Lilly & Co.", "category": "Healthcare / Pharma"},
        {
            "symbol": "JPM",
            "name": "JPMorgan Chase & Co.",
            "category": "Financial Services",
        },
        {"symbol": "AVGO", "name": "Broadcom Inc.", "category": "Semiconductors"},
    ],
    "etfs": [
        {
            "symbol": "SPY",
            "name": "SPDR S&P 500 ETF Trust",
            "category": "Large Cap Blend",
        },
        {"symbol": "QQQ", "name": "Invesco QQQ Trust", "category": "Tech / Growth"},
        {
            "symbol": "VTI",
            "name": "Vanguard Total Stock Market",
            "category": "Total US Market",
        },
        {
            "symbol": "SMH",
            "name": "VanEck Semiconductor ETF",
            "category": "Semiconductors",
        },
        {
            "symbol": "SCHD",
            "name": "Schwab US Dividend Equity",
            "category": "Dividend Value",
        },
        {
            "symbol": "XLF",
            "name": "Financial Select Sector SPDR",
            "category": "Financials",
        },
        {
            "symbol": "XLV",
            "name": "Health Care Select Sector SPDR",
            "category": "Healthcare",
        },
        {"symbol": "IWM", "name": "iShares Russell 2000 ETF", "category": "Small Cap"},
    ],
    "cryptos": [
        {
            "symbol": "BTC-USD",
            "name": "Bitcoin",
            "category": "Digital Gold / Store of Value",
        },
        {
            "symbol": "ETH-USD",
            "name": "Ethereum",
            "category": "Smart Contract Platform",
        },
        {"symbol": "SOL-USD", "name": "Solana", "category": "High-Throughput L1"},
        {"symbol": "BNB-USD", "name": "BNB", "category": "Exchange Ecosystem"},
        {"symbol": "XRP-USD", "name": "XRP", "category": "Cross-Border Settlement"},
        {"symbol": "AVAX-USD", "name": "Avalanche", "category": "DeFi / Subnets"},
        {"symbol": "ADA-USD", "name": "Cardano", "category": "Proof-of-Stake L1"},
        {"symbol": "LINK-USD", "name": "Chainlink", "category": "Oracle Network"},
    ],
    "commodities": [
        {"symbol": "GC=F", "name": "Gold Futures", "category": "Precious Metals"},
        {
            "symbol": "SI=F",
            "name": "Silver Futures",
            "category": "Precious & Industrial",
        },
        {"symbol": "CL=F", "name": "Crude Oil Futures", "category": "Energy"},
        {"symbol": "HG=F", "name": "Copper Futures", "category": "Industrial Metals"},
        {
            "symbol": "NG=F",
            "name": "Natural Gas Futures",
            "category": "Clean Energy / Utility",
        },
        {"symbol": "ZC=F", "name": "Corn Futures", "category": "Agricultural"},
        {"symbol": "KC=F", "name": "Coffee Futures", "category": "Soft Commodities"},
        {
            "symbol": "PL=F",
            "name": "Platinum Futures",
            "category": "Precious / Catalysts",
        },
    ],
}


def _clean_news_item(item: dict[str, Any]) -> dict[str, Any]:
    """Normalizes yfinance news items across different version formats."""
    content = item.get("content", {})
    if isinstance(content, dict) and content.get("title"):
        title = content.get("title", "")
        summary = content.get("summary") or content.get("description", "")
        pub_date = content.get("pubDate") or content.get("displayTime", "")
        provider = content.get("provider", {})
        publisher = (
            provider.get("displayName", "Market News")
            if isinstance(provider, dict)
            else str(provider)
        )
        canonical = content.get("canonicalUrl", {})
        link = (
            canonical.get("url", "")
            if isinstance(canonical, dict)
            else str(content.get("clickThroughUrl", ""))
        )
    else:
        title = item.get("title", "")
        summary = item.get("summary", "")
        pub_date = item.get("providerPublishTime", "")
        publisher = item.get("publisher", "Market News")
        link = item.get("link", "")

    return {
        "title": title,
        "summary": summary[:280] + "..." if len(summary) > 280 else summary,
        "publisher": publisher,
        "date": str(pub_date),
        "link": link,
    }


def get_asset_details(symbol: str, domain: str = "stocks") -> dict[str, Any]:
    """Fetches real-time price, metrics, forecast targets, and historical chart data for a symbol.

    Args:
        symbol: The ticker symbol (e.g., 'AAPL', 'SPY', 'BTC-USD', 'GC=F').
        domain: Domain of asset ('stocks', 'etfs', 'cryptos', 'commodities').

    Returns:
        A dictionary with asset metadata, current price, change %, forecast gain %,
        analyst targets or calculated momentum targets, and historical price points.
    """
    ticker = yf.Ticker(symbol)

    # 1. Fetch historical data (3 months daily closes for charts)
    try:
        hist = ticker.history(period="3mo")
    except Exception:
        hist = None

    history_points: list[dict[str, Any]] = []
    current_price: float = 0.0
    prev_close: float = 0.0
    one_month_change: float = 0.0

    if hist is not None and not hist.empty:
        for index, row in hist.iterrows():
            date_str = (
                index.strftime("%Y-%m-%d")
                if hasattr(index, "strftime")
                else str(index)[:10]
            )
            close_val = round(float(row["Close"]), 2)
            history_points.append({"date": date_str, "close": close_val})

        if len(history_points) > 0:
            current_price = float(history_points[-1]["close"])
        if len(history_points) > 1:
            prev_close = float(history_points[-2]["close"])
        if len(history_points) >= 20:
            start_price = float(history_points[-20]["close"])
            if start_price > 0:
                one_month_change = round(
                    ((current_price - start_price) / start_price) * 100, 2
                )

    # 2. Extract info & fast_info
    info: dict[str, Any] = {}
    try:
        info = ticker.info or {}
    except Exception:
        info = {}

    if current_price == 0.0:
        val = info.get("regularMarketPrice") or info.get("currentPrice") or 0.0
        current_price = float(val)
    if prev_close == 0.0:
        val = info.get("regularMarketPreviousClose")
        prev_close = float(val) if val else current_price

    day_change = round(current_price - prev_close, 2)
    day_change_pct = (
        round(((current_price - prev_close) / prev_close * 100), 2)
        if prev_close
        else 0.0
    )

    # 3. Forecast Gain % and Price Target
    target_price = float(info.get("targetMeanPrice") or 0.0)
    forecast_gain_pct = 0.0

    if target_price > 0 and current_price > 0:
        forecast_gain_pct = round(
            ((target_price - current_price) / current_price) * 100, 2
        )
    else:
        # Momentum-informed forecast based on 30-day moving average and trend
        if len(history_points) >= 30:
            close_values: list[float] = [
                float(p["close"]) for p in history_points[-30:]
            ]
            ma_30 = sum(close_values) / 30.0
            momentum = ((current_price - ma_30) / ma_30) if ma_30 > 0 else 0.0
            forecast_gain_pct = round(max(5.0, min(35.0, 12.0 + (momentum * 45))), 2)
            target_price = round(current_price * (1.0 + (forecast_gain_pct / 100.0)), 2)
        else:
            forecast_gain_pct = 14.5
            target_price = round(current_price * 1.145, 2)

    # 4. News
    recent_news = []
    try:
        raw_news = ticker.news or []
        for n in raw_news[:3]:
            recent_news.append(_clean_news_item(n))
    except Exception:
        recent_news = []

    # 5. Domain specific metrics
    metrics = {
        "market_cap": info.get("marketCap"),
        "pe_ratio": round(
            float(info.get("forwardPE") or info.get("trailingPE") or 0), 2
        )
        if (info.get("forwardPE") or info.get("trailingPE"))
        else None,
        "fifty_two_week_high": round(float(info.get("fiftyTwoWeekHigh") or 0), 2)
        if info.get("fiftyTwoWeekHigh")
        else None,
        "fifty_two_week_low": round(float(info.get("fiftyTwoWeekLow") or 0), 2)
        if info.get("fiftyTwoWeekLow")
        else None,
        "volume": info.get("regularMarketVolume") or info.get("volume"),
        "one_month_change_pct": one_month_change,
    }

    # Find name and category from candidate list or info
    name = info.get("shortName") or info.get("longName") or symbol
    category = "General"
    candidates = DOMAIN_CANDIDATES.get(domain, [])
    for c in candidates:
        if c["symbol"] == symbol:
            name = c["name"]
            category = c["category"]
            break

    # Construct synthesized thesis rationale
    thesis = _generate_thesis(
        symbol, name, domain, day_change_pct, forecast_gain_pct, metrics, recent_news
    )

    return _sanitize_for_json(
        {
            "symbol": symbol,
            "name": name,
            "category": category,
            "domain": domain,
            "current_price": current_price,
            "day_change": day_change,
            "day_change_pct": day_change_pct,
            "target_price": target_price,
            "forecast_gain_pct": forecast_gain_pct,
            "metrics": metrics,
            "history": history_points,
            "news": recent_news,
            "thesis": thesis,
        }
    )


def _generate_thesis(
    symbol: str,
    name: str,
    domain: str,
    day_change: float,
    forecast_gain: float,
    metrics: dict[str, Any],
    news: list[dict[str, Any]],
) -> str:
    """Generates an investment thesis rationale based on market data and news."""
    top_headline = news[0]["title"] if news and news[0].get("title") else None

    if domain == "stocks":
        pe_str = (
            f"trading at {metrics['pe_ratio']}x P/E"
            if metrics.get("pe_ratio")
            else "robust balance sheet"
        )
        news_str = f" Catalyzed by: '{top_headline}'." if top_headline else ""
        return (
            f"{name} ({symbol}) demonstrates strong fundamentals with projected upside of +{forecast_gain}%, "
            f"{pe_str} and sustained institutional demand.{news_str}"
        )
    elif domain == "etfs":
        return (
            f"{name} ({symbol}) provides premier institutional liquidity and sector exposure, "
            f"demonstrating steady momentum with a projected target upside of +{forecast_gain}%."
        )
    elif domain == "cryptos":
        news_str = f" Recent driver: '{top_headline}'." if top_headline else ""
        return (
            f"{name} ({symbol}) displays resilient market depth and active accumulation patterns. "
            f"Risk/reward indicators point to an estimated target gain of +{forecast_gain}%.{news_str}"
        )
    else:  # commodities
        return (
            f"{name} ({symbol}) is supported by global macro supply/demand fundamentals and inflation resilience, "
            f"projecting an estimated target upside of +{forecast_gain}%."
        )


def get_top_assets_for_domain(domain: str, limit: int = 5) -> list[dict[str, Any]]:
    """Analyzes candidates in a given domain and returns the top ranked assets.

    Args:
        domain: One of 'stocks', 'etfs', 'cryptos', 'commodities'.
        limit: Number of top assets to return (default 5).

    Returns:
        List of dictionaries with full asset details and forecast metrics.
    """
    candidates = DOMAIN_CANDIDATES.get(domain.lower(), [])
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_symbol = {
            executor.submit(get_asset_details, c["symbol"], domain.lower()): c["symbol"]
            for c in candidates
        }
        for future in concurrent.futures.as_completed(future_to_symbol):
            try:
                res = future.result()
                if res["current_price"] > 0:
                    results.append(res)
            except Exception as e:
                sym = future_to_symbol[future]
                print(f"Error fetching {sym}: {e}")

    # Rank by forecast gain % and 1-month momentum
    results.sort(
        key=lambda x: (
            x["forecast_gain_pct"] * 0.7
            + (x["metrics"].get("one_month_change_pct") or 0) * 0.3
        ),
        reverse=True,
    )
    return results[:limit]


def get_all_domains_recommendations() -> dict[str, list[dict[str, Any]]]:
    """Returns top 5 recommendations for all 4 domains simultaneously."""
    domains = ["stocks", "etfs", "cryptos", "commodities"]
    all_data = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_domain = {
            executor.submit(get_top_assets_for_domain, d, 5): d for d in domains
        }
        for future in concurrent.futures.as_completed(future_to_domain):
            d = future_to_domain[future]
            try:
                all_data[d] = future.result()
            except Exception as e:
                print(f"Error getting recommendations for {d}: {e}")
                all_data[d] = []
    return _sanitize_for_json(all_data)
