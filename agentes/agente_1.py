import os
from google import genai

class AgenteUno:
    def __init__(self):
        # Cliente independiente de Gemini para el Agente 1
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        # Sistema en blanco para configurar más adelante
        self.system_instruction = ""

    def responder(self, mensaje_entrada: str) -> str:
        prompt = f"{self.system_instruction}\n\nEntrada: {mensaje_entrada}"
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text