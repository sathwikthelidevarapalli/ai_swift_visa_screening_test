# ==================================
# SwiftVisa Logging Configuration
# ==================================

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path


def setup_logging(
    log_level: str = "INFO",
    log_file: str = "logs/swiftvisa.log",
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Setup comprehensive logging for SwiftVisa application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        log_format: Log message format
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup log files to keep
    
    Returns:
        Configured logger instance
    """
    
    # Create logs directory if it doesn't exist
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert log level string to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger("swiftvisa")
    logger.setLevel(numeric_level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    simple_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S"
    )
    
    # Console Handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File Handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Error File Handler (separate file for errors)
    error_log_file = log_file.replace(".log", "_errors.log")
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    # Log startup message
    logger.info("=" * 80)
    logger.info(f"SwiftVisa Logging Initialized - Level: {log_level}")
    logger.info(f"Log File: {log_file}")
    logger.info(f"Error Log: {error_log_file}")
    logger.info("=" * 80)
    
    return logger


def get_logger(name: str = "swiftvisa") -> logging.Logger:
    """
    Get logger instance
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Middleware for request logging
class RequestLoggingMiddleware:
    """FastAPI middleware for logging all requests"""
    
    def __init__(self, app, logger: logging.Logger):
        self.app = app
        self.logger = logger
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = datetime.now()
            
            # Log request
            self.logger.info(
                f"→ {scope['method']} {scope['path']} "
                f"from {scope['client'][0] if scope.get('client') else 'unknown'}"
            )
            
            # Process request
            await self.app(scope, receive, send)
            
            # Log completion
            duration = (datetime.now() - start_time).total_seconds()
            self.logger.info(
                f"← {scope['method']} {scope['path']} "
                f"completed in {duration:.3f}s"
            )
        else:
            await self.app(scope, receive, send)


# Exception logging decorator
def log_exceptions(logger: logging.Logger = None):
    """
    Decorator to log exceptions from functions
    
    Args:
        logger: Logger instance (optional)
    """
    if logger is None:
        logger = get_logger()
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"Exception in {func.__name__}: {str(e)}",
                    exc_info=True
                )
                raise
        return wrapper
    return decorator


# Performance logging context manager
class LogExecutionTime:
    """Context manager to log execution time"""
    
    def __init__(self, operation_name: str, logger: logging.Logger = None):
        self.operation_name = operation_name
        self.logger = logger or get_logger()
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.debug(f"Starting: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.info(
                f"Completed: {self.operation_name} in {duration:.3f}s"
            )
        else:
            self.logger.error(
                f"Failed: {self.operation_name} after {duration:.3f}s - {exc_val}"
            )
        
        return False  # Don't suppress exceptions


if __name__ == "__main__":
    # Test logging setup
    logger = setup_logging(log_level="DEBUG")
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    print("\n✅ Logging test complete. Check logs/swiftvisa.log")
