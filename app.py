from flask import Flask, request, jsonify
from crewai import Crew, Process
from agents import to_know_task, to_know_agent
import json

app = Flask(__name__)

with open("chapters.json", 'r') as file:
    data = json.load(file)

@app.route('/get-subjects', methods=['POST'])
def get_chapters():
    language_id = request.json['language_id']
    standard_id = request.json['standard_id']
    subject_id = request.json['subject_id']
    
    # Find language
    language = next((lang for lang in data["languages"] if lang["name"] == language_id), None)
    if not language:
        return {"error":f"Language with ID {language_id} not found."}
    
    # Find standard
    standard = next((std for std in language["standards"] if std["id"] == standard_id), None)
    if not standard:
        return {"error":f"Standard with ID {standard_id} not found in language ID {language_id}."}
    
    # Find subject
    subject = next((sub for sub in standard["subjects"] if sub["name"] == subject_id), None)
    if not subject:
        return {"error":f"Subject with ID {subject_id} not found in standard ID {standard_id} of language ID {language_id}."}
    
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


if __name__ == '__main__':
    app.run(debug=True)
