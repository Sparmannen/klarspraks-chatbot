from fastapi import FastAPI
from pydantic import BaseModel
import openai
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os

# Skapa en FastAPI-app
app = FastAPI()

# Tillåt CORS för frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Din OpenAI API-nyckel (måste läggas till separat i produktionsmiljö)
openai.api_key = "YOUR_OPENAI_API_KEY"

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(input: TextInput):
    """Analyserar en text och ger klarspråksförslag."""
    prompt = f"""
    Analysera följande text utifrån klarspråksprinciper:
    - Markera långa meningar
    - Ersätt byråkratiska ord
    - Använd enklare formuleringar
    - Ge en kort sammanfattning av textens klarspråksnivå
    
    Text:
    """
    {input.text}
    """
    
    Svara med en förbättrad version av texten samt en kort analys.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Du är en expert på klarspråk och hjälper användare att förenkla myndighetstexter."},
                  {"role": "user", "content": prompt}]
    )
    
    return {"suggested_text": response["choices"][0]["message"]["content"]}

# Servera en enkel HTML-fil som frontend
@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

# Skapa en mapp för frontend-filer
os.makedirs("static", exist_ok=True)
