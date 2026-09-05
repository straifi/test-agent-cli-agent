# ruff: noqa
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

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.tools.market_data import (
    get_all_domains_recommendations,
    get_asset_details,
    get_top_assets_for_domain,
)

MODEL = "gemini-3.7-flash"


def research_asset(symbol: str, domain: str = "stocks") -> dict:
    """Researches an asset by ticker symbol across stocks, ETFs, cryptos, or commodities.

    Args:
        symbol: The ticker symbol (e.g. 'NVDA', 'SPY', 'BTC-USD', 'GC=F').
        domain: One of 'stocks', 'etfs', 'cryptos', 'commodities'.

    Returns:
        A dictionary with current price, 24h change, target price, forecast gain %,
        fundamental metrics, historical price points, and recent news catalysts.
    """
    return get_asset_details(symbol=symbol, domain=domain)


def rank_domain_top_assets(domain: str, limit: int = 5) -> list[dict]:
    """Evaluates candidates in a domain and returns the top ranked assets.

    Args:
        domain: The domain to screen: 'stocks', 'etfs', 'cryptos', or 'commodities'.
        limit: Number of top assets to return (default 5).

    Returns:
        List of the top assets with full performance metrics, historical charts, and investment thesis.
    """
    return get_top_assets_for_domain(domain=domain, limit=limit)


def get_market_overview() -> dict:
    """Retrieves top 5 investment recommendations across all 4 domains simultaneously:
    Stocks, ETFs, Cryptos, and Commodities.
    """
    return get_all_domains_recommendations()


# 1. Autonomous Stock Research Agent
stock_agent = Agent(
    name="stock_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Specialized autonomous agent for researching equities, individual stocks, earnings, valuation ratios (P/E), and selecting top 5 stock picks.",
    instruction="""You are the Stock Research Subagent.
Your mission is to autonomously research equity markets, examine corporate earnings, valuation ratios (P/E, forward P/E), 52-week ranges, analyst price targets, and company news.
Select the top 5 stock investments based on risk/reward, projected forecast gains, and near-term market catalysts.
Provide your reasoning, current market metrics, and specific price targets.""",
    tools=[research_asset, rank_domain_top_assets],
)

# 2. Autonomous ETF Research Agent
etf_agent = Agent(
    name="etf_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Specialized autonomous agent for researching Exchange-Traded Funds (ETFs), index trackers, thematic sector funds, and selecting top 5 ETF picks.",
    instruction="""You are the ETF Research Subagent.
Your mission is to autonomously research Exchange-Traded Funds (ETFs) covering broad market indices (S&P 500, Nasdaq-100, Total Market) and high-conviction thematic/sector funds (semiconductors, financials, healthcare, small caps).
Evaluate expense ratios, liquidity, macroeconomic sector tailwinds, and historical risk-adjusted returns to select the top 5 ETF investments.""",
    tools=[research_asset, rank_domain_top_assets],
)

# 3. Autonomous Crypto Research Agent
crypto_agent = Agent(
    name="crypto_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Specialized autonomous agent for researching digital assets, cryptocurrencies, 24h volume, volatility, and selecting top 5 crypto picks.",
    instruction="""You are the Crypto Research Subagent.
Your mission is to autonomously analyze digital assets and cryptocurrencies including major store-of-value assets, smart contract platforms, and high-growth ecosystem tokens.
Evaluate price trends, 24-hour volume, network momentum, market capitalization, volatility profiles, and news catalysts to select the top 5 crypto investments.""",
    tools=[research_asset, rank_domain_top_assets],
)

# 4. Autonomous Commodities Research Agent
commodity_agent = Agent(
    name="commodity_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Specialized autonomous agent for researching commodities including energy, precious metals, industrial metals, and agriculture, selecting top 5 commodity picks.",
    instruction="""You are the Commodities Research Subagent.
Your mission is to autonomously analyze physical and futures commodity markets including precious metals (Gold, Silver), energy (Crude Oil, Natural Gas), industrial metals (Copper), and agricultural commodities.
Evaluate macroeconomic supply/demand imbalances, geopolitical risk factors, inflation trends, and seasonal drivers to select the top 5 commodity investments.""",
    tools=[research_asset, rank_domain_top_assets],
)

# Root Coordinator Agent
root_agent = Agent(
    name="investment_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Lead Investment Coordinator overseeing autonomous subagents for stocks, ETFs, cryptos, and commodities.",
    instruction="""You are the Lead Investment Coordinator.
You manage 4 dedicated autonomous domain subagents:
1. `stock_agent`: Equities & corporate earnings specialist.
2. `etf_agent`: Exchange-traded funds & macro sector specialist.
3. `crypto_agent`: Digital assets & blockchain market specialist.
4. `commodity_agent`: Energy, precious metals, and commodity specialist.

When asked for analysis or recommendations:
- Delegate queries to the appropriate domain subagent or retrieve complete multi-domain market overviews using your tools.
- Provide clear, professional, structured investment intelligence including ticker, asset name, current price, forecast gain (%), historical performance, and key market catalysts.
- Emphasize diversification across the 4 asset classes.""",
    sub_agents=[stock_agent, etf_agent, crypto_agent, commodity_agent],
    tools=[research_asset, rank_domain_top_assets, get_market_overview],
)

app = App(
    root_agent=root_agent,
    name="app",
)
