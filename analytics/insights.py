# analytics/insights.py
from typing import Dict, Any, List

def generate_insights(summary: Dict[str, Any], trends: Dict[str, Any], health: Dict[str, Any], correlations: List[Dict[str, Any]] = None) -> List[str]:
    """Generate automated insights based on data summary, trends, and health score."""
    insights = []
    
    # Check health
    score = health.get("health_score", 0)
    if score < 50:
        insights.append(f"Salud critica de datos: el dataset tiene una puntuacion baja ({score}). Revisa faltantes y duplicados.")
    elif score >= 80:
        insights.append("Salud excelente de datos: el dataset se ve limpio y bien estructurado.")
        
    # Check summary
    missing = summary.get("total_missing", 0)
    if missing > 0:
        insights.append(f"Datos faltantes: se detectaron {missing} valores ausentes en el dataset.")
        
    dupes = summary.get("duplicate_rows", 0)
    if dupes > 0:
        insights.append(f"Registros duplicados: se encontraron {dupes} filas duplicadas que pueden afectar el analisis.")
        
    # Check trends
    for col, trend_data in trends.items():
        trend_val = trend_data.get("trend", 0)
        if trend_val > 0:
            insights.append(f"Tendencia positiva en {col}: los datos muestran una trayectoria ascendente (pendiente: {trend_val:.2f}).")
        elif trend_val < 0:
            insights.append(f"Tendencia negativa en {col}: los datos muestran una trayectoria descendente (pendiente: {trend_val:.2f}).")
            
    # Check correlations / Relationships
    if correlations:
        for corr in correlations:
            col1 = corr["col1"]
            col2 = corr["col2"]
            direction = corr["direction"]
            strength = corr["strength"]
            val = corr["correlation"]
            
            if direction == "Positiva":
                insights.append(f"Relación relacional {strength.lower()} positiva ({val}): A medida que '{col1}' aumenta, '{col2}' también tiende a subir. Esto sugiere un fuerte vínculo empresarial que podría explotarse para crecimiento.")
            else:
                insights.append(f"Relación relacional {strength.lower()} negativa ({val}): A medida que '{col1}' aumenta, '{col2}' tiende a bajar. Esto podría indicar un trade-off o canibalización que el negocio debe vigilar.")
            
    if not insights:
        insights.append("No se detectaron insights inmediatos relevantes. Los datos parecen estables sin correlaciones fuertes evidentes.")
        
    return insights
