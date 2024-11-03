from flask import Flask, request, render_template, send_from_directory, abort
import requests
import os
from dotenv import load_dotenv

# Initialize the Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Check for API Key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("API key is missing. Please set OPENAI_API_KEY as an environment variable.")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Cache content from JoannTalk.txt
cached_content = None

def load_file_content():
    global cached_content
    if cached_content is None:
        try:
            with open('private/JoannTalk.txt', 'r', encoding='utf-8') as f:
                cached_content = f.read()
        except FileNotFoundError:
            print("File not found: private/JoannTalk.txt")
            cached_content = ""
    return cached_content

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except FileNotFoundError:
        return "<h1>index.html not found</h1>", 500

@app.route('/process', methods=['GET'])
def process():
    user_input = request.args.get('user-input')
    if not user_input:
        return render_template('index.html', messages=[{"role": "Chatbot", "content": "請輸入有效的問題。"}])

    # Prepend "Joann，妳"  to the user input
    modified_input = f"Joann，妳{user_input}"

    # Load RoseTalk.txt content
    specified_file_content = load_file_content()
    if not specified_file_content:
        return render_template('index.html', messages=[{"role": "Chatbot", "content": "無法找到指定的文件 RoseTalk.txt。"}])

    # Construct the system message
    system_message = (
        f"你是一個問答系統，基於以下內容回答問題：\n"
        f"{specified_file_content}\n"
        "你是一位人生導師，請用溫暖的對話方式來回答。\n"
        "請按照以下格式回答：\n"
        "- 每個標題只使用一個 #，如：# 主題。\n"
        "- 各段落之間請換行，保持清楚結構。\n"
        "- 每個要點前請加上 1.、2. 等編號。\n"
        "- 最後請提供簡潔的總結。"
    )

    # Prepare API request payload
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.4,
        "max_tokens": 1000
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}'
    }

    # Make the API request
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data
        )
        response.raise_for_status()
        answer = response.json().get('choices', [{}])[0].get('message', {}).get('content', '無法取得回覆。')
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        answer = f"API 請求失敗，狀態碼：{response.status_code}"
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        answer = "API 請求失敗，請稍後再試。"

    return render_template('index.html', messages=[{"role": "回覆", "content": answer}])

@app.before_request
def restrict_access():
    pass  # Modify this function as needed for access control

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)