## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

# Try to import required packages with fallbacks
try:
    from crewai.agents import Agent  # type: ignore
except ImportError:
    print("Warning: crewai package not available. Please install it with: pip install crewai")
    # Create a mock Agent class for development
    class Agent:
        def __init__(self, **kwargs):
            self.role = kwargs.get('role', 'Mock Agent')
            self.goal = kwargs.get('goal', 'Mock Goal')
            self.tools = kwargs.get('tools', [])
            self.llm = kwargs.get('llm', None)
            print(f"Mock Agent created: {self.role}")

try:
    from langchain_openai import ChatOpenAI  # type: ignore
except ImportError:
    print("Warning: langchain_openai package not available. Please install it with: pip install langchain-openai")
    ChatOpenAI = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
except ImportError:
    print("Warning: langchain_google_genai package not available. Please install it with: pip install langchain-google-genai")
    ChatGoogleGenerativeAI = None

try:
    from tools import blood_test_tool, nutrition_tool, exercise_tool
except ImportError:
    print("Warning: tools module not available. Creating mock tools.")
    # Create mock tools
    class MockTool:
        def __init__(self, name):
            self.name = name
        def __call__(self, *args, **kwargs):
            return f"Mock {self.name} tool called"
        def __getattr__(self, name):
            # Handle any attribute access (like read_data_tool)
            return self
    
    blood_test_tool = MockTool("blood_test")
    nutrition_tool = MockTool("nutrition")
    exercise_tool = MockTool("exercise")

### Loading LLM - Fixed the circular reference bug
# Try OpenAI first, fallback to Google if not available
llm = None
if ChatOpenAI:
    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    except Exception as e:
        print(f"Error initializing OpenAI: {e}")
        llm = None

if not llm and ChatGoogleGenerativeAI:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    except Exception as e:
        print(f"Error initializing Google AI: {e}")
        llm = None

if not llm:
    print("Warning: No LLM available. Using mock LLM.")
    class MockLLM:
        def __call__(self, *args, **kwargs):
            return "Mock LLM response"
    llm = MockLLM()

# Creating an Experienced Doctor agent - Fixed to be professional
doctor = Agent(
    role="Senior Medical Doctor and Blood Test Analyst",
    goal="Analyze blood test reports accurately and provide evidence-based medical insights for: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a board-certified physician with over 15 years of experience in internal medicine "
        "and laboratory medicine. You specialize in interpreting blood test results and providing "
        "comprehensive health assessments. You always base your recommendations on scientific evidence "
        "and current medical guidelines. You communicate clearly and compassionately with patients, "
        "explaining complex medical concepts in understandable terms."
    ),
    tools=[blood_test_tool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=True
)

# Creating a verifier agent - Fixed to be professional
verifier = Agent(
    role="Medical Report Verification Specialist",
    goal="Verify the authenticity and completeness of medical reports, ensuring they contain valid blood test data",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified medical technologist with expertise in laboratory procedures and "
        "medical documentation. You have extensive experience in validating medical reports and "
        "ensuring they meet clinical standards. You are thorough and detail-oriented, always "
        "verifying that reports contain the necessary information for proper medical interpretation."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=5,
    allow_delegation=True
)

# Creating a nutritionist agent - Fixed to be professional
nutritionist = Agent(
    role="Clinical Nutritionist",
    goal="Provide evidence-based nutritional recommendations based on blood test results for: {query}",
    verbose=True,
    backstory=(
        "You are a registered dietitian with a master's degree in clinical nutrition and over "
        "10 years of experience working with patients with various health conditions. You specialize "
        "in translating blood test results into practical dietary recommendations. You always base "
        "your advice on scientific research and individual patient needs, avoiding fad diets and "
        "unproven supplements."
    ),
    llm=llm,
    max_iter=3,
    max_rpm=8,
    allow_delegation=False
)

# Creating an exercise specialist agent - Fixed to be professional
exercise_specialist = Agent(
    role="Exercise Physiologist and Fitness Specialist",
    goal="Design safe and effective exercise programs based on blood test results and health status for: {query}",
    verbose=True,
    backstory=(
        "You are a certified exercise physiologist with a degree in kinesiology and specialized "
        "training in medical exercise therapy. You have worked with patients of all ages and fitness "
        "levels, including those with chronic health conditions. You design personalized exercise "
        "programs that are safe, effective, and appropriate for each individual's health status "
        "and fitness goals."
    ),
    llm=llm,
    max_iter=3,
    max_rpm=8,
    allow_delegation=False
)
