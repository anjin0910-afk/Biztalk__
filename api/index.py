import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("GROQ_API_KEY")
client = None
if api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"Error: {e}")

SYSTEM_PROMPTS = {
    "Upward": "당신은 비즈니스 커뮤니케이션 전문가입니다. 사용자의 메시지를 '상사'에게 보고하는 상황에 맞게 변환하세요.",
    "Lateral": "당신은 비즈니스 커뮤니케이션 전문가입니다. 사용자의 메시지를 '타팀 동료'에게 전달하는 상황에 맞게 변환하세요.",
    "External": "당신은 비즈니스 커뮤니케이션 전문가입니다. 사용자의 메시지를 '고객'에게 안내하는 상황에 맞게 변환하세요."
}

@app.route('/api/convert', methods=['GET', 'POST'])
def convert_text():
    if request.method == 'GET':
        return jsonify({"status": "ok"}), 200
    
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data.get('text')
    target = data.get('target', 'Upward')
    
    if not client:
        return jsonify({"error": "API Key not configured"}), 500

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS.get(target, SYSTEM_PROMPTS["Upward"])},
                {"role": "user", "content": f"변환: {text}"}
            ]
        )
        return jsonify({"converted": completion.choices[0].message.content.strip()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def feedback():
    return jsonify({"status": "success"}), 200