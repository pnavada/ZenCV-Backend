from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from pathlib import Path

class FileProcessorConfig(BaseModel):
    """Configuration for file processing"""
    max_file_size: int = Field(
        default=5 * 1024 * 1024,  # 5MB
        description="Maximum file size in bytes"
    )
    supported_formats: List[str] = Field(
        default=[".pdf"],
        description="List of supported file extensions"
    )
    temp_dir: Path = Field(
        default=Path("temp"),
        description="Directory for temporary files"
    )

class GoogleModelConfig(BaseModel):
    """Configuration for Google GenAI model"""
    api_key: str = Field(..., description="Google Cloud API key")
    model_name: str = Field(
        default="gemini-1.5-flash",
        description="Google GenAI model name"
    )

class BedrockModelConfig(BaseModel):
    """Configuration for AWS Bedrock model"""
    aws_access_key: str = Field(..., description="AWS access key")
    aws_secret_key: str = Field(..., description="AWS secret key")
    region: str = Field(
        default="us-west-2",
        description="AWS region"
    )
    model_id: str = Field(
        default="anthropic.claude-v2",
        description="Bedrock model ID"
    )

class ModelsConfig(BaseModel):
    """Configuration for AI models"""
    default_model: str = Field(
        default="google",
        description="Default model to use"
    )
    google: Optional[GoogleModelConfig] = None
    bedrock: Optional[BedrockModelConfig] = None

class AppConfig(BaseModel):
    """Main application configuration"""
    app_name: str = Field(
        default="Resume Customization API",
        description="Application name"
    )
    debug: bool = Field(
        default=False,
        description="Debug mode flag"
    )
    file_processor: FileProcessorConfig = Field(
        default=FileProcessorConfig(),
        description="File processor configuration"
    )
    models: ModelsConfig = Field(
        default=ModelsConfig(),
        description="AI models configuration"
    )
