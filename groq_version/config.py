"""
Configuration management module for Financial AI Agent System.

This module handles loading and validating environment variables from .env file,
ensuring all required API keys are present before the application starts.
"""

import os
from typing import Dict
from dotenv import load_dotenv
from error_handler import ConfigurationError
from logger import get_logger

# Initialize logger
logger = get_logger("config")


def load_config() -> Dict[str, str]:
    """
    Load and validate configuration from .env file.
    
    This function loads environment variables from a .env file and validates
    that all required API keys are present. It provides clear error messages
    for missing configuration.
    
    Returns:
        Dict[str, str]: Dictionary containing validated API keys with keys:
            - 'phidata_api_key': Phidata API key
            - 'groq_api_key': Groq API key  
            - 'openai_api_key': OpenAI API key
    
    Raises:
        FileNotFoundError: If .env file is not found
        ValueError: If any required API keys are missing
    
    Example:
        >>> config = load_config()
        >>> phidata_key = config['phidata_api_key']
    """
    # Check if .env file exists
    if not os.path.exists('.env'):
        logger.error("Configuration file '.env' not found")
        raise ConfigurationError(
            message=(
                "Configuration file '.env' not found. "
                "Please create a .env file in the project root directory. "
                "You can use .env.example as a template."
            ),
            details={
                "steps": [
                    "Copy .env.example to .env",
                    "Replace placeholder values with your actual API keys"
                ],
                "required_keys": ["PHIDATA_API_KEY", "GROQ_API_KEY", "OPENAI_API_KEY"]
            }
        )
    
    # Load environment variables from .env file
    logger.info("Loading configuration from .env file")
    load_dotenv()
    
    # Define required API keys
    # Maps environment variable names to config dictionary keys
    # Required keys for the system to function:
    #   - PHIDATA_API_KEY: Required for phidata framework
    #   - GROQ_API_KEY: Required for Groq LLM model
    required_keys = {
        'PHIDATA_API_KEY': 'phidata_api_key',
        'GROQ_API_KEY': 'groq_api_key',
    }
    
    # Optional keys
    optional_keys = {
        'OPENAI_API_KEY': 'openai_api_key'
    }
    
    # Validate that all required keys are present
    # Check each key for:
    #   1. Existence (not None)
    #   2. Non-empty value
    #   3. Not a placeholder (doesn't contain 'your_')
    missing_keys = []
    config = {}
    
    # Check required keys
    for env_key, config_key in required_keys.items():
        value = os.getenv(env_key)
        if not value or value.strip() == '' or 'your_' in value.lower():
            missing_keys.append(env_key)
        else:
            config[config_key] = value
    
    # Check optional keys (don't fail if missing)
    for env_key, config_key in optional_keys.items():
        value = os.getenv(env_key)
        if value and value.strip() != '' and 'your_' not in value.lower():
            config[config_key] = value
            logger.info(f"Optional key {env_key} loaded")
        else:
            logger.info(f"Optional key {env_key} not configured (skipping)")
    
    # Raise error if any required keys are missing
    if missing_keys:
        logger.error(f"Missing required API keys: {', '.join(missing_keys)}")
        raise ConfigurationError(
            message=f"Missing or invalid required API keys: {', '.join(missing_keys)}",
            details={
                "missing_keys": missing_keys,
                "required_keys": ["PHIDATA_API_KEY", "GROQ_API_KEY"],
                "note": "Make sure to replace placeholder values with your actual API keys"
            }
        )
    
    logger.info("Configuration loaded successfully")
    return config


def get_api_key(key_name: str) -> str:
    """
    Get a specific API key from environment variables.
    
    Args:
        key_name: Name of the API key to retrieve (e.g., 'PHIDATA_API_KEY')
    
    Returns:
        str: The API key value
    
    Raises:
        ValueError: If the specified key is not found or is invalid
    """
    value = os.getenv(key_name)
    if not value or value.strip() == '' or 'your_' in value.lower():
        raise ConfigurationError(
            message=f"API key '{key_name}' is not set or is invalid",
            details={
                "key_name": key_name,
                "note": "Please check your .env file and ensure it contains a valid value"
            }
        )
    return value
