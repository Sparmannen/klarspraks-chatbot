# Använd en Python-bild med FastAPI
FROM python:3.9

# Sätt arbetsmapp
WORKDIR /app

# Kopiera nödvändiga filer
COPY requirements.txt .
COPY app.py .
COPY static/ static/

# Installera beroenden
RUN pip install --no-cache-dir -r requirements.txt

# Exponera port 7860
EXPOSE 7860

# Starta applikationen
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
