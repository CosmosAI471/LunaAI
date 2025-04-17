import requests

url = "https://cosmosai471--lunaapi.hf.space/generate"
data = {
    "prompt": "What is the capital of Japan?",
    "max_tokens": 256
}
response = requests.post(url, json=data)
print(response.json())
