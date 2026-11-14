
import logging
import time

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

logger = logging.getLogger("viela.monitoramento")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(handler)

logger.propagate = False

app = FastAPI(
    title="VIELA API",
    description="Caminhos que conectam.",
    version="1.0.0",
)


@app.middleware("http")
async def monitorar_requisicoes(request: Request, call_next):
    inicio = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        duracao_ms = (time.perf_counter() - inicio) * 1000

        logger.info(
            "VIELA_METRIC metodo=%s rota=%s status=%d latencia_ms=%.2f",
            request.method,
            request.url.path,
            status_code,
            duracao_ms,
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
