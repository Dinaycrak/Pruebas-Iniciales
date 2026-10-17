import os
from google import genai

class AgenteUno:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("No se encontró GEMINI_API_KEY en las variables de entorno o en el archivo .env")
        
        self.client = genai.Client(api_key=api_key)
        self.system_instruction = ""

    def responder(self, mensaje_entrada: str) -> str:
        prompt = f"{self.system_instruction}\n\nEntrada: {mensaje_entrada}"
        response = self.client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt
        )
        return response.text