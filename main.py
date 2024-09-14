
from fastapi import FastAPI
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI()

# entrada de dados
class EnergyData(BaseModel):
    month: str
    generation: float
    consumption: float

# armazenar dados de geração e consumo de energia
energy_data_store: List[Dict] = []


@app.get("/")
async def root():
    return {"message": "Sistema de Gestão de Energia Solar"}

# Adicionar dados de geração e consumo mensal
@app.post("/add_data/")
async def add_energy_data(data: EnergyData):
    global energy_data_store
    # Calcula créditos como geração - consumo
    credits = data.generation - data.consumption
    energy_data_store.append({
        "month": data.month,
        "generation": data.generation,
        "consumption": data.consumption,
        "credits": credits
    })
    return {"message": "Dados adicionados com sucesso", "credits": credits}

# Consultar todos os dados de energia
@app.get("/get_data/")
async def get_all_energy_data():
    return {"energy_data": energy_data_store}

# Consultar créditos acumulados
@app.get("/get_credits/")
async def get_total_credits():
    total_credits = sum([entry["credits"] for entry in energy_data_store])
    return {"total_credits": total_credits}

# Balanço mensal de energia (geração vs consumo)
@app.get("/balance/")
async def get_balance():
    balance_data = [{"month": entry["month"], "balance": entry["generation"] - entry["consumption"]} for entry in energy_data_store]
    return {"balance_per_month": balance_data}