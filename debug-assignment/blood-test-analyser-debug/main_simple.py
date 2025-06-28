from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import json

app = FastAPI(title="Blood Test Report Analyser - Simple Version")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running (Simple Version)"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if query == "" or query is None:
            query = "Summarise my Blood Test Report"
            
        # Simple analysis response (placeholder for CrewAI integration)
        analysis_response = {
            "status": "success",
            "query": query,
            "analysis": f"""
            Blood Test Analysis Report
            
            Query: {query}
            
            Medical Analysis:
            - Blood test report has been successfully uploaded and processed
            - File: {file.filename}
            - Analysis ID: {file_id}
            
            General Recommendations:
            - Consult with a healthcare professional for detailed interpretation
            - Review any abnormal values with your doctor
            - Follow up on any concerning results
            - Maintain regular check-ups
            
            Note: This is a simplified version. For full AI-powered analysis, 
            ensure all dependencies are properly installed.
            """,
            "file_processed": file.filename,
            "analysis_id": file_id
        }
        
        return analysis_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "features": [
            "PDF file upload",
            "Basic file validation",
            "Simple analysis response",
            "File cleanup"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_simple:app", host="0.0.0.0", port=8000, reload=True) 