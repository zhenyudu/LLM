import os
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from model.ModelLoader import ModelLoader
from model.ModelGenerator import ModelGenerator
from vectordb.vectordb import get_retriever

## Set Line API Keys
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    raise Exception("Specify LINE_CHANNEL_SECRET as environment variable.")
if channel_access_token is None:
    raise Exception("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
del channel_access_token, channel_secret

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    global llm, retriever

    ## Load Model & Retriever
    model = ModelLoader.ollama_loader(model_name = "llama3.2")
    llm = ModelGenerator(model=model)
    del model
    retriever = get_retriever()


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
    reply_text = llm.rag_generate(
        retriever   = retriever,
        question    = text,
        params      = {
            "temperature": 0.1,
            "max_new_tokens": 512,
            "context_length": 2048,
            "top_k": 10,
            "top_p": 0.95,
            "repetition_penalty": 1.2,
            "seed": 42,
        }
    ).content
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)