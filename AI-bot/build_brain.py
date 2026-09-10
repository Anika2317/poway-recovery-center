html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Poway Recovery Center - Chat Test</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

<button id="prc-chat-toggle">💬</button>

<div id="prc-chat-widget">
  <div id="prc-chat-header">
    <span>PRC Support Bot</span>
    <button id="prc-close-btn">&times;</button>
  </div>
  
  <div id="prc-crisis-popup">
    <strong>Crisis Support:</strong> If you are experiencing severe withdrawal or a medical emergency, please call <strong>988</strong> or visit a local San Diego emergency room immediately. We are still here to chat.
    <button class="prc-crisis-close" onclick="document.getElementById('prc-crisis-popup').classList.remove('visible')">&times;</button>
  </div>

  <div id="prc-chat-body">
    <div class="prc-msg bot">Hi. This is a safe, confidential space. How can we support your recovery today?</div>
  </div>
  
  <div id="prc-chat-input-area">
    <input type="text" id="prc-chat-input" placeholder="Type your message..." />
    <button id="prc-send-btn">➤</button>
  </div>
</div>

<script>
  const toggleBtn = document.getElementById('prc-chat-toggle');
  const widget = document.getElementById('prc-chat-widget');
  const closeBtn = document.getElementById('prc-close-btn');
  const inputArea = document.getElementById('prc-chat-input');
  const sendBtn = document.getElementById('prc-send-btn');
  const chatBody = document.getElementById('prc-chat-body');
  const crisisPopup = document.getElementById('prc-crisis-popup');

  // UPDATED: Now points to our actual Python server brain!
  const BACKEND_WEBHOOK_URL = '/api/chat';

  toggleBtn.addEventListener('click', () => {
    widget.classList.add('open');
    toggleBtn.style.display = 'none';
  });

  closeBtn.addEventListener('click', () => {
    widget.classList.remove('open');
    setTimeout(() => toggleBtn.style.display = 'block', 300);
  });

  async function sendMessage() {
    const text = inputArea.value.trim();
    if (!text) return;

    const userMsg = document.createElement('div');
    userMsg.className = 'prc-msg user';
    userMsg.textContent = text;
    chatBody.appendChild(userMsg);
    inputArea.value = '';
    chatBody.scrollTop = chatBody.scrollHeight;

    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'prc-msg bot';
    loadingMsg.textContent = '...';
    chatBody.appendChild(loadingMsg);
    chatBody.scrollTop = chatBody.scrollHeight;

    try {
      const response = await fetch(BACKEND_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      
      const data = await response.json();
      chatBody.removeChild(loadingMsg);
      
      if (data.isCrisis) {
        crisisPopup.classList.add('visible');
      }
      
      const botMsg = document.createElement('div');
      botMsg.className = 'prc-msg bot';
      botMsg.textContent = data.reply || "I'm here for you. Let's get you connected to a meeting.";
      chatBody.appendChild(botMsg);
    } catch (error) {
      chatBody.removeChild(loadingMsg);
      const errorMsg = document.createElement('div');
      errorMsg.className = 'prc-msg bot';
      errorMsg.textContent = "We're experiencing a connection issue, but you are not alone. Please call our main line at (858) 414-1856.";
      chatBody.appendChild(errorMsg);
    }
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  sendBtn.addEventListener('click', sendMessage);
  inputArea.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
</script>

</body>
</html>
"""

makefile_content = """install:
\tpip install libsass flask openai

css:
\tpysassc style.sass style.css

run:
\tpython3 server.py

dev: install css run
"""

server_content = """from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.')

# 1. Serve the Frontend HTML
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# 2. Serve the CSS file
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# 3. The Bot's Brain (API Endpoint)
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').lower()
    
    # Crisis Detection Logic
    crisis_keywords = ['suicide', 'kill', 'die', 'shaking', 'seizure', 'emergency', 'hospital', 'relapse', 'overdose']
    is_crisis = any(word in user_message for word in crisis_keywords)
    
    # Trauma-Informed Response Router
    if is_crisis:
        reply = "Your nervous system is under extreme stress right now. This physical reaction is severe, and we need to keep you safe. Please use the resources on your screen or head to a San Diego ER."
    elif "craving" in user_message or "want to use" in user_message or "urge" in user_message:
        reply = "Your brain is experiencing dopamine depletion right now, which triggers false alarm signals. This craving is a physical symptom of withdrawal, not a failure of your willpower. We have 36 weekly 12-step meetings in Poway to help you through this."
    elif "hi" in user_message or "hello" in user_message:
        reply = "Hello. This is a safe, confidential space rooted in understanding how addiction affects the brain. How is your body and nervous system feeling today?"
    else:
        reply = "I hear you. Addiction physically rewires the nervous system, and what you are experiencing is valid. Would you like information on our local ACA groups or meeting schedules?"
        
    return jsonify({
        "reply": reply,
        "isCrisis": is_crisis
    })

if __name__ == '__main__':
    print("Starting Poway Recovery Center Secure Server on http://localhost:8000")
    app.run(port=8000)
"""

with open('index.html', 'w') as f:
    f.write(html_content)

with open('Makefile', 'w') as f:
    f.write(makefile_content)

with open('server.py', 'w') as f:
    f.write(server_content)

print("SUCCESS: The brain (server.py) has been built, and the frontend is connected!")