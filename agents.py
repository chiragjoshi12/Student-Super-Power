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
        " Questions should be in json format."
        " Generate questions only, nothing anything else with that."
        " Mostly our students from 10 to 12 grade."
        # "Ask the student the following questions if information is incomplete:"
        # "\n1. What subjects are you most interested in?"
        # "\n2. How many hours do you study per week?"
        # "\n3. Do you prefer reading, watching videos, or hands-on practice?"
        # "\n4. What challenges do you face in learning?"
    ),
    expected_output='Student profile with subjects, hours of study, and learning preferences.',
    agent=to_know_agent
)

crew = Crew(
    agents=[to_know_agent],
    tasks=[to_know_task],
    process=Process.sequential
)

# Kicking off the crew for a specific task
output = crew.kickoff()
# print(output)