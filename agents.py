from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os

# Load environment variables for API keys
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]="gpt-4-0125-preview"

# To Know Agent
to_know_agent = Agent(
    role="Student Information Collector",
    goal="Get the basic information about the student's background, interests and study habits.",
    backstory=(
        "You gather information about the student's preferences, background, interests, Favourite Subject."
    ),
    verbose=True
)

# To Know Task
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

def learning_tracker_agent(standard, subject, chapter):
    # Learning Score Tracker Agents
    learning_tracker_agent = Agent(
        role="Student's Learning Analyzer/Tracker",
        goal=f"Track the student's learning level/status in {chapter} chapter of {standard}th standard's {subject} subject. prepare the quizzes to assess their knowledge.",
        backstory=(
            f"Your primary role is to analyze the student's knowledge through tests in {chapter} Chapter."
            # "and track their progress in different subjects."
        ),
        verbose=True
    )

    # Learning Score Tracker Agents Task
    learning_tracker_task = Task(
        description=(
            f"Create a quiz on {chapter} chapter of {standard}th standard's {subject} subject to assess the student's understanding of a specific topic. "
            " Generate quiz in json format without using ```json."
            " Generate only questions, options (with options tag A., B.,..) and correct answer (define correct answer by just option's tag), nothing else."
        ),
        expected_output='Preapre Quiz for Check initial Learning Status of student understanding in Particular topic.',
        agent=learning_tracker_agent
    )
    
    crew = Crew(
        agents=[learning_tracker_agent],
        tasks=[learning_tracker_task],
        process=Process.sequential
    )

    result = crew.kickoff()
    return result