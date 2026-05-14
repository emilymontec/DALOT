from groq import Groq
from dotenv import load_dotenv

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_ai_report(
    results,
    score_data
):

    prompt = f"""
    Eres un analista senior empresarial.
    
    Tu trabajo es:
    - detectar riesgos
    - identificar problemas críticos
    - encontrar oportunidades
    - priorizar problemas
    - generar recomendaciones accionables

    Datos analizados:
    {results}
    
    Business score:
    {score_data}
    
    Problemas detectados:
    {score_data['issues']}
    
    Genera un informe ejecutivo profesional.
    
    Incluye:
    
    1. Resumen general
    2. Riesgos
    3. Fortalezas
    4. Oportunidades
    5. Recomendaciones
    """