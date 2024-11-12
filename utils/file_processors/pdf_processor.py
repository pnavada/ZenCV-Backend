from .base import FileProcessorBase
import PyPDF2
import io
from fastapi import HTTPException

class PDFProcessor(FileProcessorBase):
    """Processor for PDF files"""
    
    async def extract_text(self, content: bytes) -> str:
        try:
            # Create PDF reader object
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text_content = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text.strip():  # Only add non-empty pages
                    text_content.append(text.strip())
            
            final_text = "\n\n".join(text_content)
            
            if not final_text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Could not extract text from PDF. Please ensure the PDF contains readable text"
                )
                
            return final_text
            
        except PyPDF2.PdfReadError:
            raise HTTPException(
                status_code=400,
                detail="Invalid or corrupted PDF file"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing PDF: {str(e)}"
            )
