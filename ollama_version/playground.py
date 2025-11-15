"""
FastAPI Playground for Financial AI Agent System

This module creates a FastAPI deployment service using phidata's Playground
to expose the Web Search Agent and Financial Agent via REST API with
interactive documentation.
"""

import os
from phi.playground import Playground, serve_playground_app
from dotenv import load_dotenv
from web_search_agent import web_search_agent
from financial_agent_module import financial_agent
from error_handler import ConfigurationError, handle_configuration_error
from logger import setup_logging, get_logger

# Set up logging
setup_logging(level="INFO", log_file="financial_agent.log")
logger = get_logger("playground")


def validate_api_keys():
    """
    Validate that all required API keys are present before starting the server.
    
    Raises:
        ConfigurationError: If any required API keys are missing with a clear error message
    """
    required_keys = ['PHIDATA_API_KEY', 'GROQ_API_KEY']
    missing_keys = []
    
    for key in required_keys:
        value = os.getenv(key)
        if not value or value.strip() == '' or 'your_' in value.lower():
            missing_keys.append(key)
    
    if missing_keys:
        raise ConfigurationError(
            message="Missing required API keys for FastAPI startup",
            details={
                "missing_keys": missing_keys,
                "required_keys": required_keys,
                "steps": [
                    "Create a .env file in the project root (use .env.example as template)",
                    "Add your actual API keys (replace placeholder values)",
                    "Restart the server"
                ]
            }
        )


# Load environment variables from .env file
# This must be done before accessing any environment variables
logger.info("Starting FastAPI Playground service")
load_dotenv()

# Validate API keys before proceeding
# This ensures the server won't start with missing or invalid keys
logger.info("Validating API keys")
try:
    validate_api_keys()
    logger.info("API keys validated successfully")
except ConfigurationError as e:
    logger.error(f"API key validation failed: {e.message}")
    raise

# Set API keys from environment variables
# These are required for phidata and OpenAI integrations
phi_api_key = os.getenv('PHIDATA_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

# Set environment variables for phidata
# Phidata expects PHI_API_KEY (without the 'DATA' suffix)
if phi_api_key:
    os.environ['PHI_API_KEY'] = phi_api_key
if openai_api_key:
    os.environ['OPENAI_API_KEY'] = openai_api_key

# Create Playground app with both agents
# The Playground automatically generates REST API endpoints for each agent
logger.info("Creating Playground app with agents")
app = Playground(agents=[financial_agent, web_search_agent]).get_app()
logger.info("Playground app created successfully")

if __name__ == "__main__":
    # Serve the playground app with hot reload enabled for development
    # Hot reload automatically restarts the server when code changes are detected
    # Access the API documentation at http://localhost:7777/docs
    logger.info("Starting Playground server with hot reload")
    serve_playground_app("playground:app", reload=True)
