import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# 프론트엔드 폴더 경로 설정 (backend 폴더의 부모 폴더 내 frontend 폴더)
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

app = Flask(__name__, static_folder=frontend_dir)
CORS(app, resources={r"/*": {"origins": "*"}})

api_key = os.getenv("GROQ_API_KEY")
client = None
if api_key and api_key != "your_groq_api_key_here":
    try:
        client = Groq(api_key=api_key)
        print("--- Groq Client Ready ---")
    except Exception as e:
        print(f"Error: {e}")

# 시스템 프롬프트 정의
SYSTEM_PROMPTS = {
    "Upward": (
        "당신은 비즈니스 커뮤니케이션 전문가입니다. 사용자의 메시지를 '상사'에게 보고하는 상황에 맞게 변환하세요.\n"
        "1. 정중한 격식체(-하십시오, -합니까)를 사용하십시오.\n"
        "2. 결론부터 명확하게 제시하는 두괄식 보고 형식을 따르십시오.\n"
        "3. 불필요한 수식어는 줄이고 전문적이고 신뢰감 있는 어조를 유지하십시오."
    ),
    "Lateral": (
        "당신은 비즈니스 커뮤니케이션 전문가입니다. 사용자의 메시지를 '타팀 동료'에게 전달하는 상황에 맞게 변환하세요.\n"
        "1. 친절하고 상호 존중하는 어투(-해요, -합니다)를 사용하십시오.\n"
        "2. 협업을 위한 요청 사항과 마감 기한을 명확하게 전달하십시오.\n"
        "3. 부드러우면서도 업무의 핵심이 잘 드러나는 협조 요청 형식을 따르십시오."
    ),
    "External": (
        "당신은 비즈니스 커뮤니케이션 전문가입니다. 사용자의 메시지를 '고객'에게 안내하는 상황에 맞게 변환하세요.\n"
        "1. 극존칭을 사용하여 최고의 예우를 갖추십시오.\n"
        "2. 전문성과 서비스 마인드가 느껴지도록 신뢰감 있는 단어를 선택하십시오.\n"
        "3. 안내, 공지, 사과 등 목적에 부합하는 정중한 형식을 따르십시오."
    )
}

@app.route('/')
def index():
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(frontend_dir, path)

@app.route('/api/convert', methods=['POST'])
def convert_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "변환할 텍스트가 없습니다."}), 400
    
    text = data.get('text')
    target = data.get('target', 'Upward') # 기본값은 상사
    
    if target not in SYSTEM_PROMPTS:
        return jsonify({"error": "유효하지 않은 수신자 설정입니다."}), 400

    if not client:
        return jsonify({
            "original": text, 
            "converted": "[환경 설정 오류] API 키가 설정되지 않았습니다. 백엔드의 .env 파일을 확인해주세요.",
            "status": "error"
        }), 500

    try:
        print(f"--- Conversion Request: Target={target} ---")
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS[target]},
                {"role": "user", "content": f"다음 문장을 변환해줘: {text}"}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        converted_text = completion.choices[0].message.content.strip()
        
        return jsonify({
            "original": text, 
            "target": target,
            "converted": converted_text
        }), 200

    except Exception as e:
        print(f"API Error: {str(e)}")
        return jsonify({"error": f"AI 변환 중 오류가 발생했습니다: {str(e)}"}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    if not data:
        return jsonify({"error": "데이터가 없습니다."}), 400
    
    # Vercel 환경에서는 파일 저장 대신 로그로 출력하여 확인합니다.
    # 데이터 예시: {"type": "positive", "original": "...", "converted": "...", "target": "..."}
    print(f"--- FEEDBACK RECEIVED ---\n{data}\n-------------------------")
    
    return jsonify({"status": "success", "message": "피드백이 기록되었습니다."}), 200

if __name__ == '__main__':
    # host='0.0.0.0'을 추가하여 네트워크 접속을 명확히 합니다.
    app.run(debug=True, host='0.0.0.0', port=5000)