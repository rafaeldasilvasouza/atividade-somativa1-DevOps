import sys
import os

# Adiciona o diretório do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sistema de Gestão de Energia Solar"}

# Teste para adicionar dados de geração e consumo
def test_add_energy_data():
    response = client.post("/add_data/", json={
        "month": "Janeiro",
        "generation": 500.0,
        "consumption": 400.0
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Dados adicionados com sucesso"
    assert response.json()["credits"] == 100.0

# Teste para consultar todos os dados de energia
def test_get_all_energy_data():
    response = client.get("/get_data/")
    assert response.status_code == 200
    assert "energy_data" in response.json()
    assert len(response.json()["energy_data"]) > 0

# Teste para consultar os créditos acumulados
def test_get_total_credits():
    response = client.get("/get_credits/")
    assert response.status_code == 200
    assert "total_credits" in response.json()
    assert response.json()["total_credits"] == 100.0

# Teste para consultar o balanço mensal de energia
def test_get_balance():
    response = client.get("/balance/")
    assert response.status_code == 200
    assert "balance_per_month" in response.json()
    assert len(response.json()["balance_per_month"]) > 0
    assert response.json()["balance_per_month"][0]["month"] == "Janeiro"
    assert response.json()["balance_per_month"][0]["balance"] == 100.0
