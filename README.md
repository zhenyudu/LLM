# Large Languge Model (LLM) Applications Development

## 1. Introduction
個人LLM領域的應用開發紀錄

## 2. Applications
- LLM 基礎對答 (app/basic_llm.py)
- LineBot x RAG (app/rag_linebot.py)



## 3. Architecture






## ⌘ 事前準備
- Python
- Ngork
- HuggingFace Account
- Line Developer Account

#### Line Developer Tokens
```
$ export LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
$ export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
```
```python
line_bot_api = LineBotApi('YOUR_LINE_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_LINE_CHANNEL_SECRET')
```