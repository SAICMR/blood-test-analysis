# Blood Test Report Analyser - CrewAI Application

A professional medical application that uses CrewAI to analyze blood test reports and provide comprehensive health insights, nutrition recommendations, and exercise plans.

## 🐛 Bug Fixes Applied

### **Critical Bugs Fixed:**

1. **LLM Configuration Bug** - Fixed circular reference `llm = llm` in `agents.py`
2. **Missing PDFLoader Import** - Added proper import for PDF processing
3. **Async/Sync Method Mismatch** - Fixed tool method definitions
4. **Missing Dependencies** - Added required packages to requirements.txt
5. **Crew Configuration** - Fixed to include all agents and tasks properly
6. **Professional Agent Roles** - Replaced unprofessional agent descriptions with proper medical roles

### **Additional Improvements:**
- Added proper error handling throughout the application
- Improved file validation and security
- Enhanced tool implementations with actual functionality
- Professional medical language and evidence-based recommendations

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- API keys for either OpenAI or Google Gemini (optional, will use fallback if not provided)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd blood-test-analyser-debug
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables (optional):**
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### Running the Application

1. **Start the FastAPI server:**
```bash
python main.py
```

2. **Access the API:**
- Health check: `http://localhost:8000/`
- API documentation: `http://localhost:8000/docs`

### Using the API

**Endpoint:** `POST /analyze`

**Parameters:**
- `file`: PDF blood test report file
- `query`: Your specific question about the blood test (optional, defaults to "Summarise my Blood Test Report")

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_blood_test.pdf" \
  -F "query=What do my cholesterol levels mean?"
```

## 🏥 Application Features

### **Multi-Specialist Analysis:**
1. **Medical Doctor** - Comprehensive blood test interpretation
2. **Verification Specialist** - Document validation and completeness check
3. **Clinical Nutritionist** - Evidence-based dietary recommendations
4. **Exercise Physiologist** - Safe and personalized exercise plans

### **Professional Medical Analysis:**
- Evidence-based recommendations
- Clear interpretation of blood markers
- Safety-focused exercise guidance
- Scientific nutrition advice
- Professional medical language

## 🔧 Technical Architecture

- **Framework:** FastAPI for REST API
- **AI Framework:** CrewAI for multi-agent orchestration
- **LLM:** OpenAI GPT-3.5-turbo or Google Gemini Pro
- **Document Processing:** LangChain PDFLoader
- **File Handling:** Secure PDF upload and processing

## 📁 Project Structure

```
blood-test-analyser-debug/
├── main.py              # FastAPI application entry point
├── agents.py            # CrewAI agent definitions
├── tools.py             # Custom tools for PDF processing and analysis
├── task.py              # Task definitions for each agent
├── requirements.txt     # Python dependencies
├── data/               # Sample PDF files and uploads
└── outputs/            # Generated analysis outputs
```

## 🛡️ Security Features

- File type validation (PDF only)
- Secure file handling with cleanup
- Input validation and sanitization
- Error handling with appropriate HTTP status codes

## 📝 Notes

- The application requires PDF blood test reports for analysis
- API keys are optional but recommended for better performance
- All medical advice is for informational purposes only
- Always consult healthcare professionals for medical decisions

## 🐛 Debugging Guide

If you encounter issues:

1. **Check API keys** - Ensure your environment variables are set correctly
2. **Verify PDF format** - Ensure uploaded files are valid PDF blood test reports
3. **Check logs** - Review console output for detailed error messages
4. **Test with sample data** - Use the provided sample PDF files for testing

## 🤝 Contributing

When contributing to this project:
1. Follow professional medical standards
2. Ensure all recommendations are evidence-based
3. Maintain security best practices
4. Add proper error handling
5. Update documentation as needed
