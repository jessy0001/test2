from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# OpenAI API 密鑰從環境變數中取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    response_text = "Hello! World!!!"
    if request.method == "POST":
        user_input = request.form["user_input"]

        # 設定 OpenAI API 請求
        api_url = "https://api.openai.com/v1/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }


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


        # 發送請求到 OpenAI API
        try:
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            response_text = response.json()["choices"][0]["text"].strip()
        except Exception as e:
            response_text = f"出現錯誤：{str(e)}"

    return render_template("index.html", response_text=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)