import streamlit as st
import requests
import json

# API endpoints
API_URL = "http://127.0.0.1:5000/get-subjects"
TO_KNOW_AGENT_API_URL = "http://127.0.0.1:5000/to-know-agent"
LEARNING_SCORE_TRACKER_API_URL = "http://127.0.0.1:5000/learning-score-tracker"
GET_LEARNING_SCORE_API_URL = "http://127.0.0.1:5000/get-learning-score"
GENERATE_ROADMAP_API_URL = "http://127.0.0.1:5000/generate-roadmap"

# Function to display the login-like interface
def login_page():
    st.title("Learning Platform")
    st.header("Choose your preferences to start learning")

    # Question 1: Language
    language = st.selectbox("What's your Language?", ["Gujarati", "English"])

    # Question 2: Standard
    standard = st.selectbox("What's Your Standard?", ["10", "11", "12"])

    # Question 3: Subject (dynamic based on standard)
    if standard == "10":
        subject = st.selectbox("Which subject do you want to learn?", ["Maths", "Science", "Social Science"])
    else:
        subject = st.selectbox("Which subject do you want to learn?", ["Biology", "Physics", "Chemistry", "Maths"])

    # Button to submit the answers
    if st.button("Next Chapter"):
        # Store user inputs in session state
        st.session_state.language = language
        st.session_state.standard = standard
        st.session_state.subject = subject
        st.session_state.page = "chapters"  # Navigate to chapters page

# Function to display chapters
def chapters_page():
    st.title("Chapters Available")

    # Call the API with the selected values
    response = requests.post(
        API_URL,
        json={
            "language_id": st.session_state.language,
            "standard_id": int(st.session_state.standard),
            "subject_id": st.session_state.subject
        }
    )

    # Parse the response
    if response.status_code == 200:
        chapters = response.json()
        st.subheader("Chapters:")

        # Create buttons for each chapter
        for chapter in chapters:
            chapter_name = chapter.get('name')
            if st.button(chapter_name):
                st.session_state.selected_chapter = chapter_name
                # Check if student_info exists in session state
                if 'student_info' in st.session_state:
                    st.session_state.page = "chapter_info"  # Navigate to chapter_info
                else:
                    st.session_state.page = "to_know_agent"  # Navigate to to_know_agent
    else:
        st.error("Could not retrieve chapters. Please check your selection.")

# Function to display chapter information
def chapter_info_page():
    st.title(f"Chapter: {st.session_state.selected_chapter}")

    st.subheader("Chapter Content")
    st.write("Displaying chapter information...")  # Placeholder for chapter content

    # Initialize session state variables if they don't exist
    if 'questions' not in st.session_state:
        st.session_state.questions = None
    if 'learning_score_response' not in st.session_state:
        st.session_state.learning_score_response = None
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = ""
    if 'show_coach_input' not in st.session_state:  # New variable to track input visibility
        st.session_state.show_coach_input = False

    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Button for Learning Score Tracker
        if st.button("Learning Score Tracker"):
            data = {
                "standard": st.session_state.standard,
                "subject": st.session_state.subject,
                "chapter": st.session_state.selected_chapter
            }
            response = requests.post(LEARNING_SCORE_TRACKER_API_URL, json=data)

            if response.status_code == 200:
                st.success("Learning score tracker updated successfully.")
                response_data = response.json()
                st.session_state.questions = response_data.get("response", [])
                
                # Display the quiz question
                if st.session_state.questions:
                    st.markdown("### Quiz Question")
                    st.write(response_data)
            else:
                st.error(f"Failed to update learning score tracker. Status code: {response.status_code}")
                st.write("Response:", response.text)

        # Only show answer input if we have questions
        if st.session_state.questions:
            st.session_state.user_answer = st.text_input(
                "Your answer:",
                key="answer_input",
                value=st.session_state.user_answer
            )
            
            if st.button("Submit Answer"):
                if st.session_state.user_answer:
                    # Prepare data for the GET Learning Score API call
                    payload = {
                        "quiz": st.session_state.questions,
                        "answer": st.session_state.user_answer
                    }
                    
                    try:
                        learning_score_response = requests.post(
                            GET_LEARNING_SCORE_API_URL,
                            json=payload
                        )
                        
                        st.write(learning_score_response.text)  # Print the raw response text
                        
                        if learning_score_response.status_code == 200:
                            st.session_state.learning_score_response = learning_score_response.json()
                            st.success("Answer submitted successfully!")
                        else:
                            st.error(f"Error getting learning score. Status code: {learning_score_response.status_code}")
                            st.write("Error response:", learning_score_response.text)
                    except json.JSONDecodeError:
                        st.error("Failed to decode JSON response. The response may not be in valid JSON format.")
                        st.write("Response Text:", learning_score_response.text)  # Print the raw response text
                    except requests.exceptions.RequestException as e:
                        st.error(f"API call failed: {str(e)}")
                else:
                    st.warning("Please enter an answer before submitting.")

        # New button for Roadmap Generator
        if st.button("Roadmap Generator"):
            # Prepare data for the Roadmap Generator API call
            roadmap_data = {
                "learning_score": st.session_state.learning_score_response,
                "student_info": st.session_state.get('student_info', {})
            }
            
            try:
                roadmap_response = requests.post(GENERATE_ROADMAP_API_URL, json=roadmap_data)
                
                if roadmap_response.status_code == 200:
                    st.success("Roadmap generated successfully!")
                    # Display the generated roadmap in Markdown format
                    roadmap_content = roadmap_response.text  # Assuming this is a Markdown formatted string
                    st.markdown(roadmap_content)  # Directly render the Markdown content
                else:
                    st.error(f"Error generating roadmap. Status code: {roadmap_response.status_code}")
                    st.write("Error response:", roadmap_response.text)
            except requests.exceptions.RequestException as e:
                st.error(f"API call failed: {str(e)}")

        # Button to show the Coach Agent input box
        if st.button("Coach Agent"):
            st.session_state.show_coach_input = True  # Set flag to show input

        # Input box for Coach Agent appears if the button was clicked
        if st.session_state.show_coach_input:
            prompt_input = st.text_input("Enter your prompt for the Coach Agent:")
            if st.button("Send to Coach Agent"):
                if prompt_input:
                    payload = {"prompt": prompt_input}
                    try:
                        coach_response = requests.post("http://127.0.0.1:5000/coach-agent", json=payload)
                        if coach_response.status_code == 200:
                            st.success("Prompt sent to Coach Agent successfully!")
                            response_data = coach_response.json() 
                            response_text = response_data.get("response", "")
                            response_text = response_text.replace("\\n", "\n")  
                            st.markdown("### Coach Agent Response")
                            # st.markdown(coach_response.text)
                            st.markdown(response_text)
                        else:
                            st.error(f"Error communicating with Coach Agent. Status code: {coach_response.status_code}")
                            st.write("Error response:", coach_response.text)
                    except requests.exceptions.RequestException as e:
                        st.error(f"API call failed: {str(e)}")
                else:
                    st.warning("Please enter a prompt before sending.")

    with col2:
        # Display the learning score response in the sidebar
        if st.session_state.learning_score_response:
            st.markdown("### Learning Score Results")
            
            # Handle different response formats
            if isinstance(st.session_state.learning_score_response, dict):
                for key, value in st.session_state.learning_score_response.items():
                    st.markdown(f"**{key}:** {value}")
            elif isinstance(st.session_state.learning_score_response, str):
                st.write(st.session_state.learning_score_response)
            else:
                st.json(st.session_state.learning_score_response)

    # Add a button to go back to chapters
    if st.button("Back to Chapters", key="back_to_chapters"):
        st.session_state.page = "chapters"

# Function to handle the questionnaire
def to_know_agent_page():
    st.title("Fetching Knowledge...")

    # Call the /to-know-agent API
    response = requests.get(TO_KNOW_AGENT_API_URL)

    if response.status_code == 200:
        data = response.json()

        if 'response' in data:
            inner_data = json.loads(data['response'])

            if 'response' in inner_data:
                questions = inner_data['response']

                if isinstance(questions, list):
                    # Only display questions if student_info is not set
                    if 'student_info' not in st.session_state:
                        st.subheader("Please answer the following questions:")

                        with st.form(key='quiz_form'):
                            answers = {}

                            for question in questions:
                                if isinstance(question, dict) and 'question' in question:
                                    q_text = question['question']
                                    answer = st.text_input(q_text, key=q_text)
                                    answers[q_text] = answer

                            submit_button = st.form_submit_button(label='Submit')

                            if submit_button:
                                st.session_state.student_info = answers  # Store responses
                                st.success("Your responses have been saved.")
                                st.session_state.page = "chapter_info"  # Navigate to chapter_info
                    else:
                        st.success("Your responses have already been submitted. Proceeding to Chapter Information.")
                        st.session_state.page = "chapter_info"
                else:
                    st.error("Unexpected response format: expected a list of questions.")
            else:
                st.error("Inner response does not contain questions.")
        else:
            st.error("Response does not contain inner response.")
    else:
        st.error("Could not fetch data from the agent. Please try again later.")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "login"  # Default to login page

# Main navigation logic
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "chapters":
    chapters_page()
elif st.session_state.page == "to_know_agent":
    to_know_agent_page()
elif st.session_state.page == "chapter_info":
    chapter_info_page()
