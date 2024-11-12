from abc import ABC, abstractmethod
from fastapi import HTTPException

class FileProcessorBase(ABC):
    """Base class for file processors"""
    
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    def __init__(self, max_file_size: int = None):
        if max_file_size is not None:
            self.MAX_FILE_SIZE = max_file_size
    
    @abstractmethod
    async def extract_text(self, content: bytes) -> str:
        """Extract text from file content"""
        pass
    
    async def validate_size(self, content: bytes) -> None:
        if len(content) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum limit of {self.MAX_FILE_SIZE // 1024 // 1024}MB"
            )
