from dotenv import load_dotenv
load_dotenv()

import json
from datetime import datetime as dt

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

LOG_FILE = "requests.log"

def log_requests(text, label, score):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps({
            "ts": dt.utcnow().isoformat(),
            "text": text,
            "label": label,
            "score": score
        }) + "\n")


app = FastAPI(title="HF Sentiment Service")

#load at startup
ppl_emotion = pipeline(
    task="sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",

)

class InferenceRequest(BaseModel):
    text: str
    temperature: float = 0.0 #for gen model


@app.post("/predict")
def predict(req: InferenceRequest):
    result = ppl_emotion(req.text)[0]
    label = result["label"]
    score = result["score"]
    input_text = req.text

    log_requests(req.text, label, score)

    return {
        "label": label,
        "score": score,
        "input": input_text,
           
    }

@app.get("/")
def  root():
    return {"status": "all good", "endpoints": ["/predict"]}