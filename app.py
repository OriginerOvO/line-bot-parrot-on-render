# 引入 flask 模組中的 Flask, request, abort
from flask import Flask, request, abort

# 引入 linebot 模組中的 LineBotApi（Line Token）, WebhookHandler（Line Secret）
from linebot import (
    LineBotApi, WebhookHandler
)

# 引入 linebot.exceptions 模組中的 InvalidSignatureError（錯誤偵錯的）
from linebot.exceptions import (
    InvalidSignatureError
)

# 引入 linebot.models 模組中的 MessageEvent, TextMessage, TextSendMessage
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# LINE BOT-Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# LINE BOT-Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # Handle Webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# line bot 訊息接收處
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 處理訊息
    msg = event.message.text
    # 回傳訊息
    line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))
        
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
