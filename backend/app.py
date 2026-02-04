import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
client = None

if api_key and api_key != "your_groq_api_key_here":
    try:
        client = Groq(api_key=api_key)
        print("Groq client initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
else:
    print("Warning: GROQ_API_KEY is not set or is the default value. AI features will return mock data.")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify server status."""
    return jsonify({"status": "healthy", "service": "BizTone Converter API"}), 200

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """
    Endpoint to convert text using Groq API.
    Expects JSON: { "text": "...", "target": "boss" | "colleague" | "customer" }
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data.get('text')
    target = data.get('target', 'boss') # Default to boss

    # Mock response if client is not initialized
    if not client:
        return jsonify({
            "original": text,
            "converted": f"[Mock] ({target}) 변환된 텍스트입니다: {text}",
            "note": "Real AI conversion requires a valid GROQ_API_KEY."
        }), 200

    try:
        # Define system prompts based on target
        system_prompts = {
            "boss": "You are a helpful assistant. Convert the following text into a polite, professional, and respectful business tone suitable for reporting to a boss (Superior). Use formal Korean honorifics (Hasio-che or Hapsyo-che).",
            "colleague": "You are a helpful assistant. Convert the following text into a polite but cooperative business tone suitable for a colleague in another team. Use 'Haeyo-che' (polite informal) but maintain professional courtesy.",
            "customer": "You are a helpful assistant. Convert the following text into a formal, very polite, and service-oriented business tone suitable for communicating with an external customer. Focus on empathy and professionalism."
        }

        system_content = system_prompts.get(target, system_prompts["boss"])

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": f"Text to convert: {text}"
                }
            ],
            model="llama3-8b-8192", # Using a fast model supported by Groq
        )

        converted_text = chat_completion.choices[0].message.content

        return jsonify({
            "original": text,
            "converted": converted_text
        }), 200

    except Exception as e:
        print(f"Error during AI conversion: {e}")
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
