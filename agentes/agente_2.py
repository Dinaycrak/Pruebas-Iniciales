import os
from google import genai

class AgenteDos:
    def __init__(self):
        # Cliente independiente de Gemini para el Agente 2
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        # Sistema en blanco para configurar más adelante
        self.system_instruction = ""

    def responder(self, mensaje_del_agente_1: str) -> str:
        prompt = f"{self.system_instruction}\n\nEntrada del Agente 1: {mensaje_del_agente_1}"
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text