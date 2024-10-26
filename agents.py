from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os

# Load environment variables for API keys
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]="gpt-4"

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
        " Generate only 5 questions. "
        """
        Questions should be only text formmat.
        It's format should be like:
        {
        "response": [
            {"question": <questions>},
            ....
        ]
        }
        """
    ),
    expected_output='Student profile with subjects, hours of study, and learning preferences.',
    agent=to_know_agent
)

# Learning Tracker Agent
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
            " Generate quiz in json format without using ```json or ```. "
            " ```json or ``` is bad sign. "
            " Generate only questions, options (with options tag A., B.,..) and correct answer (define correct answer by just option's tag), nothing else. "
            " Questions Must be in English. "
            """Questions Must be in below format:
            {   
                {
                    \"Question\": \"Questions...\",
                    \"Options\": {
                        \"A.\": \"Option A\",
                        \"B.\": \"Option B\",
                        \"C.\": \"Option C\",
                        \"D.\": \"Option D\"
                    },
                }
            }
            """
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

# Roadmap Generator Agent
def roadmap_generator_agent(learning_score, student_details):
    roadmap_agent = Agent(
        role="Personalized Roadmap Creator",
        goal=f"Create a personalized learning roadmap based on the student's Learning Score: {learning_score} and Student's basic Details : {student_details}.",
        backstory=(
            "With your expertise, you craft tailored learning paths for student according them learning score, "
            "ensuring they learn efficiently. "
            "Learning score is a Showing the Initial level of Understanding in any topic or chapter. "
            "Add link of related course, video, article or something else as resources if required."
        ),
        verbose=True
    )
    
    roadmap_task = Task(
        description=(
            "Create a personalized learning roadmap for the student based on their Learning Score: {learning_score} and Student's basic Details : {student_details} \n for ipmprove them understanding. "
            "Your final output should be a step-by-step roadmap for the student to follow. "
            "Learning score is a Showing the Initial level of Understanding in any topic or chapter"
        ),
        expected_output='A personalized learning roadmap outlining next steps for the student according them Learning Score.',
        agent=roadmap_agent
    )
    
    crew = Crew(
        agents=[roadmap_agent],
        tasks=[roadmap_task],
        process=Process.sequential
    )

    result = crew.kickoff()
    return result

