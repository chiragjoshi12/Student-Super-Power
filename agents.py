from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os

# Load environment variables for API keys
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]="gpt-4-0125-preview"

to_know_agent = Agent(
    role="Student Information Collector",
    goal="Get the basic information about the student's background, interests and study habits.",
    backstory=(
        "You gather information about the student's preferences, background, interests, Favourite Subject."
    ),
    verbose=True
)

# Task for To Know Agent
to_know_task = Task(
    description=(
        "Ask the questions to student for Collect information about the student's interests, like-dis like for study and study habits."
        " Questions should be in json format without using ```json."
        " Generate questions only, nothing anything else with that."
        " Mostly our students from 10 to 12 grade."
    ),
    expected_output='Student profile with subjects, hours of study, and learning preferences.',
    agent=to_know_agent
)
