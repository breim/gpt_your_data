import requests
from dotenv import load_dotenv
import os

load_dotenv()

class ChatGPTService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("API key must be provided, either via argument or environment variable OPENAI_API_KEY.")
    
    def generate_response(self, prompt: str, semantic_result: str, model: str = "gpt-4o-mini", max_tokens: int = 500) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        descriptions = [item['pokemon'].description for item in semantic_result]

        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Read the following passage and answer the question based solely on what is stated in the text"},
                {"role": "user", "content": f"Text: {descriptions}, Question:{prompt}"}
            ],
            "max_tokens": max_tokens
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
        
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip()
