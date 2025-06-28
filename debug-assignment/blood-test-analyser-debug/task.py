## Importing libraries and files
try:
    from crewai import Task  # type: ignore
except ImportError:
    print("Warning: crewai package not available. Please install it with: pip install crewai")
    # Create a mock Task class for development
    class Task:
        def __init__(self, **kwargs):
            self.description = kwargs.get('description', 'Mock Task')
            self.expected_output = kwargs.get('expected_output', 'Mock Output')
            self.agent = kwargs.get('agent', None)
            self.tools = kwargs.get('tools', [])
            self.async_execution = kwargs.get('async_execution', False)
            print(f"Mock Task created: {self.description[:50]}...")

try:
    from agents import doctor, verifier, nutritionist, exercise_specialist
except ImportError:
    print("Warning: agents module not available. Creating mock agents.")
    # Create mock agents
    class MockAgent:
        def __init__(self, name):
            self.name = name
    doctor = MockAgent("doctor")
    verifier = MockAgent("verifier")
    nutritionist = MockAgent("nutritionist")
    exercise_specialist = MockAgent("exercise_specialist")

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
            return self
    
    blood_test_tool = MockTool("blood_test")
    nutrition_tool = MockTool("nutrition")
    exercise_tool = MockTool("exercise")

## Creating a task to help solve user's query - Fixed to be professional
help_patients = Task(
    description="Analyze the blood test report and provide comprehensive medical insights for the user's query: {query}. "
    "Review the blood test data carefully, identify any abnormalities, and provide evidence-based recommendations. "
    "Focus on the specific concerns raised in the user's query while providing a complete health assessment.",

    expected_output="""Provide a comprehensive blood test analysis including:
- Summary of key findings and normal/abnormal values
- Interpretation of results in relation to the user's query
- Evidence-based medical recommendations
- Any concerning values that require follow-up
- General health insights and lifestyle recommendations
- Clear, professional language suitable for patient communication""",

    agent=doctor,
    tools=[blood_test_tool.read_data_tool],
    async_execution=False,
)

## Creating a nutrition analysis task - Fixed to be professional
nutrition_analysis = Task(
    description="Analyze the blood test results and provide evidence-based nutritional recommendations for: {query}. "
    "Focus on how specific blood markers relate to dietary needs and provide practical nutrition advice.",

    expected_output="""Provide detailed nutrition recommendations including:
- Analysis of blood markers relevant to nutrition (glucose, cholesterol, vitamins, etc.)
- Specific dietary recommendations based on test results
- Foods to include or avoid based on blood values
- Supplement recommendations if medically indicated
- Meal planning suggestions
- Evidence-based advice with scientific backing""",

    agent=nutritionist,
    tools=[blood_test_tool.read_data_tool, nutrition_tool.analyze_nutrition_tool],
    async_execution=False,
)

## Creating an exercise planning task - Fixed to be professional
exercise_planning = Task(
    description="Create a safe and effective exercise plan based on the blood test results for: {query}. "
    "Consider the individual's health status and design appropriate physical activity recommendations.",

    expected_output="""Create a comprehensive exercise plan including:
- Assessment of fitness level based on blood markers
- Safe exercise recommendations appropriate for health status
- Specific workout routines and intensity guidelines
- Frequency and duration recommendations
- Safety considerations and contraindications
- Progressive training approach
- Monitoring and adjustment guidelines""",

    agent=exercise_specialist,
    tools=[blood_test_tool.read_data_tool, exercise_tool.create_exercise_plan_tool],
    async_execution=False,
)

## Creating a verification task - Fixed to be professional
verification = Task(
    description="Verify that the uploaded document is a valid blood test report and contains the necessary information "
    "for medical analysis. Check for completeness and authenticity of the medical data.",

    expected_output="""Provide verification results including:
- Confirmation of document type (blood test report)
- Assessment of report completeness
- Identification of key blood markers present
- Validation of report format and structure
- Any missing or unclear information
- Overall assessment of report quality for analysis""",

    agent=verifier,
    tools=[blood_test_tool.read_data_tool],
    async_execution=False
)