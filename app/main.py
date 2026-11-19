from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Atividade 07 - API DevSecOps", version="1.0.0")


class Mensagem(BaseModel):
    texto: str = Field(min_length=1, max_length=200)


@app.middleware("http")
async def cabecalhos_de_seguranca(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@app.get("/")
def inicio():
    return {"mensagem": "API DevSecOps funcionando"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/echo")
def echo(mensagem: Mensagem):
    return {"resposta": mensagem.texto}
