import sys
from pathlib import Path

# Agregar dinámicamente la raíz del proyecto a sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import os
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv(override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.backend.agentes.agente_gemini import AgenteGemini
from src.backend.agentes.agente_openai import AgenteOpenAI

app = FastAPI()

# Permite peticiones CORS desde GitHub Pages y entorno local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_agent = AgenteGemini()
openai_agent = AgenteOpenAI()

class ChatRequest(BaseModel):
    prompt: str
    mode: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    modo = request.mode
    user_prompt = request.prompt

    if modo == "individual_gemini":
        resultado = gemini_agent.procesar(user_prompt)
        return {"agente_usado": "Gemini (Individual)", "respuesta": resultado}

    elif modo == "individual_chatgpt":
        resultado = openai_agent.procesar(user_prompt)
        return {"agente_usado": "ChatGPT (Individual)", "respuesta": resultado}

    elif modo == "gemini_to_chatgpt":
        salida_gemini = gemini_agent.procesar(user_prompt)
        prompt_mejora = f"Analiza la siguiente respuesta generada por Gemini. Mejora la precisión, los datos y corrige cualquier detalle necesario:\n\n{salida_gemini}"
        resultado_final = openai_agent.procesar(prompt_mejora)
        return {
            "agente_usado": "Flujo Gemini ➔ ChatGPT (Analizado y Mejorado)",
            "respuesta": resultado_final
        }

    elif modo == "chatgpt_to_gemini":
        salida_chatgpt = openai_agent.procesar(user_prompt)
        prompt_mejora = f"Analiza la siguiente respuesta generada por ChatGPT. Mejora la precisión, los datos y corrige cualquier detalle necesario:\n\n{salida_chatgpt}"
        resultado_final = gemini_agent.procesar(prompt_mejora)
        return {
            "agente_usado": "Flujo ChatGPT ➔ Gemini (Analizado y Mejorado)",
            "respuesta": resultado_final
        }

    return {"error": "Modo de ejecución no reconocido"}