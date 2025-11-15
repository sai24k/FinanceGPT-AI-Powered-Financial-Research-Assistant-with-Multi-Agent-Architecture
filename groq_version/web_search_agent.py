"""
Web Search Agent Module (Groq Version)

This module implements a web search agent using phidata framework
with DuckDuckGo search capabilities and Groq LLM.

Key Features:
    - Web search using DuckDuckGo API
    - Markdown-formatted results
    - Source URL inclusion for all information
    - Tool call transparency
    - Powered by Groq's llama-3.3-70b-versatile model

Configuration:
    - Model: Groq "llama-3.3-70b-versatile"
    - Tools: DuckDuckGo search
    - Output: Markdown with citations

Example:
    >>> from web_search_agent_groq import web_search_agent
    >>> response = web_search_agent.run("Latest AI news")
    >>> print(response.content)
"""

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo


def create_web_search_agent() -> Agent:
    """
    Create and configure the Web Search Agent with Groq.
    
    The agent is configured to perform web searches using DuckDuckGo
    and format results in Markdown with proper source citations.
    
    Configuration:
        - Name: "WebSearchAgent"
        - Role: Search the web for information
        - Model: Groq "llama-3.3-70b-versatile"
        - Tools: DuckDuckGo search tool
        - Output: Markdown formatted with sources
    
    Returns:
        Agent: Configured web search agent with DuckDuckGo tool
        
    Example:
        >>> agent = create_web_search_agent()
        >>> response = agent.run("Python programming tutorials")
    """
    web_search_agent = Agent(
        name="WebSearchAgent",
        role="Search the web for information.",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[DuckDuckGo()],
        instructions=[
            "Always include sources and URLs in your responses",
            "Format all results in Markdown format",
            "Provide clear citations for all information"
        ],
        show_tool_calls=True,  # Display which tools are called during execution
        markdown=True  # Enable Markdown formatting for responses
    )
    
    return web_search_agent


# Initialize the agent for direct import
# This allows users to import and use the agent directly:
# from web_search_agent_groq import web_search_agent
web_search_agent = create_web_search_agent()
