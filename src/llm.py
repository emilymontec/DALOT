from groq import Groq
from dotenv import load_dotenv

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# REPORTE GENERAL
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

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.4
    )

    return response.choices[0].message.content


# CHAT ANALITICO
def chat_with_data(
    context,
    question
):

    prompt = f"""
    Eres un analista senior empresarial.

    Debes responder preguntas
    sobre datos empresariales.

    Contexto del análisis:

    {context}

    Pregunta del usuario:

    {question}

    Responde de forma:
    - profesional
    - clara
    - analítica
    - accionable
    """

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3
    )

    return response.choices[0].message.content