import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    
    # OpenAI Configuration
    OPENAI_MODEL = "gpt-3.5-turbo"
    
    # API Configuration
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # News API Configuration
    NEWS_API_BASE_URL = "https://newsapi.org/v2"
    
    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set"""
        required_vars = [
            "OPENAI_API_KEY",
            "SERPER_API_KEY", 
            "NEWS_API_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

config = Config()