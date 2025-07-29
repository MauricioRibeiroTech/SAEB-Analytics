import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Análise de Desempenho em Simulados",
    page_icon="📊",
    layout="wide"
)


# Carregar dados
@st.cache_data
def load_data():
    data = pd.read_csv("pages/LAM.csv", sep=";", encoding='utf-8-sig')
    # Limpar nomes de colunas
    data.columns = data.columns.str.strip()
    # Substituir 0 por NaN para facilitar análise
    data.replace(0, np.nan, inplace=True)
    return data


df = load_data()

# Título
st.title("📊 Análise de Desempenho em Simulados - Turma 9A LAM")

# Sidebar com filtros
st.sidebar.header("Filtros")
selected_simulado = st.sidebar.selectbox(
    "Selecione o Simulado:",
    options=["Todos"] + [f"Simulado {i}" for i in range(1, 6)]
)

show_absent = st.sidebar.checkbox("Mostrar alunos ausentes", value=False)

# Processar dados conforme filtros
if selected_simulado != "Todos":
    simulado_col = selected_simulado.replace(" ", "")
    df_filtered = df[["Aluno", "Série", "Turma", simulado_col]].copy()
else:
    df_filtered = df.copy()

if not show_absent:
    df_filtered = df_filtered.dropna(how='all', subset=[col for col in df_filtered.columns if "Simulado" in col])

# Layout em abas
tab1, tab2, tab3, tab4 = st.tabs(["📈 Visão Geral", "📊 Estatísticas", "👤 Desempenho Individual", "🏆 Ranking"])

with tab1:
    st.header("Visão Geral da Turma")

    # Gráfico de participação por simulado
    st.subheader("Participação nos Simulados")
    participation = df[[f"Simulado {i}" for i in range(1, 6)]].notna().sum().reset_index()
    participation.columns = ["Simulado", "Participantes"]

    fig = px.bar(participation, x="Simulado", y="Participantes",
                 color="Participantes", text="Participantes",
                 color_continuous_scale="Blues")
    fig.update_layout(title_text="Número de Alunos por Simulado", title_x=0.3)
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap de desempenho
    st.subheader("Mapa de Calor de Desempenho")
    simulado_cols = [f"Simulado {i}" for i in range(1, 6)]
    df_melted = df.melt(id_vars=["Aluno"], value_vars=simulado_cols,
                        var_name="Simulado", value_name="Nota")

    heatmap_data = df_melted.pivot_table(index="Aluno", columns="Simulado", values="Nota")

    plt.figure(figsize=(12, 10))
    sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".0f",
                linewidths=.5, cbar_kws={'label': 'Nota'})
    plt.title("Desempenho dos Alunos em Cada Simulado", pad=20)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    st.pyplot(plt)
    plt.clf()

with tab2:
    st.header("Estatísticas Descritivas")

    if selected_simulado == "Todos":
        st.subheader("Estatísticas por Simulado")
        stats = df[[f"Simulado {i}" for i in range(1, 6)]].describe().T
        stats = stats[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]
        stats.columns = ['Participantes', 'Média', 'Desvio Padrão', 'Mínimo',
                         '25%', 'Mediana', '75%', 'Máximo']
        st.dataframe(stats.style.background_gradient(cmap='Blues'))

        # Boxplot comparativo
        st.subheader("Distribuição das Notas por Simulado")
        fig = px.box(df_melted, x="Simulado", y="Nota", color="Simulado",
                     points="all", hover_data=["Aluno"])
        fig.update_layout(title_text="Comparação entre Simulados", title_x=0.3)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.subheader(f"Estatísticas do {selected_simulado}")
        col1, col2 = st.columns(2)

        with col1:
            stats = df_filtered[simulado_col].describe()
            st.metric("Média", f"{stats['mean']:.1f}")
            st.metric("Mediana", f"{stats['50%']:.1f}")
            st.metric("Desvio Padrão", f"{stats['std']:.1f}")

        with col2:
            st.metric("Nota Máxima", f"{stats['max']:.1f}")
            st.metric("Nota Mínima", f"{stats['min']:.1f}")
            st.metric("Participantes", f"{stats['count']:.0f}")

        # Histograma
        st.subheader("Distribuição de Notas")
        fig = px.histogram(df_filtered, x=simulado_col, nbins=15,
                           color_discrete_sequence=['#1f77b4'])
        fig.update_layout(title_text=f"Distribuição de Notas - {selected_simulado}",
                          title_x=0.3,
                          xaxis_title="Nota",
                          yaxis_title="Número de Alunos")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Desempenho Individual")

    selected_student = st.selectbox("Selecione o Aluno:", df["Aluno"].unique())

    student_data = df[df["Aluno"] == selected_student].iloc[0]
    simulado_scores = [student_data[f"Simulado {i}"] for i in range(1, 6)]

    # Gráfico de evolução
    st.subheader(f"Evolução do Desempenho - {selected_student}")

    fig = px.line(x=[f"Simulado {i}" for i in range(1, 6)], y=simulado_scores,
                  markers=True, text=simulado_scores,
                  labels={"x": "Simulado", "y": "Nota"})
    fig.update_traces(textposition="top center", line_color='#1f77b4',
                      marker=dict(size=10, color='#ff7f0e'))
    fig.update_layout(yaxis_range=[0, 15], title_x=0.3)
    st.plotly_chart(fig, use_container_width=True)

    # Comparação com a turma
    st.subheader("Comparação com a Turma")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Último Simulado**")
        last_simulado = "Simulado 5"
        student_last_score = student_data[last_simulado]
        if pd.isna(student_last_score):
            st.warning("Aluno ausente no último simulado")
        else:
            class_avg = df[last_simulado].mean()
            diff = student_last_score - class_avg
            st.metric("Sua Nota", f"{student_last_score:.1f}",
                      f"{diff:+.1f} em relação à média")

    with col2:
        st.markdown("**Melhor Desempenho**")
        best_score = max([score for score in simulado_scores if not pd.isna(score)])
        best_simulado = [f"Simulado {i + 1}" for i, score in enumerate(simulado_scores)
                         if score == best_score][0]
        st.metric("Melhor Nota", f"{best_score:.1f}", best_simulado)

with tab4:
    st.header("Ranking de Desempenho")

    # Calcular média geral (considerando apenas alunos que fizeram pelo menos 3 simulados)
    df['Média'] = df[[f"Simulado {i}" for i in range(1, 6)]].mean(axis=1)
    df['Participação'] = df[[f"Simulado {i}" for i in range(1, 6)]].count(axis=1)
    ranking_df = df[df['Participação'] >= 3].sort_values('Média', ascending=False)

    # Top 5 alunos
    st.subheader("Top 5 Alunos")
    top5 = ranking_df.head(5)[['Aluno', 'Média', 'Participação']]
    top5['Média'] = top5['Média'].round(1)

    fig = px.bar(top5, x="Aluno", y="Média",
                 color="Média", text="Média",
                 hover_data=["Participação"],
                 color_continuous_scale="greens")
    fig.update_layout(title_text="Melhores Médias (mínimo 3 simulados)", title_x=0.3)
    st.plotly_chart(fig, use_container_width=True)

    # Tabela de ranking completa
    st.subheader("Ranking Completo")
    full_ranking = ranking_df[['Aluno', 'Média', 'Participação']].copy()
    full_ranking['Média'] = full_ranking['Média'].round(1)
    full_ranking['Posição'] = range(1, len(full_ranking) + 1)
    full_ranking = full_ranking[['Posição', 'Aluno', 'Média', 'Participação']]

    st.dataframe(
        full_ranking.style \
            .background_gradient(subset=['Média'], cmap='YlGnBu') \
            .format({'Média': '{:.1f}'}),
        height=600
    )

# Rodapé
st.markdown("---")
st.markdown("**Desenvolvido para análise de desempenho em simulados - Turma 9A LAM**")