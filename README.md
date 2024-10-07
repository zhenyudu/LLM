# Large Languge Model (LLM) Applications Development

## 1. Introduction
個人LLM領域的應用開發紀錄

## 2. Projects


## 3. Architecture


### Line Developer Tokens
```
$ export LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
$ export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
```
```python
line_bot_api = LineBotApi('YOUR_LINE_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_LINE_CHANNEL_SECRET')
```