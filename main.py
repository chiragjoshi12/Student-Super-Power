import os
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process

if __name__ == "__main__":

    # Load the google gemini api key
    google_api_key = os.getenv("GOOGLE_API_KEY")

    # Set gemini pro as llm
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", verbose=True, temperature=0.9, google_api_key=google_api_key
    )

    # Create agents
    screenwriter = Agent(
        role="Screenwriter",
        goal="Translate ideas into engaging scenes with vivid descriptions, snappy dialogue, and emotional depth.",
        backstory="""Former freelance screenwriter for low-budget indie films. Learned to work quickly under constraints, 
                    generating multiple variations on a theme. Excels at building tension and incorporating plot twists.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    critic = Agent(
        role="Analytical Eye & Genre Enforcer",
        goal="Ensure stories are internally consistent, adhere to the intended genre, and maintain stylistic choices.",
        backstory="""A retired film studies professor with an encyclopedic knowledge of classic tropes, storytelling structures, 
                    and audience expectations. Has a knack for spotting potential plot holes and continuity errors.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    story_master = Agent(
        role="Project Lead & Master Orchestrator",
        goal="Guide the overall story generation process, manage the workflow between the Screenwriter and Critic, and ensure a cohesive final product.",
        backstory="""A seasoned novelist turned game narrative designer. Has a strong understanding of both high-level plot frameworks and the detailed 
                    scene creation required to immerse a reader in the world.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
    )

    # Get the story idea from the user
    user_input = input(
        "Please provide a short story idea. You can specify the genre and theme: "
    )

    # Create the task
    story_task = Task(
        description=f"Write a short story with the following user input: {user_input}",
        agent=story_master,
    )

    # Create the crew
    story_crew = Crew(
        agents=[screenwriter, critic, story_master],
        tasks=[story_task],
        verbose=True,
        process=Process.sequential,
    )

    # Execution Flow
    story_output = story_crew.kickoff()