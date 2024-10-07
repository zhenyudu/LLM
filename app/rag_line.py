import os
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from model.model import model_loader
from vectordb.vectordb import get_retriever


app = FastAPI()

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    raise Exception("Specify LINE_CHANNEL_SECRET as environment variable.")
if channel_access_token is None:
    raise Exception("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

model = model_loader(
    model_name  = "llama3.2",
    params      = {
        "temperature": 0.1,
        "max_new_tokens": 512,
        "context_length": 2048,
        "top_k": 10,
        "top_p": 0.95,
        "repetition_penalty": 1.2,
        "seed": 42,
    }
)
vectordb = get_retriever()

def get_answer(question):
    retrieval = vectordb.similarity_search_with_relevance_scores(question, k=5)
    context = "\n\n".join( [doc[0].page_content for doc in retrieval] )
    prompt = f"""
    只能使用繁體中文回答問題。
    請根據參考文件回答使用者問題。
    參考文件：\n{context}\n
    使用者問題：{question}
    你的回答：
    """
    return model.invoke(prompt)


@app.post("/callback")
async def callback(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    reply_text = get_answer(text).content
    # reply_text = f"你說了: {text}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)