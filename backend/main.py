"""
FastAPI Backend for ATS Resume Score Application
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ats import ATSScorer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ATS Resume Scorer API",
    description="API for analyzing resume ATS compatibility",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ATS scorer
ats_scorer = ATSScorer()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ATS Resume Scorer API",
        "version": "1.0.0",
        "endpoints": {
            "/analyze": "POST - Analyze resume against job description",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ATS Resume Scorer"}


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(..., description="Resume PDF file"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Analyze resume against job description
    
    Args:
        resume: PDF file of the resume
        job_description: Text of the job description
    
    Returns:
        JSON with ATS score and recommendations
    """
    try:
        logger.info(f"Received analyze request - Filename: {resume.filename}, Content-Type: {resume.content_type}")
        
        # Validate file type
        if not resume.filename.lower().endswith('.pdf'):
            logger.warning(f"Invalid file type: {resume.filename}")
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported. Please upload a PDF resume."
            )
        
        # Validate file size (max 10MB)
        resume_bytes = await resume.read()
        file_size_mb = len(resume_bytes) / (1024 * 1024)
        logger.info(f"File size: {file_size_mb:.2f} MB")
        
        if len(resume_bytes) > 10 * 1024 * 1024:  # 10MB
            logger.warning(f"File too large: {file_size_mb:.2f} MB")
            raise HTTPException(
                status_code=400,
                detail="File size too large. Maximum size is 10MB."
            )
        
        # Validate job description
        if not job_description or len(job_description.strip()) < 10:
            logger.warning(f"Job description too short: {len(job_description) if job_description else 0} characters")
            raise HTTPException(
                status_code=400,
                detail="Job description is too short. Please provide a detailed job description."
            )
        
        logger.info(f"Analyzing resume: {resume.filename}")
        
        # Analyze resume
        result = ats_scorer.analyze_resume(resume_bytes, job_description)
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Error analyzing resume")
            )
        
        logger.info(f"Analysis complete. Score: {result['overall_score']}")
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze_resume: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again."}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
