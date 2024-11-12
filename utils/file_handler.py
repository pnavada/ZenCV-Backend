from fastapi import UploadFile, HTTPException
from .file_processors.factory import FileProcessorFactory

class FileHandler:
    """Main file handling class"""
    
    @staticmethod
    async def extract_text(file: UploadFile) -> str:
        """
        Extract text from uploaded file
        
        Args:
            file (UploadFile): The uploaded file
            
        Returns:
            str: Extracted text content
            
        Raises:
            HTTPException: For invalid files or processing errors
        """
        try:
            # Get appropriate processor
            processor = FileProcessorFactory.get_processor(file.filename)
            
            # Read file content
            content = await file.read()
            
            # Validate file size
            await processor.validate_size(content)
            
            # Extract text
            text = await processor.extract_text(content)
            
            return text
            
        except HTTPException as http_err:
            raise http_err
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file: {str(e)}"
            )
        finally:
            await file.seek(0)  # Reset file pointer
