from flask import Flask, request, jsonify
from flask_cors import CORS
from crewai import Crew, Process
from agents import *
import google.generativeai as genai
import json

app = Flask(__name__)
CORS(app)

# CORS(app, resources={r"/*": {"origins": "http://localhost:5500"}})

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

with open("chapters.json", 'r') as file:
    data = json.load(file)

def call_gemini(system_instruction, prompt):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-002",
        generation_config=generation_config,
        system_instruction=system_instruction,
    )
    
    chat_session = model.start_chat(
        history=[
        ]
    )
    
    response = chat_session.send_message(prompt)
    return response.text

@app.route('/get-subjects', methods=['POST'])
def get_chapters():
    language_id = request.json['language_id']
    standard_id = request.json['standard_id']
    subject_id = request.json['subject_id']
    
    # Find language
    language = next((lang for lang in data["languages"] if lang["name"] == language_id), None)
    if not language:
        return {"error":f"{language_id} not found."}
    
    # Find standard
    standard = next((std for std in language["standards"] if std["id"] == standard_id), None)
    if not standard:
        return {"error":f"{standard_id} not found in {language_id} language."}
    
    # Find subject
    subject = next((sub for sub in standard["subjects"] if sub["name"] == subject_id), None)
    if not subject:
        return {"error":f"{subject_id} not found."}
    
    return subject["chapters"]

@app.route('/to-know-agent', methods=['GET'])
def call_toKnow_agent():
    crew = Crew(
        agents=[to_know_agent],
        tasks=[to_know_task],
        process=Process.sequential
    )

    result = crew.kickoff()
    return jsonify({"response": str(result)})

@app.route('/learning-score-tracker', methods=['POST'])
def call_learning_score_tracker_agent():
    standard = request.json['standard']
    subject = request.json['subject']
    chapter = request.json['chapter']
    
    response = learning_tracker_agent(standard, subject, chapter)
    return jsonify({"response": str(response)})

@app.route("/get-learning-score", methods=['POST'])
def get_learning_score():
    quiz = request.json['quiz']
    answer = request.json['answer']
    
    prompt_format = f"Quiz : {quiz} \n\n My Answer : {answer}"
    print(prompt_format)
    system_instruction="You are the Learning Status Tracker Expert. the coolest quiz master and expert quiz evaluator. Your mission is to gauge a student's understanding of specific Topic according Quiz Answer which has given by students.\n\nPrimary Objective:\nYour primary objective is to accurately assess the student's understanding of a specific topic or chapter. You need to determine the student's level of mastery, identify what they have understood, highlight areas they find challenging, and quantify their understanding with a Learning Score. Additionally, you will provide a comprehensive Learning Status summary for the evaluated topic/chapter. You need to provide 2 Things - 1. Learning Score and 2. Learning Summary\n\nKey Responsibilities:\n1. Analyze responses to gauge knowledge depth\n2. Calculate a Learning Score\n3. Provide a comprehensive Learning Score and Learning Summary\n\nLearning Score Calculation:\n- For multiple-choice questions: Mark as correct (1) or incorrect (0)\nLearning Score = (Total points earned / Total possible points) * 100\nRound the final score to the nearest whole number\n\nLearning Status Summary Components:\n1. Overall understanding level (Beginner, Intermediate, Advanced, Master)\n2. Key concepts grasped\n3. Areas of strength\n4. Concepts needing improvement\n5. Specific challenges identified\n6. Recommendations for further study\n\nFinal Reporting:\nAfter completing the assessment:\n1. Calculate and present the Learning Score\n2. Provide the detailed (not very much) Learning Status summary\n\nEvaluation Example:\nCorrect Answers: 3 out of 4\nLearning Score: 3/4 = 0.75 or 75%\nLearning Status Summary: \\\"The student has a strong foundational understanding of the topic, correctly identifying the chemical formula for water and explaining the polarity of water. They provided a clear explanation of photosynthesis but need to improve their understanding of chlorophyll's specific role. Overall, the student's mastery level is 75%, with a need to focus on the detailed processes within photosynthesis.\\\" ⁠"
    
    learning_score = call_gemini(system_instruction, prompt_format)
    
    return learning_score

@app.route("/generate-roadmap", methods=['POST'])
def generate_roadmap():
    learning_score = request.json['learning_score']
    student_info = request.json['student_info']

    response = roadmap_generator_agent(learning_score, student_info)

    return jsonify({"response":str(response)})

@app.route("/coach-agent", methods=['POST'])
def coach_agent():
    query = request.json['prompt']
    system_instruction = "Your Role: You are the World's best Teacher with a deep understanding of how to explain any question to students in an easy, simple, and engaging manner. Your goal is to provide interactive, fun, and highly informative response that make students understand the topic better and inspire curiosity. You are a very disciplined teacher who always follows instructions strictly.\n\nStrict Instructions for you:\n- Be specific and concise; do not prolong the explanation unnecessarily.\n- Sometimes use emojis but don't overuse them.\n- Make sure explanations are detailed and comprehensive according to the specified length.\n- Talk as if you are explaining to a younger student. Do not use too much professional language.\n- Bold important points."
    
    response = call_gemini(system_instruction, query)
    return jsonify({"response":response})

if __name__ == '__main__':
    app.run(debug=True)
