import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

load_dotenv()


GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise EnvironmentError("Defina GEMINI_API_KEY no .env")

# Inicializa o cliente Gemini
def init_client():
    return genai.Client(api_key=GEMINI_KEY)

# Cria configuração de geração de conteúdo
def build_config():
    return types.GenerateContentConfig(
        temperature=0,
        response_mime_type="text/plain",
        thinking_config=types.ThinkingConfig(thinking_budget=0),
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_ONLY_HIGH"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"),
        ],
    )

# Instrução inicial do chatbot
SYSTEM_INSTRUCTION = (
    "Você é FUR.IA, chatbot com conhecimento de pro player de CS:GO e coach"
    "Use gírias de CS:GO e memes da comunidade (ex: 'VAMO DE RUSH B', 'bunnyhop', 'bangar', 'eco', etc)"
    "Use expressões de torcida como 'Vamo FURIA!', '#FURIACS', '#DIADEFURIA', mas não exagere usando em todas as frases"
    "Responda em PT-BR de forma direta e envolvente, "
    "Dê dicas práticas (spray control, smokes, rotações) e cite estatísticas recentes quando possível. "
    "Se o usuário pedir, mostre um diagrama ou link de tutorial. "
    "Exemplo: Usuário: Como melhorar meu recoil? --  Assistente: Treine o spray no mapa de tiro por 15 min diários, começando em bursts de 5 balas e subindo gradualmente."
    "Dê respostas de no máximo 3 frases, seja conciso"
    "E lembre que o site é furia.gg e o Instagram é @furiagg."
    "Não exagere mandando todas informações em uma frase só"
)

# Configura o Flask
app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)
client = init_client()
model = "gemini-1.5-flash"

# Histórico de conversas: inicia com a instrução do sistema
history = [
    types.Content(
        role="user",
        parts=[types.Part.from_text(text=SYSTEM_INSTRUCTION)]
    )
]

@app.route("/")
def index():
    return app.send_static_file("landing.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    global history
    data = request.get_json() or {}
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "Mensagem vazia."}), 400

    # Adiciona mensagem do usuário ao histórico
    history.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)]
        )
    )

    # Gera resposta com o histórico completo
    reply_text = ""
    try:
        stream = client.models.generate_content_stream(
            model=model,
            contents=history,
            config=build_config()
        )
        for chunk in stream:
            reply_text += chunk.text
    except Exception as e:
        return jsonify({"reply": f"Erro ao gerar resposta: {e}"}), 500

    # Adiciona resposta do assistente ao histórico
    history.append(
        types.Content(
            role="assistant",
            parts=[types.Part.from_text(text=reply_text)]
        )
    )

    # Limita histórico: mantém somente as últimas N trocas
    max_turns = 20  # número de trocas (usuário+assistente)
    # sistema + últimas max_turns trocas
    if len(history) > max_turns * 2 + 1:
        history = [history[0]] + history[-(max_turns*2):]

    return jsonify({"reply": reply_text})

if __name__ == "__main__":
    app.run(debug=True)