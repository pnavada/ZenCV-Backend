from typing import Dict, Type
from .base import FileProcessorBase
from .pdf_processor import PDFProcessor
from fastapi import HTTPException
from pathlib import Path

class FileProcessorFactory:
    """Factory class for creating file processors"""
    
    _processors: Dict[str, Type[FileProcessorBase]] = {
        '.pdf': PDFProcessor
        # Add more processors here as they're implemented:
        # '.docx': DocxProcessor,
        # '.txt': TextProcessor,
        # etc.
    }
    
    @classmethod
    def get_processor(cls, filename: str) -> FileProcessorBase:
        """Get appropriate processor for file type"""
        ext = Path(filename).suffix.lower()
        
        if ext not in cls._processors:
            supported = ", ".join(cls._processors.keys())
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Currently supported formats: {supported}"
            )
            
        return cls._processors[ext]()
    
    @classmethod
    def register_processor(cls, extension: str, processor: Type[FileProcessorBase]):
        """Register a new file processor"""
        cls._processors[extension.lower()] = processor
