from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# OpenAI API 密鑰從環境變數中取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        user_input = request.form["user_input"]

        # 設定 OpenAI API 請求
        api_url = "https://api.openai.com/v1/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

    data = {
        "model": "gpt-4o-mini",  # 模型名稱
        "messages": [
            {"role": "user", "content": "Please tell me about open ai"}  # 用戶的輸入
        ],
        "max_tokens": 100  # 控制生成的最大 token 數
    }

   # 發送 POST 請求
    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        # 請求成功，返回的資料
        response_data = response.json()
        response_text = response_data['choices'][0]['message']['content']  # 獲取生成的內容
    else:
        # 請求失敗，輸出錯誤信息
        response_text = f"Error: {response.status_code}, {response.text}"

    return render_template("index.html", response_text=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    