"""
Logging Infrastructure Module

This module provides centralized logging configuration for the Financial AI Agent System.
It ensures API keys are never logged and provides structured logging for queries and errors.
"""

import logging
import re
import sys
from typing import Optional, Dict, Any
from datetime import datetime


class SensitiveDataFilter(logging.Filter):
    """Filter to remove sensitive data (API keys) from log messages."""
    
    # Patterns to detect potential API keys
    SENSITIVE_PATTERNS = [
        r'PHIDATA_API_KEY[=:]\s*[^\s]+',
        r'GROQ_API_KEY[=:]\s*[^\s]+',
        r'OPENAI_API_KEY[=:]\s*[^\s]+',
        r'api[_-]?key["\']?\s*[=:]\s*["\']?[a-zA-Z0-9_-]{20,}',
        r'token["\']?\s*[=:]\s*["\']?[a-zA-Z0-9_-]{20,}',
        r'sk-[a-zA-Z0-9]{20,}',  # OpenAI key pattern
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log records to remove sensitive data.
        
        Args:
            record: Log record to filter
            
        Returns:
            bool: Always True (we modify but don't block records)
        """
        # Sanitize the message
        if isinstance(record.msg, str):
            record.msg = self._sanitize_text(record.msg)
        
        # Sanitize arguments
        if record.args:
            if isinstance(record.args, dict):
                record.args = {k: self._sanitize_value(v) for k, v in record.args.items()}
            elif isinstance(record.args, tuple):
                record.args = tuple(self._sanitize_value(arg) for arg in record.args)
        
        return True
    
    def _sanitize_text(self, text: str) -> str:
        """
        Remove sensitive data from text.
        
        Args:
            text: Text to sanitize
            
        Returns:
            str: Sanitized text with sensitive data replaced
        """
        for pattern in self.SENSITIVE_PATTERNS:
            text = re.sub(pattern, '[REDACTED_API_KEY]', text, flags=re.IGNORECASE)
        return text
    
    def _sanitize_value(self, value: Any) -> Any:
        """
        Sanitize a value (recursively for dicts and lists).
        
        Args:
            value: Value to sanitize
            
        Returns:
            Sanitized value
        """
        if isinstance(value, str):
            return self._sanitize_text(value)
        elif isinstance(value, dict):
            return {k: self._sanitize_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return type(value)(self._sanitize_value(item) for item in value)
        return value


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with structured information.
        
        Args:
            record: Log record to format
            
        Returns:
            str: Formatted log message
        """
        # Add timestamp
        record.timestamp = datetime.utcnow().isoformat()
        
        # Format the base message
        message = super().format(record)
        
        # Add extra context if available
        if hasattr(record, 'query_id'):
            message = f"[Query:{record.query_id}] {message}"
        
        if hasattr(record, 'agent_name'):
            message = f"[Agent:{record.agent_name}] {message}"
        
        return message


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True
) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        enable_console: Whether to enable console logging
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("financial_agent")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = StructuredFormatter(
        fmt='%(timestamp)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add sensitive data filter
    sensitive_filter = SensitiveDataFilter()
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        console_handler.setFormatter(formatter)
        console_handler.addFilter(sensitive_filter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        file_handler.addFilter(sensitive_filter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Optional logger name (defaults to 'financial_agent')
        
    Returns:
        logging.Logger: Logger instance
    """
    if name:
        return logging.getLogger(f"financial_agent.{name}")
    return logging.getLogger("financial_agent")


def log_query(
    logger: logging.Logger,
    query: str,
    agent_name: str,
    query_id: Optional[str] = None
) -> None:
    """
    Log a query without sensitive data.
    
    Args:
        logger: Logger instance
        query: User query (will be sanitized)
        agent_name: Name of the agent processing the query
        query_id: Optional unique query identifier
    """
    # Create extra context
    extra = {
        'agent_name': agent_name,
        'query_id': query_id or datetime.utcnow().isoformat()
    }
    
    # Sanitize query to remove potential sensitive data
    sanitized_query = _sanitize_query(query)
    
    logger.info(f"Processing query: {sanitized_query}", extra=extra)


def log_error(
    logger: logging.Logger,
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    agent_name: Optional[str] = None
) -> None:
    """
    Log an error with context.
    
    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Optional additional context
        agent_name: Optional agent name
    """
    extra = {}
    if agent_name:
        extra['agent_name'] = agent_name
    
    error_msg = f"Error occurred: {type(error).__name__}: {str(error)}"
    
    if context:
        # Sanitize context
        sanitized_context = _sanitize_dict(context)
        error_msg += f" | Context: {sanitized_context}"
    
    logger.error(error_msg, extra=extra, exc_info=True)


def log_response(
    logger: logging.Logger,
    success: bool,
    agent_name: str,
    query_id: Optional[str] = None,
    execution_time: Optional[float] = None
) -> None:
    """
    Log query response status.
    
    Args:
        logger: Logger instance
        success: Whether the query was successful
        agent_name: Name of the agent
        query_id: Optional query identifier
        execution_time: Optional execution time in seconds
    """
    extra = {
        'agent_name': agent_name,
        'query_id': query_id or datetime.utcnow().isoformat()
    }
    
    status = "SUCCESS" if success else "FAILED"
    msg = f"Query {status}"
    
    if execution_time is not None:
        msg += f" (execution time: {execution_time:.2f}s)"
    
    if success:
        logger.info(msg, extra=extra)
    else:
        logger.warning(msg, extra=extra)


def _sanitize_query(query: str) -> str:
    """
    Sanitize a query string to remove potential sensitive data.
    
    Args:
        query: Query string to sanitize
        
    Returns:
        str: Sanitized query
    """
    # Remove potential API keys or tokens
    patterns = [
        r'sk-[a-zA-Z0-9]{20,}',
        r'[a-zA-Z0-9_-]{40,}',  # Long strings that might be keys
    ]
    
    sanitized = query
    for pattern in patterns:
        sanitized = re.sub(pattern, '[REDACTED]', sanitized)
    
    return sanitized


def _sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize a dictionary to remove sensitive data.
    
    Args:
        data: Dictionary to sanitize
        
    Returns:
        Dict: Sanitized dictionary
    """
    sensitive_keys = ['api_key', 'token', 'password', 'secret', 'key']
    
    sanitized = {}
    for key, value in data.items():
        # Check if key contains sensitive terms
        if any(term in key.lower() for term in sensitive_keys):
            sanitized[key] = '[REDACTED]'
        elif isinstance(value, dict):
            sanitized[key] = _sanitize_dict(value)
        elif isinstance(value, str):
            sanitized[key] = _sanitize_query(value)
        else:
            sanitized[key] = value
    
    return sanitized
