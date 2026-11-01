import os
from google import genai

class AgenteGemini:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("No se encontró GEMINI_API_KEY en las variables de entorno.")
        self.client = genai.Client(api_key=api_key)
        self.system_instruction = "Eres el Agente Gemini: Especialista en análisis inicial, estructuración y síntesis de respuestas."

    def procesar(self, prompt: str) -> str:
        prompt_completo = f"{self.system_instruction}\n\nEntrada del usuario: {prompt}"
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt_completo
        )
        return response.text