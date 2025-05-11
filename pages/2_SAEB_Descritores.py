import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def per_aluno(A, B):
    p = (A / B) * 100
    return p


# Configuração da página com estilo melhorado
st.set_page_config(
    page_title="SAEB Analytics",
    page_icon=":book:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/MauricioRibeiroTech',
        'Report a bug': "https://github.com/MauricioRibeiroTech",
        'About': "# Aplicativo para os Índices dos Simulados do SAEB-HD"
    }
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 15px;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar melhorada
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #2c3e50; font-size: 24px;">Simulados SAEB 2025</h1>
        <h2 style="color: #3498db; font-size: 18px;">Escola Estadual Helena Dionysio</h2>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("main.py", label="🏠 Página Inicial")
    st.page_link("pages/3-Relatorios Mensais.py", label="📅 Relatório Mensal")
    st.page_link("pages/2-SAEB Descritores.py", label="📊 Relatório SAEB Descritores")
    st.page_link("pages/1-SAEB Metodologia.py", label="📈 Desempenho percentual")

    with st.container():
        st.markdown("### Configurações do Relatório")
        df = pd.read_csv("pages/descritores.csv", sep=",")
        salas_distintas = df["Simulados"].unique().tolist()
        salas_selecionadas = st.selectbox("Selecione o Simulado", salas_distintas)
        componente_selecionada = st.radio("Componente Curricular", ["Matematica", "Portugues"])

        if componente_selecionada:
            df = df[df["Simulados"] == salas_selecionadas]
            df = df[df["Componentes"] == componente_selecionada]

    st.markdown("---")
    st.markdown("### Links Importantes")
    col1, col2 = st.columns(2)
    with col1:
        st.page_link(
            "https://download.inep.gov.br/educacao_basica/prova_brasil_saeb/menu_do_professor/o_que_cai_nas_provas/Matriz_de_Referencia_de_Matematica.pdf",
            label="Matemática", icon="📊")
    with col2:
        st.page_link(
            "https://download.inep.gov.br/educacao_basica/prova_brasil_saeb/menu_do_professor/o_que_cai_nas_provas/Matriz_de_Referencia_de_Lingua_Portuguesa.pdf",
            label="Português", icon="📚")

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p style="color: #7f8c8d; font-size: 14px;">Desenvolvido por Mauricio A. Ribeiro</p>
        <p style="color: #7f8c8d; font-size: 12px;">mau.ap.ribeiro@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

# Conteúdo principal
st.markdown(f"""
<div style="background-color: #3498db; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; text-align: center; margin: 0;">Relatório de {componente_selecionada}</h1>
    <h2 style="color: white; text-align: center; margin: 0;">Simulado: {salas_selecionadas} (Descritores)</h2>
</div>
""", unsafe_allow_html=True)

# Processamento dos dados (mantido igual)
df1 = df.iloc[:, 3:38]
num_NaN = df1.iloc[1].isna().sum()
Num_descritores_contemplados = len(df1.columns) - num_NaN

df_alunos = df.iloc[:, 0]
Num_descritores = len(df1.columns) - num_NaN
Num_alunos = len(df_alunos)
df_analise_alunos = pd.DataFrame()
df_descritores = pd.DataFrame()

df2 = df1.sum(axis=1)
df_analise_alunos['Nomes'] = df_alunos
df_analise_alunos['Porcentagem'] = (df2 / Num_descritores_contemplados) * 100

df_acima_de_60 = df_analise_alunos[df_analise_alunos['Porcentagem'] >= 60]

df_descritores['Descritor'] = df1.columns.tolist()
df_descritores['Porcentagem'] = df1.sum(axis=0).tolist()
df_descritores['Porcentagem'] = (df_descritores['Porcentagem'] / Num_alunos) * 100
df_descritores_mean = df_descritores[df_descritores['Porcentagem'] != 0.0]

# Gráficos interativos com Plotly
st.markdown("## 📊 Desempenho dos Alunos")
fig_alunos = px.bar(df_analise_alunos,
                    x='Nomes',
                    y='Porcentagem',
                    color='Porcentagem',
                    color_continuous_scale='Viridis',
                    text='Porcentagem',
                    labels={'Porcentagem': 'Desempenho (%)', 'Nomes': 'Alunos'},
                    height=500)
fig_alunos.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_alunos.update_layout(xaxis_tickangle=-45, yaxis_range=[0, 100])
st.plotly_chart(fig_alunos, use_container_width=True)

st.markdown(f"## 📈 Desempenho por Descritor - {salas_selecionadas}")
fig_descritores = px.bar(df_descritores_mean.sort_values('Porcentagem', ascending=True),
                         x='Porcentagem',
                         y='Descritor',
                         orientation='h',
                         color='Porcentagem',
                         color_continuous_scale='Plasma',
                         text='Porcentagem',
                         labels={'Porcentagem': 'Acerto (%)', 'Descritor': ''},
                         height=600)
fig_descritores.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_descritores.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_range=[0, 100])
st.plotly_chart(fig_descritores, use_container_width=True)

# Métricas em colunas
st.markdown("## 📌 Indicadores Principais")
a, b = st.columns(2)
dif1 = df_descritores_mean['Porcentagem'].mean().round(2) - 60
dif2 = df_analise_alunos['Porcentagem'].mean().round(2) - 60

a.metric("Média dos Descritores",
         f"{df_descritores_mean['Porcentagem'].mean().round(2)}%",
         f"{dif1.round(2)}% vs meta",
         delta_color="inverse",
         help="Média de acerto em todos os descritores avaliados")

b.metric("Média dos Alunos",
         f"{df_analise_alunos['Porcentagem'].mean().round(2)}%",
         f"{dif2.round(2)}% vs meta",
         delta_color="inverse",
         help="Média de desempenho de todos os alunos")

# Tabelas com estilo
st.markdown(f"## 🏆 Melhores Alunos - {salas_selecionadas}")
st.dataframe(
    df_acima_de_60.round(2).style
    .background_gradient(cmap='Greens', subset=['Porcentagem'])
    .format({'Porcentagem': '{:.1f}%'}),
    use_container_width=True,
    height=400
)

st.markdown(f"## 📋 Descritores por Desempenho - {salas_selecionadas}")
st.dataframe(
    df_descritores_mean.sort_values('Porcentagem', ascending=False).round(2).style
    .background_gradient(cmap='Purples', subset=['Porcentagem'])
    .format({'Porcentagem': '{:.1f}%'}),
    use_container_width=True,
    height=400
)
