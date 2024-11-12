# main.py
from fastapi import FastAPI, UploadFile, File, Body, HTTPException, Depends, Form
from starlette.background import BackgroundTask
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from models.model_factory import ModelFactory
from utils.file_handler import FileHandler
from config.settings import get_settings, AppConfig
import tempfile
import os
from typing import Dict
from pydantic import BaseModel

app = FastAPI(title="Resume Customization API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model factory with configuration
model_factory = ModelFactory()

class CustomizeRequest(BaseModel):
    """Request body validation model"""
    job_description: str
    model_name: str = None

@app.post("/api/customize-resume")
async def customize_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
    model_name: str = Form(None),
    config: AppConfig = Depends(get_settings)
) -> FileResponse:
    """
    Customize resume based on job description.
    
    Args:
        resume_file: Resume file (currently supports PDF)
        data: JSON containing job description and optional model name
        config: Application configuration settings
        
    Returns:
        FileResponse: Customized resume as a text file
        
    Raises:
        HTTPException: For various error conditions
    """

    data = {
        "job_description": job_description,
        "model_name": model_name
    }
        
    # Validate request data
    if 'job_description' not in data:
        raise HTTPException(
            status_code=400,
            detail="job_description is required in request body"
        )

    print(data)

    # Create temporary file for output
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix='.txt',
        mode='w',
        encoding='utf-8'
    )
    
    try:
        # Extract text from file
        resume_text = await FileHandler.extract_text(
            resume_file
        )
        
        # Get model
        model_name = data.get('model_name', config.models.default_model)
        model = await model_factory.get_model(model_name)
        
        # Process resume
        result = await model.customize_resume(
            resume_text=resume_text,
            job_description=data['job_description']
        )
        
        if result.error:
            raise HTTPException(
                status_code=500,
                detail=result.error
            )

        # Write result to temporary file
        temp_file.write(result.customized_resume)
        temp_file.close()  # Close file to ensure all content is written
        
        # Create background task to cleanup temp file
        cleanup_task = BackgroundTask(lambda: os.unlink(temp_file.name))
        
        # Return file response
        return FileResponse(
            path=temp_file.name,
            filename="customized_resume.txt",
            media_type="text/plain",
            background=cleanup_task
        )
        
    except HTTPException as http_err:
        # Clean up temp file if exists
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
        raise http_err
        
    except Exception as e:
        # Clean up temp file if exists
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@app.get("/api/models")
async def list_models(
    config: AppConfig = Depends(get_settings)
) -> Dict:
    """
    Get list of available AI models
    
    Returns:
        Dict: Dictionary containing list of available models
    """
    try:
        return {
            "status": "success",
            "models": model_factory.list_available_models()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving models: {str(e)}"
        )

# Health check endpoint
@app.get("/api/health")
async def health_check() -> Dict:
    """
    API health check endpoint
    
    Returns:
        Dict: Health status
    """
    return {
        "status": "healthy",
        "version": "1.0.0"
    }
