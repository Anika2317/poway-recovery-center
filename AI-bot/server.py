from flask import Flask, request, jsonify, send_from_directory
import os
import google.generativeai as genai

app = Flask(__name__, static_folder='.')

# =================================================================
# Put your FREE Gemini API key between the single quotes below:
# =================================================================
GEMINI_API_KEY = 'YOUR-FREE-KEY-HERE'
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the trauma-informed Gemini brain
model = genai.GenerativeModel(
    'gemini-3.6-flash',
    system_instruction="You are a trauma-informed AI assistant for Poway Recovery Center. You understand withdrawal neuroscience (like PAWS and dopamine depletion). Never gaslight users. If a user is hesitant, gently validate their feelings. Answer naturally and conversationally like a real human. Keep responses concise (1-3 sentences)."
)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    # 1. Safety Triage
    crisis_keywords = ['suicide', 'kill', 'die', 'shaking', 'seizure', 'emergency', 'hospital', 'relapse', 'overdose']
    is_crisis = any(word in user_message.lower() for word in crisis_keywords)
    
    # 2. The Free Gemini AI Brain
    try:
        response = model.generate_content(user_message)
        reply = response.text
    except Exception as e:
        reply = "GEMINI ERROR: " + str(e)
        
    return jsonify({
        "reply": reply,
        "isCrisis": is_crisis
    })

if __name__ == '__main__':
    print("Starting Poway Recovery Center FREE AI Server on http://localhost:8000")
    app.run(port=8000)