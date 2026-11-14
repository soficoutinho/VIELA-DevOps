
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="VIELA API",
    description="Caminhos que conectam.",
    version="1.0.0",
)

trajetos = [
    {
        "id": 1,
        "origem": "Vila Mariana",
        "destino": "Paraíso",
        "horario": "18:00",
    },
    {
        "id": 2,
        "origem": "Ana Rosa",
        "destino": "Vergueiro",
        "horario": "18:30",
    },
]

alertas = [
    {
        "id": 1,
        "local": "Vila Mariana",
        "tipo": "iluminacao",
        "descricao": "Trecho com iluminação insuficiente.",
    },
    {
        "id": 2,
        "local": "Paraíso",
        "tipo": "baixa_movimentacao",
        "descricao": "Trecho com pouca movimentação.",
    },
]


class Alerta(BaseModel):
    local: str = Field(min_length=2)
    tipo: str = Field(min_length=2)
    descricao: str = Field(min_length=5)


@app.get("/")
def inicio():
    return {
        "aplicativo": "VIELA",
        "slogan": "Caminhos que conectam.",
        "status": "online",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/trajetos")
def listar_trajetos():
    return trajetos


@app.get("/alertas")
def listar_alertas():
    return alertas


@app.post("/alertas", status_code=201)
def criar_alerta(alerta: Alerta):
    novo_alerta = {
        "id": len(alertas) + 1,
        **alerta.model_dump(),
    }
    alertas.append(novo_alerta)
    return novo_alerta


@app.get("/match")
def buscar_match(origem: str, destino: str):
    encontrados = [
        trajeto
        for trajeto in trajetos
        if trajeto["origem"].casefold() == origem.casefold()
        and trajeto["destino"].casefold() == destino.casefold()
    ]
    return {
        "total": len(encontrados),
        "trajetos": encontrados,
    }
