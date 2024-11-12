from typing import Dict, Optional, Type
from .base import AIModelBase
from .bedrock import BedrockModel
from .google import GoogleModel
import os
from fastapi import HTTPException

class ModelFactory:
    """Factory for creating and managing AI models"""
    
    _instance = None
    _models: Dict[str, AIModelBase] = {}
    _config: Dict[str, Dict] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelFactory, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._models:
            self._initialize_models()
    
    def _initialize_models(self):
        """Initialize available models based on environment configuration"""
        # Initialize Google if credentials available
        if all(key in os.environ for key in ['GOOGLE_API_KEY']):
            self._models['google'] = GoogleModel(
                api_key=os.environ['GOOGLE_API_KEY'],
            )
            
        # Initialize Bedrock if credentials available
        if all(key in os.environ for key in ['AWS_ACCESS_KEY', 'AWS_SECRET_KEY']):
            self._models['bedrock'] = BedrockModel(
                aws_access_key=os.environ['AWS_ACCESS_KEY'],
                aws_secret_key=os.environ['AWS_SECRET_KEY']
            )
    
    async def get_model(self, model_name: Optional[str] = None) -> AIModelBase:
        """
        Get specified or default AI model
        
        Args:
            model_name: Optional name of specific model to use
            
        Returns:
            AIModelBase: Instance of AI model
            
        Raises:
            HTTPException: If model not available
        """
        # Return specified model if available
        if model_name:
            if model_name not in self._models:
                raise HTTPException(
                    status_code=400,
                    detail=f"Model '{model_name}' not available. Available models: {', '.join(self._models.keys())}"
                )
            
            model = self._models[model_name]
            return model
        
        # Try models in order of preference
        for name in ['google', 'bedrock']:
            if name in self._models:
                model = self._models[name]
                return model
        
        raise HTTPException(
            status_code=503,
            detail="No AI models are currently available"
        )
    
    def register_model(self, name: str, model: AIModelBase):
        """Register a new model"""
        self._models[name] = model
    
    def list_available_models(self) -> list:
        """Get list of available model names"""
        return list(self._models.keys())
