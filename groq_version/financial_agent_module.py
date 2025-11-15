"""
Financial Agent Module (Groq Version)

This module implements a financial agent using phidata framework
with yfinance capabilities for stock market data analysis and Groq LLM.

The Financial Agent retrieves and analyzes stock market data including:
    - Real-time stock prices
    - Analyst recommendations
    - Company fundamentals (revenue, earnings, ratios)
    - Company news and updates

Key Features:
    - Stock data retrieval using yfinance
    - Ticker symbol validation
    - Error handling for invalid tickers
    - Structured data display in tables
    - Comprehensive logging
    - Powered by Groq's llama-3.3-70b-versatile model

Configuration:
    - Model: Groq "llama-3.3-70b-versatile"
    - Tools: YFinanceTools with multiple capabilities
    - Output: Markdown with tabular data

Example:
    >>> from financial_agent_module_groq import financial_agent
    >>> response = financial_agent.run("What is the current price of AAPL?")
    >>> print(response.content)
"""

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
import yfinance as yf
from typing import Optional
from error_handler import AgentExecutionError, ValidationError, handle_agent_execution_error
from logger import get_logger, log_query, log_error, log_response
import time

# Initialize logger
logger = get_logger("financial_agent")


def validate_ticker(ticker: str) -> tuple[bool, Optional[str]]:
    """
    Validate if a ticker symbol exists and is valid.
    
    Args:
        ticker: Stock ticker symbol to validate
        
    Returns:
        tuple: (is_valid, error_message)
        
    Raises:
        ValidationError: If ticker validation fails
    """
    try:
        stock = yf.Ticker(ticker)
        # Try to fetch basic info to verify ticker exists
        info = stock.info
        
        # Check if we got valid data back
        if not info or 'symbol' not in info:
            raise ValidationError(
                message=f"Invalid ticker symbol: '{ticker}'",
                details={
                    "ticker": ticker,
                    "suggestion": "Please verify the ticker symbol and try again"
                }
            )
        
        return True, None
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(
            message=f"Error validating ticker '{ticker}'",
            details={
                "ticker": ticker,
                "original_error": str(e),
                "suggestion": "Please check the ticker symbol"
            }
        )


def create_financial_agent() -> Agent:
    """
    Create and configure the Financial Agent with Groq and error handling.
    
    The agent is configured with YFinanceTools to retrieve comprehensive
    stock market data including prices, recommendations, fundamentals, and news.
    
    Configuration:
        - Name: "FinancialAgent"
        - Role: Fetch financial details about stocks
        - Model: Groq "llama-3.3-70b-versatile"
        - Tools: YFinanceTools with all capabilities enabled
        - Output: Markdown formatted with tables
    
    YFinanceTools Capabilities:
        - analyst_recommendations: Get analyst ratings and price targets
        - stock_price: Retrieve current and historical stock prices
        - stock_fundamentals: Access financial metrics and ratios
        - company_news: Fetch recent company news and updates
    
    Returns:
        Agent: Configured financial agent with YFinance tool
        
    Example:
        >>> agent = create_financial_agent()
        >>> response = agent.run("Show me TSLA analyst recommendations")
    """
    financial_agent = Agent(
        name="FinancialAgent",
        role="Fetch financial details about stocks.",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[
            YFinanceTools(
                analyst_recommendations=True,  # Enable analyst recommendations
                stock_price=True,              # Enable stock price data
                stock_fundamentals=True,       # Enable fundamental data
                company_news=True              # Enable company news
            )
        ],
        instructions=[
            "Use tables to display the data",
            "Provide clear and structured financial information",
            "Include relevant metrics and context",
            "If a ticker symbol is invalid or not found, provide a clear error message to the user",
            "Handle errors gracefully and suggest checking the ticker symbol"
        ],
        show_tool_calls=True,  # Display which tools are called during execution
        markdown=True          # Enable Markdown formatting for responses
    )
    
    return financial_agent


def query_financial_agent(query: str, agent: Optional[Agent] = None) -> str:
    """
    Query the financial agent with error handling for invalid tickers.
    
    Args:
        query: User query about stocks
        agent: Optional pre-configured agent (uses default if not provided)
        
    Returns:
        str: Agent response or error message
        
    Raises:
        AgentExecutionError: If agent execution fails
    """
    if agent is None:
        agent = financial_agent
    
    # Log the query
    log_query(logger, query, agent_name="FinancialAgent")
    
    start_time = time.time()
    success = False
    
    try:
        # Execute the query through the agent
        logger.info("Executing financial agent query")
        response = agent.run(query)
        success = True
        
        # Log successful response
        execution_time = time.time() - start_time
        log_response(logger, success=True, agent_name="FinancialAgent", execution_time=execution_time)
        
        return response
    except Exception as e:
        # Log the error
        log_error(logger, e, context={"query": query}, agent_name="FinancialAgent")
        
        # Use centralized error handler
        error = handle_agent_execution_error(e, agent_name="FinancialAgent")
        
        # Log failed response
        execution_time = time.time() - start_time
        log_response(logger, success=False, agent_name="FinancialAgent", execution_time=execution_time)
        
        # Format error for display
        error_dict = error.to_dict()
        return (
            f"❌ **Error**: {error_dict['error']}\n\n"
            f"**Error Type**: {error_dict['error_type']}\n"
        )


# Initialize the agent for direct import
# This allows users to import and use the agent directly:
# from financial_agent_module_groq import financial_agent
financial_agent = create_financial_agent()
