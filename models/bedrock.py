# models/bedrock_model.py
import boto3
import json
import asyncio
from .base import AIModelBase, ModelResponse

class BedrockModel(AIModelBase):
    def __init__(
        self, 
        aws_access_key: str, 
        aws_secret_key: str,
        region: str = "us-west-2",
        model_id: str = "anthropic.claude-v2"
    ):
        self.client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        self.model_id = model_id

    async def customize_resume(self, resume_text: str, job_description: str) -> ModelResponse:
        prompt = self._create_prompt(resume_text, job_description)
        
        try:
            response = await asyncio.to_thread(
                self.client.invoke_model,
                modelId=self.model_id,
                body=json.dumps({
                    "prompt": prompt,
                })
            )
            
            return ModelResponse(
                customized_resume=json.loads(response['body'].read())['completion']
            )
            
        except Exception as e:
            return ModelResponse(
                customized_resume="",
                error=f"Bedrock API error: {str(e)}"
            )
