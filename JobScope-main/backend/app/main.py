import os
import requests

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

# CARREGA .ENV
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# VARIÁVEIS DE AMBIENTE
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# CLIENTE IA (GROQ)
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


@app.get("/")
def home():
    return {"message": "API rodando com IA"}


# FUNÇÃO YOUTUBE
def search_youtube_video(profession):

    try:

        query = f"dia a dia da profissão {profession}"

        url = "https://www.googleapis.com/youtube/v3/search"

        params = {
            "part": "snippet",
            "q": query,
            "key": YOUTUBE_API_KEY,
            "maxResults": 1,
            "type": "video"
        }

        response = requests.get(url, params=params)

        data = response.json()

        print(data)

        if "items" not in data:
            return ""

        if len(data["items"]) == 0:
            return ""

        video_id = data["items"][0]["id"]["videoId"]

        return f"https://www.youtube.com/embed/{video_id}"

    except Exception as e:

        print("ERRO YOUTUBE:", e)

        return ""


@app.get("/career/{profession}")
def generate_text(profession: str):

    try:

        prompt = f"""
Explique como funciona a profissão:
{profession}

Responda de forma curta e objetiva.

Máximo de 550 palavras.

Fale sobre:
- rotina
- mercado
- salário

Use tópicos curtos.
"""

        print("enviando para IA")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=300
        )

        print("IA respondeu")

        # TEXTO IA
        text = response.choices[0].message.content

        # VÍDEO YOUTUBE
        video_url = search_youtube_video(profession)

        return {
            "profession": profession,
            "text": text,
            "video": video_url
        }

    except Exception as e:

        print("ERRO:", str(e))

        return {
            "error": str(e)
        }