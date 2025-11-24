from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from transformers import pipeline
from rag.retriever import get_retriever

app = FastAPI()

#placeholder for now; can swap in Azure/OpenAI here -
gen = pipeline("text-generation", model="microsoft/phi-1_5", max_new_tokens=256)
               
retriever=get_retriever(k=3)

class AskRequest(BaseModel):
    question: str
    temperature: float=0.0

@app.post("/ask")
def ask(req: AskRequest):
    #jwk note: from retriever.py: as_retriever implents LangChain Retriever interface, which has .get_reevant_doucuments(query) method
    # docs = retriever.get_relevant_documents(req.question)
    docs = retriever.invoke(req.question)

    #temp
    print(type(retriever), dir(retriever))

    context = "\n\n".join(d.page_content for d in docs)

    prompt = (
        "You are a helfpul assistant. Use the context to answer the question. \n"
        f"Context:\n{context}\n\nQuestion: {req.question}\nAnswer:"

    )

    out = gen(
        prompt,
        do_sample=req.temperature > 0.0,
        temperature=req.temperature,
        )[0]["generated_text"]

    return {
        "question": req.question,
        "context_docs": [d.metadata for d in docs],
        "answer": out[len(prompt):].strip(),
        "temperature_used": req.temperature,

    }

@app.get("/specials")
def specials():
    return "You have found the magic button!!! :)"

@app.get("/health")
def health():
    return{"Bert Campaneris makes unassisted triple play!!!": True}
