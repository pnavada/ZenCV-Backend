import asyncio
from .base import AIModelBase, ModelResponse
import google.generativeai as genai

class GoogleModel(AIModelBase):
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model_name)
        self.model_name = model_name

    async def customize_resume(self, resume_text: str, job_description: str) -> ModelResponse:
        prompt = self._create_prompt(resume_text, job_description)
        
        try:
            response = await asyncio.to_thread(
                self.client.generate_content,
                prompt, 
                resume_text)
            
            return ModelResponse(
                customized_resume=response.text
            )
            
        except Exception as e:
            return ModelResponse(
                customized_resume="",
                error=f"Google API error: {str(e)}"
            )
