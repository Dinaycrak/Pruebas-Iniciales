import os
from openai import OpenAI

class AgenteOpenAI:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No se encontró OPENAI_API_KEY en las variables de entorno.")
        self.client = OpenAI(api_key=api_key)
        self.system_instruction = "Eres el Agente ChatGPT: Especialista en revisión, contraste de datos y optimización de contenido."

    def procesar(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_instruction},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content