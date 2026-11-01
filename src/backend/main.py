import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from src.backend.agentes.agente_gemini import AgenteGemini
from src.backend.agentes.agente_openai import AgenteOpenAI

app = FastAPI()

# Configuración de CORS
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
    mode: str  # 'individual_gemini', 'individual_chatgpt', 'gemini_to_chatgpt', 'chatgpt_to_gemini'

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    modo = request.mode
    user_prompt = request.prompt

    # 1. Agente Individual Gemini
    if modo == "individual_gemini":
        resultado = gemini_agent.procesar(user_prompt)
        return {"agente_usado": "Gemini (Individual)", "respuesta": resultado}

    # 2. Agente Individual ChatGPT
    elif modo == "individual_chatgpt":
        resultado = openai_agent.procesar(user_prompt)
        return {"agente_usado": "ChatGPT (Individual)", "respuesta": resultado}

    # 3. Flujo Interconectado: Gemini -> ChatGPT (ChatGPT analiza y mejora)
    elif modo == "gemini_to_chatgpt":
        salida_gemini = gemini_agent.procesar(user_prompt)
        prompt_mejora = f"Analiza la siguiente respuesta generada por Gemini. Mejora la precisión, los datos y corrige cualquier detalle necesario:\n\n{salida_gemini}"
        resultado_final = openai_agent.procesar(prompt_mejora)
        return {
            "agente_usado": "Flujo Gemini ➔ ChatGPT (Analizado y Mejorado)",
            "respuesta": resultado_final
        }

    # 4. Flujo Interconectado: ChatGPT -> Gemini (Gemini analiza y mejora)
    elif modo == "chatgpt_to_gemini":
        salida_chatgpt = openai_agent.procesar(user_prompt)
        prompt_mejora = f"Analiza la siguiente respuesta generada por ChatGPT. Mejora la precisión, los datos y corrige cualquier detalle necesario:\n\n{salida_chatgpt}"
        resultado_final = gemini_agent.procesar(prompt_mejora)
        return {
            "agente_usado": "Flujo ChatGPT ➔ Gemini (Analizado y Mejorado)",
            "respuesta": resultado_final
        }

    return {"error": "Modo de ejecución no reconocido"}

# Permite servir el index.html y la carpeta src/ en servidor local
app.mount("/src", StaticFiles(directory="src"), name="src")
app.mount("/", StaticFiles(directory=".", html=True), name="root")