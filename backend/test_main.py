
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health():
    resposta = client.get("/health")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "healthy"


def test_trajetos():
    resposta = client.get("/trajetos")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)


def test_alertas():
    resposta = client.get("/alertas")
    assert resposta.status_code == 200


def test_match():
    resposta = client.get(
        "/match",
        params={
            "origem": "Vila Mariana",
            "destino": "Paraíso",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()["total"] == 1
