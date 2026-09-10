server_content = """from flask import Flask, request, jsonify, send_from_directory
import os
from openai import OpenAI

app = Flask(__name__, static_folder='.')

# =================================================================
# IMPORTANT: You MUST replace this with a real OpenAI API Key!
# =================================================================
OPENAI_API_KEY = 'YOUR-KEY-HERE4TXXFYEo7ZApbRjZeBxiyslhAOe8sAkzJiXE82A6kOaCW2fPrspSAEJYhoFWWT4PEMr7d2bgXeT3BlbkFJ52GmNobjEhyfKNE13Lz_c6LBxu6TIk5lfP9qeg_Kvgs74LyhE9J3bDRx-ppfs6JHkY7o2Co_wA'
client = OpenAI(api_key=OPENAI_API_KEY)

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
    
    # 1. Safety Triage: Check for crisis keywords BEFORE asking the AI
    crisis_keywords = ['suicide', 'kill', 'die', 'shaking', 'seizure', 'emergency', 'hospital', 'relapse', 'overdose']
    is_crisis = any(word in user_message.lower() for word in crisis_keywords)
    
    # 2. The Real AI Brain
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a trauma-informed AI assistant for Poway Recovery Center. You understand withdrawal neuroscience (like PAWS and dopamine depletion). Never gaslight users. If a user is hesitant, gently validate their feelings. Answer naturally and conversationally like a real human. Keep responses concise (1-3 sentences)."
                },
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "I cannot connect to my AI engine. You need to put a real OpenAI API Key into the server.py file!"
        
    return jsonify({
        "reply": reply,
        "isCrisis": is_crisis
    })

if __name__ == '__main__':
    print("Starting Poway Recovery Center REAL AI Server on http://localhost:8000")
    app.run(port=8000)
"""

with open("server.py", "w") as f:
    f.write(server_content)

print("SUCCESS: server.py has been fixed!")