from abc import ABC, abstractmethod
from typing import Dict, Optional
from pydantic import BaseModel
import json

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
        # Define the expected JSON structure separately for clarity
        json_structure = {
            "contact": {
                "name": "string",
                "email": "string",
                "phone": "string",
                "location": "string",
                "linkedin": "string [optional]"
            },
            "summary": "string [optional]",
            "experience": [
                {
                    "title": "string",
                    "company": "string",
                    "dates": "string",
                    "points": ["string"]
                }
            ],
            "education": [
                {
                    "degree": "string",
                    "school": "string",
                    "dates": "string",
                    "courses": ["string"] 
                }
            ],
            "skills": {
                "category_name": ["skill1", "skill2"]
            },
            "projects": [
                {
                    "name": "string",
                    "dates": "string",
                    "points": ["string"],
                    "technologies": ["string"]
                }
            ],
            "volunteering": [
                {
                    "organization": "string",
                    "role": "string",
                    "dates": "string",
                    "points": ["string"]
                }
            ],
            "honors": [
                {
                    "title": "string",
                    "issuer": "string",
                    "date": "string",
                    "description": "string"
                }
            ]
        }

        prompt_start = f"""You are an expert resume writer and ATS optimization specialist. Your task is to analyze the provided resume and job description, then customize the resume content to maximize relevance and impact.

            Resume text:
            {resume_text}

            Job Description:
            {job_description}

            Please create a customized version of this resume that:
            1. Begins with a compelling professional summary that:
               - Highlights your most relevant qualifications for this specific role
               - Demonstrates clear alignment between your experience and job requirements
               - Includes specific achievements that match key job responsibilities
               - Uses relevant keywords from the job description naturally
            2. Aligns the experience and skills with the job requirements
            3. Uses relevant keywords from the job description
            4. Quantifies achievements where possible
            5. Maintains professional tone and format

            Return a JSON object with the following structure. Include only relevant sections and ensure all content is DIRECTLY extracted or derived from the provided resume:
        """

        prompt_end = """
            Guidelines:
            1. The professional summary section is REQUIRED and must:
               - Be 3-4 sentences long
               - Focus on your strongest qualifications for this specific role
               - Include metrics and achievements when possible
               - Demonstrate clear understanding of the role's requirements
               - Use keywords from the job description naturally
            2. Skills should be grouped into logical categories based on the job requirements
            3. Include only courses that are relevant to the position
            4. Focus on achievements and responsibilities that match job requirements
            5. Use concrete numbers and metrics where available
            6. Maintain consistent date formatting throughout (e.g., "Jan 2020 - Present")
            7. Only include sections that have content and are relevant to the job
            8. Ensure all bullet points are clear, concise, and impactful
            9. Do not include any placeholder text like 'string' in the response, replace with actual content
            10. Format dates consistently as 'MMM YYYY - MMM YYYY' or 'MMM YYYY - Present'

            IMPORTANT: 
            - Ensure the response is valid JSON
            - Remove any sections that don't have content
            - Keep bullet points concise and achievement-focused
            - Use proper comma separation and JSON formatting
            - Do not include any comments or explanations outside the JSON structure
        """
        prompt = prompt_start + json.dumps(json_structure, indent=2) + prompt_end
        return prompt
