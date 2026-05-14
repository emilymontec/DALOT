import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from analyzer import analyze_data
from insights import generate_insights
from llm import generate_ai_report
from scoring import calculate_business_score

st.title("DALOT: Analyst MVP")

uploaded_file = st.file_uploader(
    "Sube un archivo CSV",
    type=["csv"]
)

if uploaded_file:

    # LEER CSV
    df = pd.read_csv(uploaded_file)

    # VISTA PREVIA
    st.subheader("Vista previa")
    st.dataframe(df.head())

    # ANALISIS
    results = analyze_data(df)

    # SCORING
    score_data = calculate_business_score(results)

    # INSIGHTS
    insights = generate_insights(results)

    # METRICAS
    st.subheader("Métricas")
    st.json(results)

    # BUSINESS HEALTH
    st.subheader("Business Health")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Health Score",
            f"{score_data['score']}/100"
        )

    with col2:

        st.metric(
            "Risk Level",
            score_data["risk_level"]
        )

    # ISSUES
    st.subheader("Detected Issues")

    for issue in score_data["issues"]:

        st.write(f"- {issue}")

    # INSIGHTS
    st.subheader("Insights")

    for insight in insights:

        st.write(f"- {insight}")

    # IA REPORT
    st.subheader("Reporte IA")

    try:

        with st.spinner(
            "Generando análisis IA..."
        ):

            ai_report = generate_ai_report(
                results,
                score_data
            )

        st.write(ai_report)

    except Exception as e:

        st.error(f"Error IA: {e}")

    # GRAFICOS
    st.subheader("Gráficos")

    numeric_columns = df.select_dtypes(
        include="number"
    )

    for column in numeric_columns.columns:

        fig, ax = plt.subplots()

        ax.plot(df[column])

        ax.set_title(column)

        st.pyplot(fig)

# Para ejecutar: streamlit run app.py