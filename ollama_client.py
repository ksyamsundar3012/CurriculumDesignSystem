import requests

def query_granite(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "granite:3.3-2b", "prompt": prompt},
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            text = data.get("response", "")
            return text
        else:
            return None
    except Exception as e:
        print("Ollama connection failed:", e)
        return None
