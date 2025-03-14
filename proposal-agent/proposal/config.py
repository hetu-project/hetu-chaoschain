import os
from dotenv import load_dotenv
load_dotenv()

class Settings:

    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "o3-mini")
    BASE_URL = os.getenv("BASE_URL", "")

    default_temperature: float = 0.7
    max_tokens: int = 4000

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    def validate(self):
        missing_keys = []
        if not self.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        
        if missing_keys:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")
        
        return True

    def setup_environment(self):
        """Set environment variables for LangChain"""
        os.environ["OPENAI_API_BASE"] = self.BASE_URL
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY

settings = Settings()