from functools import lru_cache
import os
import json
from typing import Dict, Any, Optional
import yaml
from pathlib import Path
from config.config import AppConfig

class Settings:
    """Settings management with multiple configuration sources"""
    
    def __init__(self):
        self._config: Optional[AppConfig] = None
    
    def load_config(self) -> AppConfig:
        """
        Load configuration from multiple sources in order of precedence:
        1. Environment variables
        2. Config file (yaml/json)
        3. Default values
        """
        # Start with default configuration
        config_dict = self._load_default_config()
        
        # Load from config file if exists
        file_config = self._load_from_file()
        if file_config:
            config_dict.update(file_config)
        
        # Override with environment variables
        env_config = self._load_from_env()
        config_dict.update(env_config)
        
        # Create and validate config
        return AppConfig(**config_dict)
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "app_name": "Resume Customization API",
            "debug": False,
            "file_processor": {
                "max_file_size": 5 * 1024 * 1024,
                "supported_formats": [".pdf"],
                "temp_dir": "temp"
            },
            "models": {
                "default_model": "google"
            }
        }
    
    def _load_from_file(self) -> Dict[str, Any]:
        """Load configuration from file"""
        # Check for config file in common locations
        config_locations = [
            Path("config.yaml"),
            Path("config.yml"),
            Path("config.json"),
            Path("config") / "config.yaml",
            Path("config") / "config.json",
        ]
        
        for config_path in config_locations:
            if config_path.exists():
                with open(config_path) as f:
                    if config_path.suffix in ['.yaml', '.yml']:
                        return yaml.safe_load(f)
                    return json.load(f)
        
        return {}
    
    def _load_from_env(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        config = {}
        
        # File processor config
        if "MAX_FILE_SIZE" in os.environ:
            config.setdefault("file_processor", {})["max_file_size"] = int(os.environ["MAX_FILE_SIZE"])
        
        # PaLM config
        if "GOOGLE_API_KEY" in os.environ:
            google_config = {
                "api_key": os.environ["GOOGLE_API_KEY"],
                "model_name": os.environ.get("GOOGLE_MODEL_NAME", "gemini-1.5-flash")
            }
            config.setdefault("models", {})["google"] = google_config
        
        # Bedrock config
        if "AWS_ACCESS_KEY" in os.environ:
            bedrock_config = {
                "aws_access_key": os.environ["AWS_ACCESS_KEY"],
                "aws_secret_key": os.environ["AWS_SECRET_KEY"],
                "region": os.environ.get("AWS_REGION", "us-west-2"),
                "model_id": os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-v2")
            }
            config.setdefault("models", {})["bedrock"] = bedrock_config
        
        return config

@lru_cache()
def get_settings() -> AppConfig:
    """Get cached settings instance"""
    settings = Settings()
    return settings.load_config()
