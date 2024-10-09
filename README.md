# Large Languge Model (LLM) Applications Development

## 1. Introduction
個人LLM領域的應用開發紀錄

## 2. Applications
- LLM 基礎對答 (app/basic_llm.py)
- LineBot x RAG (app/rag_linebot.py)



## 3. Architecture






## ⌘ 事前準備
- **Ollama**
- **Hugging Face**
- **Line Developer**
- **Ngrok**


### Ollama
[Download](https://ollama.com/download)
- Ollama run LLM on Terminal
```terminal
ollama run llama3.2
```


### Hugging Face - 開源模型獲取
- 建立 [Hugging Face](https://huggingface.co/) 帳號
- 建立 Access Token
    1. Settings
    2. Access Token
    3. Create New Token


### Line Developer Tokens
- Set environment variables
```terminal
$ export LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
$ export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
```
- Set in code
```python
line_bot_api = LineBotApi('YOUR_LINE_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_LINE_CHANNEL_SECRET')
```


### Ngrok
- Setup: https://dashboard.ngrok.com/get-started/setup/macos