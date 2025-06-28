from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

try:
    from crewai import Crew, Process  # type: ignore
except ImportError:
    print("Warning: crewai package not available. Please install it with: pip install crewai")
    # Create mock classes
    class Crew:
        def __init__(self, **kwargs):
            self.agents = kwargs.get('agents', [])
            self.tasks = kwargs.get('tasks', [])
            self.process = kwargs.get('process', 'sequential')
        def kickoff(self, inputs):
            return f"Mock crew analysis for: {inputs}"
    
    class Process:
        sequential = "sequential"

try:
    from agents import doctor, verifier, nutritionist, exercise_specialist
except ImportError:
    print("Warning: agents module not available. Creating mock agents.")
    class MockAgent:
        def __init__(self, name):
            self.name = name
    doctor = MockAgent("doctor")
    verifier = MockAgent("verifier")
    nutritionist = MockAgent("nutritionist")
    exercise_specialist = MockAgent("exercise_specialist")

try:
    from task import help_patients, nutrition_analysis, exercise_planning, verification
except ImportError:
    print("Warning: task module not available. Creating mock tasks.")
    class MockTask:
        def __init__(self, name):
            self.name = name
    help_patients = MockTask("help_patients")
    nutrition_analysis = MockTask("nutrition_analysis")
    exercise_planning = MockTask("exercise_planning")
    verification = MockTask("verification")

app = FastAPI(title="Blood Test Report Analyser")

def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew with all specialists"""
    medical_crew = Crew(
        agents=[verifier, doctor, nutritionist, exercise_specialist],
        tasks=[verification, help_patients, nutrition_analysis, exercise_planning],
        process=Process.sequential,
        verbose=True
    )
    
    result = medical_crew.kickoff({'query': query, 'file_path': file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

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
            
        # Process the blood report with all specialists
        response = run_crew(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)