# analytics/insights.py
from typing import Dict, Any, List

def generate_insights(summary: Dict[str, Any], trends: Dict[str, Any], health: Dict[str, Any]) -> List[str]:
    """Generate automated insights based on data summary, trends, and health score."""
    insights = []
    
    # Check health
    score = health.get("health_score", 0)
    risk = health.get("risk_level", "high")
    
    if score < 50:
        insights.append(f"Critical Data Health: The dataset has a low health score ({score}). Please check for missing values and duplicates.")
    elif score >= 80:
        insights.append("Excellent Data Health: The dataset is clean and well-structured.")
        
    # Check summary
    missing = summary.get("total_missing", 0)
    if missing > 0:
        insights.append(f"Missing Data: Detected {missing} missing values across the dataset.")
        
    dupes = summary.get("duplicate_rows", 0)
    if dupes > 0:
        insights.append(f"Duplicate Records: Found {dupes} duplicate rows that may affect analysis.")
        
    # Check trends
    for col, trend_data in trends.items():
        trend_val = trend_data.get("trend", 0)
        if trend_val > 0:
            insights.append(f"Positive Trend in {col}: The data shows an upward trajectory (slope: {trend_val:.2f}).")
        elif trend_val < 0:
            insights.append(f"Negative Trend in {col}: The data shows a downward trajectory (slope: {trend_val:.2f}).")
            
    if not insights:
        insights.append("No significant immediate insights detected. The data appears stable.")
        
    return insights
