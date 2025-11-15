"""
Centralized Error Handling Module

This module provides centralized error handling for the Financial AI Agent System,
including custom exception classes and error response formatting.
"""

from typing import Dict, Optional, Any
from enum import Enum


class ErrorType(Enum):
    """Enumeration of error types in the system."""
    CONFIGURATION_ERROR = "configuration_error"
    AGENT_EXECUTION_ERROR = "agent_execution_error"
    API_ERROR = "api_error"
    VALIDATION_ERROR = "validation_error"
    NETWORK_ERROR = "network_error"
    UNKNOWN_ERROR = "unknown_error"


class FinancialAgentError(Exception):
    """Base exception class for Financial AI Agent System."""
    
    def __init__(
        self,
        message: str,
        error_type: ErrorType = ErrorType.UNKNOWN_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the error.
        
        Args:
            message: Human-readable error message
            error_type: Type of error from ErrorType enum
            details: Additional context about the error
        """
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert error to dictionary format for API responses.
        
        Returns:
            Dict containing error information
        """
        return {
            "error": self.message,
            "error_type": self.error_type.value,
            "details": self.details
        }


class ConfigurationError(FinancialAgentError):
    """Exception raised for configuration-related errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.CONFIGURATION_ERROR,
            details=details
        )


class AgentExecutionError(FinancialAgentError):
    """Exception raised when agent execution fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.AGENT_EXECUTION_ERROR,
            details=details
        )


class APIError(FinancialAgentError):
    """Exception raised for API-related errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.API_ERROR,
            details=details
        )


class ValidationError(FinancialAgentError):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.VALIDATION_ERROR,
            details=details
        )


class NetworkError(FinancialAgentError):
    """Exception raised for network-related errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.NETWORK_ERROR,
            details=details
        )


def format_error_response(error: Exception) -> Dict[str, Any]:
    """
    Format any exception into a standardized error response.
    
    Args:
        error: Exception to format
        
    Returns:
        Dict containing formatted error information
    """
    if isinstance(error, FinancialAgentError):
        return error.to_dict()
    
    # Handle standard Python exceptions
    error_message = str(error)
    error_type = ErrorType.UNKNOWN_ERROR
    
    # Classify common exception types
    if isinstance(error, (FileNotFoundError, IOError)):
        error_type = ErrorType.CONFIGURATION_ERROR
    elif isinstance(error, ValueError):
        error_type = ErrorType.VALIDATION_ERROR
    elif isinstance(error, (ConnectionError, TimeoutError)):
        error_type = ErrorType.NETWORK_ERROR
    
    return {
        "error": error_message,
        "error_type": error_type.value,
        "details": {
            "exception_type": type(error).__name__
        }
    }


def handle_configuration_error(error: Exception) -> ConfigurationError:
    """
    Handle configuration-related errors.
    
    Args:
        error: Original exception
        
    Returns:
        ConfigurationError with formatted message
    """
    if isinstance(error, FileNotFoundError):
        return ConfigurationError(
            message=(
                "Configuration file not found. "
                "Please create a .env file with required API keys. "
                "Use .env.example as a template."
            ),
            details={"original_error": str(error)}
        )
    elif isinstance(error, ValueError):
        return ConfigurationError(
            message=str(error),
            details={"original_error": str(error)}
        )
    else:
        return ConfigurationError(
            message=f"Configuration error: {str(error)}",
            details={"original_error": str(error), "exception_type": type(error).__name__}
        )


def handle_agent_execution_error(error: Exception, agent_name: str = "Agent") -> AgentExecutionError:
    """
    Handle agent execution errors.
    
    Args:
        error: Original exception
        agent_name: Name of the agent that failed
        
    Returns:
        AgentExecutionError with formatted message
    """
    error_msg = str(error).lower()
    
    # Check for ticker-related errors
    if any(keyword in error_msg for keyword in ['ticker', 'symbol', 'not found']):
        return AgentExecutionError(
            message=(
                "Invalid ticker symbol. Please verify the ticker symbol and try again. "
                "Ensure the ticker is spelled correctly and the company is publicly traded."
            ),
            details={
                "agent": agent_name,
                "error_category": "invalid_ticker",
                "original_error": str(error)
            }
        )
    
    # Check for rate limit errors
    if any(keyword in error_msg for keyword in ['rate limit', 'too many requests', '429']):
        return AgentExecutionError(
            message=(
                "API rate limit exceeded. Please wait a moment and try again. "
                "If the issue persists, consider reducing query frequency."
            ),
            details={
                "agent": agent_name,
                "error_category": "rate_limit",
                "original_error": str(error)
            }
        )
    
    # Check for network errors
    if any(keyword in error_msg for keyword in ['connection', 'timeout', 'network']):
        return AgentExecutionError(
            message=(
                "Network error occurred while processing your request. "
                "Please check your internet connection and try again."
            ),
            details={
                "agent": agent_name,
                "error_category": "network",
                "original_error": str(error)
            }
        )
    
    # Generic agent execution error
    return AgentExecutionError(
        message=f"{agent_name} execution failed: {str(error)}",
        details={
            "agent": agent_name,
            "original_error": str(error),
            "exception_type": type(error).__name__
        }
    )


def handle_api_error(error: Exception, status_code: Optional[int] = None) -> APIError:
    """
    Handle API-related errors.
    
    Args:
        error: Original exception
        status_code: HTTP status code if available
        
    Returns:
        APIError with formatted message
    """
    details = {
        "original_error": str(error),
        "exception_type": type(error).__name__
    }
    
    if status_code:
        details["status_code"] = status_code
    
    # Map common status codes to user-friendly messages
    if status_code == 400:
        message = "Invalid request format. Please check your query and try again."
    elif status_code == 401:
        message = "Authentication failed. Please check your API keys."
    elif status_code == 403:
        message = "Access forbidden. Please verify your API key permissions."
    elif status_code == 404:
        message = "Resource not found. Please check your request."
    elif status_code == 429:
        message = "Rate limit exceeded. Please wait and try again."
    elif status_code == 500:
        message = "Internal server error. Please try again later."
    elif status_code == 503:
        message = "Service temporarily unavailable. Please try again later."
    else:
        message = f"API error occurred: {str(error)}"
    
    return APIError(message=message, details=details)
