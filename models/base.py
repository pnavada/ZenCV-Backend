from abc import ABC, abstractmethod
from typing import Dict, Optional
from pydantic import BaseModel

class ModelResponse(BaseModel):
    """Standardized model response"""
    customized_resume: str
    error: Optional[str] = None

class AIModelBase(ABC):
    """Base class for AI models"""
    
    @abstractmethod
    async def customize_resume(self, resume_text: str, job_description: str) -> ModelResponse:
        """
        Customize resume based on job description
        
        Args:
            resume_text (str): Original resume content
            job_description (str): Target job description
            
        Returns:
            ModelResponse: Standardized response with customized resume
        """
        pass

    def _create_prompt(self, resume_text: str, job_description: str) -> str:
        return f"""
        Task: Customize the provided resume for the specific job description.
        
        Resume:
        {resume_text}
        
        Job Description:
        {job_description}
        
        Instructions:
        1. Optimize the resume content for this specific job
        2. Keep all information truthful
        3. Match keywords and skills from the job description
        4. Maintain professional formatting
        5. Return only the customized resume text
        """
