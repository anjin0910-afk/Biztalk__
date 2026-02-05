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
if api_key and api_key != "your_groq_api_key_here":
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"Groq Init Error: {e}")

SYSTEM_PROMPTS = {
    "Upward": "당신은 비즈니스 커뮤니케이션 전문가입니다. 사용자의 메시지를 '상사'에게 보고하는 상황에 맞게 변환하세요. 정중한 격식체를 사용하고 결론부터 명확하게 제시하십시오.",
    "Lateral": "당신은 비즈니스 커뮤니케이션 전문가입니다. 사용자의 메시지를 '타팀 동료'에게 전달하는 상황에 맞게 변환하세요. 상호 존중하는 어투를 사용하고 업무 핵심을 명확히 하십시오.",
    "External": "당신은 비즈니스 커뮤니케이션 전문가입니다. 사용자의 메시지를 '고객'에게 안내하는 상황에 맞게 변환하세요. 극존칭을 사용하고 전문성과 서비스 마인드를 강조하십시오."
}

@app.route('/api/convert', methods=['GET', 'POST'])
@app.route('/convert', methods=['GET', 'POST'])
def convert_text():
    if request.method == 'GET':
        return jsonify({"status": "ok", "message": "BizTone API is running."}), 200

    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "변환할 텍스트가 없습니다."}), 400
    
    text = data.get('text')
    target = data.get('target', 'Upward')
    
    if target not in SYSTEM_PROMPTS:
        return jsonify({"error": "유효하지 않은 수신자 설정입니다."}), 400

    if not client:
        return jsonify({"error": "API 키가 설정되지 않았습니다."}), 500

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS[target]},
                {"role": "user", "content": f"다음 문장을 변환해줘: {text}"}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        converted_text = completion.choices[0].message.content.strip()
        return jsonify({"original": text, "target": target, "converted": converted_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    print(f"Feedback: {data}")
    return jsonify({"status": "success"}), 200

# Vercel에서는 app 객체를 직접 사용하므로 app.run()은 필요 없으나 로컬 테스트용으로 유지
if __name__ == '__main__':
    app.run(debug=True)
