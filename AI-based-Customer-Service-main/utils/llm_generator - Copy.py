import requests

API_KEY = "REDACTED"
MODEL = "deepseek/deepseek-r1-0528:free"  # Updated model
#  tested on mistralai/mistral-7b-instruct:free
def generate_answer(context, question, history=[]):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    formatted_history = ""
    if history:
        for turn in history:
            formatted_history += f"User: {turn['user']}\nBot: {turn['bot']}\n"


    prompt = f"""
You are a helpful customer support agent. Answer only based on the provided context.

If there's no exact answer, try to infer it from the context — but do not guess if it's totally unrelated.

Conversation History:{formatted_history} 

Context:
{context}

Question:
{question}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Only answer based on the context."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        print("[ERROR]", response.status_code, response.text)
        return f"[ERROR] {response.status_code} - {response.text}"
