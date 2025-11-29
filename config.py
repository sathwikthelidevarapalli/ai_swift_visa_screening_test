# ==================================
# SwiftVisa Configuration Module
# ==================================

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings and configuration"""
    
    # Application Info
    APP_NAME: str = "SwiftVisa"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-Powered Visa Eligibility Checker"
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # Vector Store
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "vectorstore")
    TOP_K: int = int(os.getenv("TOP_K", "5"))
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    WORKERS: int = int(os.getenv("WORKERS", "4"))
    RELOAD: bool = os.getenv("RELOAD", "False").lower() == "true"
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8501",
        "https://swiftvisa.streamlit.app"
    ]
    
    # Add custom origins from environment
    custom_origins = os.getenv("ALLOWED_ORIGINS", "")
    if custom_origins:
        ALLOWED_ORIGINS.extend(custom_origins.split(","))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/swiftvisa.log")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Data Paths
    DATA_RAW_DIR: str = "data/raw"
    DATA_CLEAN_DIR: str = "data/clean"
    DATA_CHUNKS_DIR: str = "data/chunks"
    LOGS_DIR: str = "logs"
    
    # Rate Limiting (Future)
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    
    # LLM Configuration
    LLM_TEMPERATURE: float = 0.0
    LLM_MAX_TOKENS: int = 1000
    LLM_MODEL_OPENAI: str = "gpt-3.5-turbo"
    LLM_MODEL_GEMINI: str = "gemini-1.5-pro"
    
    # Feature Flags
    ENABLE_MONITORING: bool = os.getenv("ENABLE_MONITORING", "False").lower() == "true"
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "False").lower() == "true"
    ENABLE_CACHING: bool = os.getenv("ENABLE_CACHING", "False").lower() == "true"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        import os
        
        errors = []
        
        # Check if vectorstore exists
        if not os.path.exists(cls.CHROMA_DB_DIR):
            errors.append(f"Vectorstore directory not found: {cls.CHROMA_DB_DIR}")
        
        # Check if data directories exist
        for dir_path in [cls.DATA_RAW_DIR, cls.DATA_CLEAN_DIR, cls.LOGS_DIR]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
        
        # Warn if no API keys (non-critical)
        if not cls.OPENAI_API_KEY and not cls.GEMINI_API_KEY:
            print("⚠️  Warning: No LLM API keys found. System will run in retrieval-only mode.")
        
        if errors:
            for error in errors:
                print(f"❌ Configuration Error: {error}")
            return False
        
        return True
    
    @classmethod
    def get_info(cls) -> dict:
        """Get configuration information (safe for API exposure)"""
        return {
            "app_name": cls.APP_NAME,
            "app_version": cls.APP_VERSION,
            "embedding_model": cls.EMBEDDING_MODEL,
            "top_k": cls.TOP_K,
            "llm_available": bool(cls.OPENAI_API_KEY or cls.GEMINI_API_KEY),
            "openai_configured": bool(cls.OPENAI_API_KEY and cls.OPENAI_API_KEY.startswith("sk-")),
            "gemini_configured": bool(cls.GEMINI_API_KEY and len(cls.GEMINI_API_KEY) > 20),
            "vectorstore_path": cls.CHROMA_DB_DIR,
            "log_level": cls.LOG_LEVEL
        }


# Create settings instance
settings = Settings()

# Validate on import
if __name__ != "__main__":
    settings.validate()
