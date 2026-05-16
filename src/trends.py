def analyze_trends(df):

    trend_results = {}

    numeric_columns = df.select_dtypes(
        include="number"
    )

    for column in numeric_columns.columns:

        first_value = df[column].iloc[0]

        last_value = df[column].iloc[-1]

        change = last_value - first_value

        percent_change = (
            (change / first_value) * 100
            if first_value != 0
            else 0
        )

        trend = "stable"

        if percent_change > 10:
            trend = "upward"

        elif percent_change < -10:
            trend = "downward"

        trend_results[column] = {

            "first_value": float(first_value),

            "last_value": float(last_value),

            "change": float(change),

            "percent_change": round(
                percent_change,
                2
            ),

            "trend": trend
        }

    return trend_results