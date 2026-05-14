def generate_insights(results):

    insights = []

    for column, metrics in results.items():

        # PROMEDIOS BAJOS
        if metrics["mean"] < 100:

            insights.append(
                f"⚠️ El promedio de {column} es bajo."
            )

        # ANOMALIAS
        if len(metrics["anomalies"]) > 0:

            insights.append(
                f"🚨 Se detectaron anomalías en {column}."
            )

        # VARIACIONES EXTREMAS
        if metrics["max"] > metrics["mean"] * 5:

            insights.append(
                f"📈 Existe alta variación en {column}."
            )

        # INSIGHT POSITIVO
        if metrics["mean"] > 500:

            insights.append(
                f"✅ {column} muestra rendimiento sólido."
            )

    return insights