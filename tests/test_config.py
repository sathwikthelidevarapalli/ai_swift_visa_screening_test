"""
Configuration Tests
Tests for application configuration and settings
"""

import pytest
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestConfigModule:
    """Test configuration module"""
    
    def test_config_import(self):
        """Test that config module can be imported"""
        try:
            from config import settings
            assert settings is not None
        except ImportError as e:
            pytest.fail(f"Could not import config: {e}")
    
    def test_settings_attributes(self):
        """Test that settings has required attributes"""
        from config import settings
        
        required_attrs = [
            'APP_NAME',
            'APP_VERSION',
            'CHROMA_DB_DIR',
            'TOP_K',
            'HOST',
            'PORT',
            'EMBEDDING_MODEL'
        ]
        
        for attr in required_attrs:
            assert hasattr(settings, attr), f"Settings missing attribute: {attr}"
    
    def test_vectorstore_path(self):
        """Test vectorstore path configuration"""
        from config import settings
        
        assert settings.CHROMA_DB_DIR is not None
        assert isinstance(settings.CHROMA_DB_DIR, str)
    
    def test_top_k_value(self):
        """Test TOP_K configuration"""
        from config import settings
        
        assert isinstance(settings.TOP_K, int)
        assert settings.TOP_K > 0
        assert settings.TOP_K <= 20
    
    def test_settings_validation(self):
        """Test settings validation method"""
        from config import settings
        
        # Validation should pass (or handle gracefully)
        try:
            is_valid = settings.validate()
            assert isinstance(is_valid, bool)
        except Exception as e:
            pytest.fail(f"Settings validation failed: {e}")


class TestEnvironmentVariables:
    """Test environment variable handling"""
    
    def test_env_file_exists(self):
        """Test that .env.example exists as template"""
        assert os.path.exists(".env.example"), ".env.example template not found"
    
    def test_required_directories(self):
        """Test that required directories exist"""
        required_dirs = [
            "data",
            "data/clean",
            "vectorstore",
            "logs"
        ]
        
        for dir_path in required_dirs:
            assert os.path.exists(dir_path), f"Required directory not found: {dir_path}"


class TestLoggingConfig:
    """Test logging configuration"""
    
    def test_logging_config_import(self):
        """Test that logging_config can be imported"""
        try:
            import logging_config
            assert logging_config is not None
        except ImportError as e:
            pytest.fail(f"Could not import logging_config: {e}")
    
    def test_setup_logging(self):
        """Test setup_logging function"""
        try:
            from logging_config import setup_logging
            logger = setup_logging(log_level="INFO", log_file="logs/test.log")
            assert logger is not None
            assert hasattr(logger, 'info')
            assert hasattr(logger, 'error')
        except Exception as e:
            pytest.fail(f"setup_logging failed: {e}")
    
    def test_get_logger(self):
        """Test get_logger function"""
        try:
            from logging_config import get_logger
            logger = get_logger("test")
            assert logger is not None
        except Exception as e:
            pytest.fail(f"get_logger failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
