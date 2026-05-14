def calculate_business_score(results):

    score = 100

    issues = []

    risk_level = "LOW"

    for column, metrics in results.items():

        # PROMEDIOS BAJOS
        if metrics["mean"] < 100:

            score -= 10

            issues.append(
                f"{column} tiene promedio bajo"
            )

        # ANOMALIAS
        if len(metrics["anomalies"]) > 0:

            score -= 15

            issues.append(
                f"Anomalías detectadas en {column}"
            )

        # VALORES MUY ALTOS
        if metrics["max"] > metrics["mean"] * 5:

            score -= 10

            issues.append(
                f"Variaciones extremas en {column}"
            )

    # EVITAR NEGATIVOS
    if score < 0:
        score = 0

    # CLASIFICAR RIESGO
    if score < 50:
        risk_level = "HIGH"

    elif score < 80:
        risk_level = "MEDIUM"

    return {

        "score": score,

        "risk_level": risk_level,

        "issues": issues
    }