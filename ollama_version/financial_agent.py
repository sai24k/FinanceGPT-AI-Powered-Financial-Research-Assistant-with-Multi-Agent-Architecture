"""
Financial AI Agent - Local Test Script

This script provides a local testing interface for the Financial AI Agent System.
It initializes all agents (Web Search, Financial, and Multi-Agent) and allows
execution of sample queries with formatted console output.

Usage:
    python financial_agent.py                           # Run sample queries
    python financial_agent.py --query "Your question"   # Run custom query
    python financial_agent.py --query "Your question" --agent financial  # Use specific agent
"""

import os
import sys
import argparse
from config import load_config
from multi_agent import multi_agent_system
from web_search_agent import web_search_agent
from financial_agent_module import financial_agent
from error_handler import (
    FinancialAgentError,
    ConfigurationError,
    AgentExecutionError,
    handle_configuration_error,
    handle_agent_execution_error
)
from logger import setup_logging, get_logger, log_query, log_error, log_response
import time

# Set up logging
setup_logging(level="INFO", enable_console=False)  # Disable console to avoid cluttering output
logger = get_logger("main")


def print_separator(char="=", length=80):
    """
    Print a separator line for better output formatting.
    
    Args:
        char: Character to use for the separator line (default: "=")
        length: Length of the separator line (default: 80)
    """
    print(char * length)


def print_header(text):
    """
    Print a formatted header with separators.
    
    Args:
        text: Header text to display
    """
    print_separator()
    print(f"  {text}")
    print_separator()


def format_response(response):
    """
    Format and display the agent response.
    
    Handles different response types from phidata agents and formats
    them for console display with proper separators.
    
    Args:
        response: Agent response object or string
            - If response has 'content' attribute, displays that
            - If response is a string, displays it directly
            - Otherwise, converts to string and displays
    """
    print("\n[RESPONSE]:")
    print_separator("-")
    
    # Handle different response types
    if hasattr(response, 'content'):
        print(response.content)
    elif isinstance(response, str):
        print(response)
    else:
        print(str(response))
    
    print_separator("-")


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Financial AI Agent System - Local Test Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python financial_agent.py
  python financial_agent.py --query "What is the current price of AAPL?"
  python financial_agent.py --query "Latest AI news" --agent web
  python financial_agent.py --query "NVIDIA stock analysis" --agent financial
  python financial_agent.py --query "Compare AAPL and MSFT" --agent multi
        """
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Custom query to execute (if not provided, runs sample queries)'
    )
    
    parser.add_argument(
        '--agent', '-a',
        type=str,
        choices=['financial', 'web', 'multi'],
        default='multi',
        help='Specify which agent to use: financial, web, or multi (default: multi)'
    )
    
    return parser.parse_args()


def execute_query(query, agent_type='multi'):
    """
    Execute a query using the specified agent.
    
    This function routes the query to the appropriate agent based on the
    agent_type parameter, executes the query, and handles any errors that occur.
    
    Args:
        query: User query string to execute
        agent_type: Type of agent to use:
            - 'financial': Use Financial Agent only
            - 'web': Use Web Search Agent only
            - 'multi': Use Multi-Agent System (default)
    
    Returns:
        bool: True if query executed successfully, False otherwise
    """
    # Select the appropriate agent based on agent_type
    # Each agent is specialized for different types of queries
    agent_map = {
        'financial': ('Financial Agent', financial_agent),
        'web': ('Web Search Agent', web_search_agent),
        'multi': ('Multi-Agent System', multi_agent_system)
    }
    
    agent_name, agent = agent_map.get(agent_type, ('Multi-Agent System', multi_agent_system))
    
    print(f"\n[*] Using: {agent_name}")
    print(f"[?] Query: {query}")
    print_separator("-")
    
    # Log the query
    log_query(logger, query, agent_name=agent_name)
    
    start_time = time.time()
    
    try:
        logger.info(f"Executing query with {agent_name}")
        response = agent.run(query)
        format_response(response)
        
        # Display tool calls if available
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print("\n[*] Tool Calls:")
            for tool_call in response.tool_calls:
                print(f"  - {tool_call}")
        
        # Log successful execution
        execution_time = time.time() - start_time
        log_response(logger, success=True, agent_name=agent_name, execution_time=execution_time)
        
        return True
    except FinancialAgentError as e:
        # Log the error
        log_error(logger, e, context={"query": query}, agent_name=agent_name)
        
        # Handle custom errors
        error_dict = e.to_dict()
        print(f"\n[-] Error: {error_dict['error']}")
        print(f"Error Type: {error_dict['error_type']}")
        if error_dict.get('details'):
            print(f"Details: {error_dict['details']}")
        
        # Log failed execution
        execution_time = time.time() - start_time
        log_response(logger, success=False, agent_name=agent_name, execution_time=execution_time)
        
        return False
    except Exception as e:
        # Log the error
        log_error(logger, e, context={"query": query}, agent_name=agent_name)
        
        # Handle unexpected errors
        error = handle_agent_execution_error(e, agent_name=agent_name)
        error_dict = error.to_dict()
        print(f"\n[-] Error: {error_dict['error']}")
        print(f"Error Type: {error_dict['error_type']}")
        
        # Log failed execution
        execution_time = time.time() - start_time
        log_response(logger, success=False, agent_name=agent_name, execution_time=execution_time)
        
        return False


def run_sample_queries():
    """
    Execute predefined sample queries to demonstrate functionality.
    
    This function runs three sample queries to showcase the capabilities
    of each agent type:
        1. Financial Agent - Stock price query
        2. Web Search Agent - General web search
        3. Multi-Agent System - Combined query requiring both agents
    """
    print("\n" + "=" * 80)
    print("SAMPLE QUERY EXECUTION")
    print("=" * 80)
    
    # Sample Query 1: Financial data
    print("\n\n[1] Query 1: Financial Data")
    execute_query("What is the current price of AAPL?", agent_type='financial')
    
    # Sample Query 2: Web search
    print("\n\n[2] Query 2: Web Search")
    execute_query("Latest news about artificial intelligence", agent_type='web')
    
    # Sample Query 3: Multi-agent query
    print("\n\n[3] Query 3: Multi-Agent Coordination")
    execute_query(
        "Summarize analyst recommendations and latest news for NVIDIA",
        agent_type='multi'
    )
    
    # Completion message
    print("\n" + "=" * 80)
    print("[+] Sample queries completed!")
    print("=" * 80)


def main():
    """
    Main execution function for local testing.
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    print_header("Financial AI Agent System - Local Test")
    
    # Step 1: Load configuration
    print("\n[*] Loading configuration...")
    logger.info("Starting Financial AI Agent System")
    try:
        logger.info("Loading configuration")
        config = load_config()
        print("[+] Configuration loaded successfully")
        logger.info("Configuration loaded successfully")
        
        # Set API keys in environment
        os.environ['PHIDATA_API_KEY'] = config['phidata_api_key']
        os.environ['PHI_API_KEY'] = config['phidata_api_key']  # Phidata also checks PHI_API_KEY
        os.environ['GROQ_API_KEY'] = config['groq_api_key']
        # OpenAI key is optional
        if 'openai_api_key' in config:
            os.environ['OPENAI_API_KEY'] = config['openai_api_key']
        
    except ConfigurationError as e:
        log_error(logger, e, context={"stage": "configuration"})
        error_dict = e.to_dict()
        print(f"[-] Configuration Error: {error_dict['error']}")
        if error_dict.get('details'):
            print(f"Details: {error_dict['details']}")
        sys.exit(1)
    except Exception as e:
        log_error(logger, e, context={"stage": "configuration"})
        error = handle_configuration_error(e)
        error_dict = error.to_dict()
        print(f"[-] Configuration Error: {error_dict['error']}")
        sys.exit(1)
    
    # Step 2: Initialize agents
    print("\n[*] Initializing agents...")
    logger.info("Initializing agents")
    print("  - Web Search Agent: Ready")
    print("  - Financial Agent: Ready")
    print("  - Multi-Agent System: Ready")
    logger.info("All agents initialized successfully")
    
    # Step 3: Execute queries
    if args.query:
        # Execute custom query
        print("\n" + "=" * 80)
        print("CUSTOM QUERY EXECUTION")
        print("=" * 80)
        
        success = execute_query(args.query, agent_type=args.agent)
        
        if success:
            print("\n[+] Query completed successfully!")
        else:
            print("\n[-] Query failed!")
            sys.exit(1)
    else:
        # Run sample queries
        run_sample_queries()


if __name__ == "__main__":
    main()
