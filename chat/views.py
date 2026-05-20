import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from ai.llm import chat_with_data, generate_ai_report
from ai.memory import memory

def index(request):
    """Render the basic frontend HTML."""
    return render(request, "index.html")

def test_endpoint(request):
    """Health check endpoint."""
    return JsonResponse({"status": "ok", "message": "La API de NURA esta operativa"})

from analytics.analyzer import load_csv, dataset_summary, column_info, compute_correlations
from analytics.scoring import evaluate_business
from analytics.trends import analyze_numeric_trends
from analytics.insights import generate_insights
from analytics.utils import make_json_safe

@csrf_exempt
def analyze_endpoint(request):
    """Endpoint to trigger dataset analysis."""
    if request.method == "POST":
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No se ha subido ningun archivo"}, status=400)
            
        file = request.FILES['file']
        session_id = request.POST.get('session_id', 'default')
        
        try:
            df = load_csv(file)
            summary = dataset_summary(df)
            cols = column_info(df)
            health = evaluate_business(summary)
            trends = analyze_numeric_trends(df)
            correlations = compute_correlations(df)
            insights = generate_insights(summary, trends, health, correlations)
            
            context = {
                "file_name": file.name,
                "summary": summary,
                "columns": cols,
                "health": health,
                "trends": trends,
                "correlations": correlations,
                "insights": insights
            }
            safe_context = make_json_safe(context)
            memory.store_dataset_context(session_id, safe_context)
            
            return JsonResponse(safe_context)
        except Exception as e:
            return JsonResponse({"error": f"Error al analizar el archivo: {str(e)}"}, status=500)
            
    return JsonResponse({"error": "Se requiere una peticion POST"}, status=400)

@csrf_exempt
def chat_endpoint(request):
    """Endpoint for chat interactions."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = (data.get("message", "") or "").strip()
            session_id = data.get("session_id", "default")
            if not message:
                return JsonResponse({"error": "El mensaje no puede estar vacio."}, status=400)
            
            history = memory.get_history(session_id, message)
            
            context = memory.get_dataset_context(session_id) or {
                "has_dataset": False,
                "message": "No hay ningun dataset cargado en esta sesion.",
                "mode": "chat_general",
            }
            
            # This calls the Groq API
            response = chat_with_data(message, context, history)
            
            memory.add_message(session_id, "user", message)
            memory.add_message(session_id, "assistant", response)
            
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Se requiere una peticion POST"}, status=400)
