## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

try:
    from crewai_tools import tools  # type: ignore
except ImportError:
    print("Warning: crewai_tools package not available. Please install it with: pip install crewai-tools")
    tools = None

try:
    from crewai_tools.tools.serper_dev_tool import SerperDevTool  # type: ignore
except ImportError:
    print("Warning: SerperDevTool not available. Creating mock search tool.")
    class SerperDevTool:
        def __call__(self, *args, **kwargs):
            return "Mock search results"

try:
    from langchain_community.document_loaders import PDFLoader  # type: ignore
except ImportError:
    print("Warning: PDFLoader not available. Creating mock PDF loader.")
    class PDFLoader:
        def __init__(self, file_path):
            self.file_path = file_path
        def load(self):
            return [MockDocument("Mock PDF content")]

class MockDocument:
    def __init__(self, content):
        self.page_content = content

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class BloodTestReportTool():
    async def read_data_tool(self, path='data/sample.pdf'):
        """Tool to read data from a pdf file from a path

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Blood Test report file
        """
        
        docs = PDFLoader(file_path=path).load()

        full_report = ""
        for data in docs:
            # Clean and format the report data
            content = data.page_content
            
            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
                
            full_report += content + "\n"
            
        return full_report

## Creating Nutrition Analysis Tool
class NutritionTool:
    async def analyze_nutrition_tool(self, blood_report_data):
        # Process and analyze the blood report data
        processed_data = blood_report_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement nutrition analysis logic here
        return "Nutrition analysis functionality to be implemented"

## Creating Exercise Planning Tool
class ExerciseTool:
    async def create_exercise_plan_tool(self, blood_report_data):        
        # TODO: Implement exercise planning logic here
        return "Exercise planning functionality to be implemented"

# Create instances of the tools
blood_test_tool = BloodTestReportTool()
nutrition_tool = NutritionTool()
exercise_tool = ExerciseTool()