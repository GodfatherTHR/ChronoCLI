import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def get_completion(self, prompt: str, system_prompt: str = "You are ChronoCLI AI, a highly efficient productivity assistant."):
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Error: {str(e)}"

    def analyze_sessions(self, sessions_data: str):
        prompt = f"Analyze these work sessions and provide productivity insights, focus scores, and burnout warnings:\n{sessions_data}"
        return self.get_completion(prompt)

    def extract_task_info(self, natural_language_input: str):
        system_prompt = "Extract task name, duration (in minutes), category, and tags from the input. Return in JSON format: {'task': '', 'duration': 0, 'category': '', 'tags': []}"
        return self.get_completion(natural_language_input, system_prompt)
