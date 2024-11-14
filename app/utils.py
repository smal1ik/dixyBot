import json
from decouple import config
import requests

from app.database.requests import add_error, add_comments

url_gpt = "https://api.openai.com/v1/chat/completions"
head_gpt = {
    "Content-Type": "application/json",
    "Authorization": "Bearer"
}


async def send_chatgpt(text):
    prompt = "".join(config("GPT_PROMPT"))
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"Идея ребёнка: {text}"
            }
        ],
        "max_tokens": config("MAX_TOKENS", cast=int),
        "temperature": config("TEMPERATURE", cast=float),

    }
    result = requests.post(url_gpt, headers=head_gpt, data=json.dumps(data))
    if result.status_code == 200:
        res = result.json()
        res = json.loads(res.get("choices")[0].get("message").get("content"))
        if res.get("head") == "error":
            #Тут добавляем статистику error +1
            await add_error()
            return None
        # Тут добавляем статистику accept +1
        await add_comments()
        return res
    return None

    # a = {'id': 'chatcmpl-AT9fYLllyI7XkTXfhvC9gFQdfeVLv', 'object': 'chat.completion', 'created': 1731512044, 'model': 'gpt-4o-mini-2024-07-18', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': '{"head": "error", "body": ""}', 'refusal': None}, 'logprobs': None, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 1050, 'completion_tokens': 11, 'total_tokens': 1061, 'prompt_tokens_details': {'cached_tokens': 0, 'audio_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 0, 'audio_tokens': 0, 'accepted_prediction_tokens': 0, 'rejected_prediction_tokens': 0}}, 'system_fingerprint': 'fp_0ba0d124f1'}


url_dixy = "https://api.dixy-stories.ru/story"
head_dixy = {
    "Content-Type": "application/json",
    "Authorization": "Basic YWRtaW46dlZxMVFhVGtJclVPbkI4VA=="
}


def send_dixy(text):
    data = {
    "title": text.get("head"),
    "content": text.get("body")
    }
    res = requests.post(url_dixy, headers=head_dixy, data=json.dumps(data))
    print(res.status_code)

    if res.status_code == 200:
        res = res.json()
        return res.get('result')
    return None
