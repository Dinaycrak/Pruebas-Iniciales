// URL base del backend. Si ejecutas localmente usa http://127.0.0.1:8000
const BACKEND_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000"
    : "https://tu-backend-en-la-nube.com"; // Reemplazar al desplegar el backend

async function enviarConsulta() {
    const prompt = document.getElementById('promptInput').value;
    const mode = document.getElementById('agentMode').value;
    const outputBox = document.getElementById('outputResponse');
    const statusBadge = document.getElementById('statusBadge');
    const sendBtn = document.getElementById('sendBtn');

    if (!prompt.trim()) {
        alert("Por favor escribe una consulta o prompt.");
        return;
    }

    sendBtn.disabled = true;
    statusBadge.innerText = "Procesando con los agentes...";
    outputBox.innerText = "Esperando respuesta...";

    try {
        const response = await fetch(`${BACKEND_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt, mode: mode })
        });

        const data = await response.json();

        if (response.ok) {
            statusBadge.innerText = `Modo ejecutado: ${data.agente_usado}`;
            outputBox.innerText = data.respuesta;
        } else {
            statusBadge.innerText = "Error en la consulta";
            outputBox.innerText = data.error || "Ocurrió un problema procesando la solicitud.";
        }
    } catch (err) {
        statusBadge.innerText = "Error de conexión";
        outputBox.innerText = "No se pudo realizar la conexión con el servidor de agentes (FastAPI).";
    } finally {
        sendBtn.disabled = false;
    }
}