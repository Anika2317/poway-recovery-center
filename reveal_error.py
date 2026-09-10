import re

# Read your current file to find and save your API key automatically
with open('server.py', 'r') as f:
    old_code = f.read()

key_match = re.search(r"OPENAI_API_KEY\s*=\s*['\"](.*?)['\"]", old_code)
current_key = key_match.group(1) if key_match else "YOUR-KEY-HERE4TXXFYEo7ZApbRjZeBxiyslhAOe8sAkzJiXE82A6kOaCW2fPrspSAEJYhoFWWT4PEMr7d2bgXeT3BlbkFJ52GmNobjEhyfKNE13Lz_c6LBxu6TIk5lfP9qeg_Kvgs74LyhE9J3bDRx-ppfs6JHkY7o2Co_wA"

# Write the new, perfect code with the real error message
new_code = """from flask import Flask, request, jsonify, send_from_directory
import os
from openai import OpenAI

app = Flask(__name__, static_folder='.')

OPENAI_API_KEY = '""" + current_key + """'
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
    
    crisis_keywords = ['suicide', 'kill', 'die', 'shaking', 'seizure', 'emergency', 'hospital', 'relapse', 'overdose']
    is_crisis = any(word in user_message.lower() for word in crisis_keywords)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a trauma-informed AI assistant for Poway Recovery Center. You understand withdrawal neuroscience. Never gaslight users. Keep responses concise (1-3 sentences)."
                },
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "OPENAI ERROR: " + str(e)
        
    return jsonify({
        "reply": reply,
        "isCrisis": is_crisis
    })

if __name__ == '__main__':
    print("Starting Poway Recovery Center REAL AI Server on http://localhost:8000")
    app.run(port=8000)
"""

with open('server.py', 'w') as f:
    f.write(new_code)

print("SUCCESS: server.py updated to show the exact error. Your key was kept safe!")