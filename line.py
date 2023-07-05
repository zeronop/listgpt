from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "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"
model_use = "text-davinci-003"

channel_secret = "b908058801e7f02983496f50f5d4dd95"
channel_access_token = "FCqiYnEDr92OYzf7H2IwgD3Uq7DK+qNU8mA3k4cyMZ+A/7SE+SSfqI+3g7oOlB7Po/wgOfnYGTKSJJ7A2kzLlDVLdKZ4/A24KhRQNZdWgedPmKunhrw/rhZi2i0iHM7X5zqnvL1qOQoJuJzLVduQwgdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    prompt_text = text

    response = openai.Completion.create(
        model=model_use,
        prompt=prompt_text,  
        max_tokens=1024) # max 4096

    text_out = response.choices[0].text 
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()
