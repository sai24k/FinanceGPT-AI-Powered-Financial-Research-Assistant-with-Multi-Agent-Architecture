"""
Multi-Agent System Module (Groq Version)

This module implements a multi-agent system that coordinates between
the Web Search Agent and Financial Agent to handle complex queries
requiring multiple data sources. Uses Groq LLM for coordination.

The Multi-Agent System acts as an orchestrator that:
    - Analyzes user queries to determine required data sources
    - Delegates tasks to specialized agents (Financial, Web Search)
    - Combines results from multiple agents
    - Synthesizes comprehensive responses

Key Features:
    - Intelligent query routing to appropriate agents
    - Parallel or sequential agent execution
    - Result synthesis and summarization
    - Comprehensive context from multiple sources
    - Powered by Groq's llama-3.3-70b-versatile model

Configuration:
    - Model: Groq "llama-3.3-70b-versatile"
    - Team: Web Search Agent + Financial Agent
    - Output: Unified Markdown response

Example:
    >>> from multi_agent_groq import multi_agent_system
    >>> response = multi_agent_system.run(
    ...     "Compare AAPL and MSFT stock prices and search for tech industry trends"
    ... )
    >>> print(response.content)
"""

from phi.agent import Agent
from phi.model.groq import Groq
from web_search_agent_groq import web_search_agent
from financial_agent_module_groq import financial_agent


def create_multi_agent_system() -> Agent:
    """
    Create and configure the Multi-Agent System with Groq.
    
    The multi-agent system coordinates between the Web Search Agent
    and Financial Agent to handle queries that require both financial
    data and web search capabilities. It intelligently routes queries
    to the appropriate agents and synthesizes their responses.
    
    Configuration:
        - Name: "MultiAgentSystem"
        - Team: [Web Search Agent, Financial Agent]
        - Model: Groq "llama-3.3-70b-versatile"
        - Output: Unified Markdown response
    
    Coordination Logic:
        1. Analyze user query to determine required data sources
        2. Delegate to Financial Agent for stock data
        3. Delegate to Web Search Agent for general information
        4. Combine results from both agents
        5. Synthesize comprehensive response
    
    Returns:
        Agent: Configured multi-agent system with both specialized agents
        
    Example:
        >>> agent = create_multi_agent_system()
        >>> response = agent.run("NVIDIA stock analysis and AI market trends")
    """
    multi_agent = Agent(
        name="MultiAgentSystem",
        team=[web_search_agent, financial_agent],  # Specialized agents in the team
        model=Groq(id="llama-3.3-70b-versatile"),
        instructions=[
            "Coordinate between the Web Search Agent and Financial Agent to answer user queries",
            "Combine data from all agents into a unified response",
            "Summarize insights from multiple sources",
            "When a query requires financial data, delegate to the Financial Agent",
            "When a query requires web search, delegate to the Web Search Agent",
            "When a query requires both, coordinate both agents and synthesize the results",
            "Always provide comprehensive and well-structured responses",
            "Include relevant context from all data sources"
        ],
        show_tool_calls=True,  # Display which agents and tools are called
        markdown=True          # Enable Markdown formatting for responses
    )
    
    return multi_agent


# Initialize the multi-agent system for direct import
# This allows users to import and use the system directly:
# from multi_agent_groq import multi_agent_system
multi_agent_system = create_multi_agent_system()
