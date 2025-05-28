import requests
def get_baidu_answer(text: str) -> str:
    DEEPSEEK_API_KEY = 'api-key'
    DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": text}],
        "temperature": 0.7
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]
if __name__ == '__main__':
   print("有什么问题吗？")
   qu=input()
   anw=get_baidu_answer(qu)
   print(anw)