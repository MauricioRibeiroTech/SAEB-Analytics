import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página com estilo moderno
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
    h1, h2, h3, h4 {
        color: #2c3e50;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stAlert {
        border-radius: 10px;
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
    st.page_link("pages/3_Relatorios_Mensais.py", label="📅 Relatório Mensal")
    st.page_link("pages/2_SAEB_Descritores.py", label="📊 Relatório SAEB Descritores")
    st.page_link("pages/1_SAEB_Metodologia.py", label="📈 Desempenho percentual")


    # Carregar dados
    df = pd.read_csv("pages/Planilha_turmas_simulados_mensais.csv", sep=',')

    # Filtros em container
    with st.container():
        st.markdown("### Configurações do Relatório")
        componente_selecionada = st.selectbox("Componente", ["Matemática", "Português"])
        turmas_selecionadas = st.radio("Série:", ["6A", "7A", "7B", "8A"])

        # Aplicar filtros
        if componente_selecionada:
            df = df[df["Turma"] == turmas_selecionadas]
            df = df[df["Componente"] == componente_selecionada]

    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p style="color: #7f8c8d; font-size: 14px;">Desenvolvido por Mauricio A. Ribeiro</p>
        <p style="color: #7f8c8d; font-size: 12px;">mau.ap.ribeiro@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

# Processamento dos dados (mantendo a mesma lógica)
labels_colunas = df.columns.tolist()
name_colunas = labels_colunas[3:]
num_colunas = len(name_colunas)

# Calcular métricas
medias_simulado = []
mediana_simulado = []
alunos_acima_media = []
for i in range(num_colunas):
    nome_coluna = f'porc_{i + 1}'
    df[nome_coluna] = (df[str(name_colunas[i])] / 10) * 100
    medias_simulado.append(df[nome_coluna].mean())
    mediana_simulado.append(df[nome_coluna].std())
    alunos_acima_media.append(len(df[df[nome_coluna] >= 60]))

# Cabeçalho principal
st.markdown(f"""
<div style="background-color: #3498db; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; text-align: center; margin: 0;">Relatório de {componente_selecionada}</h1>
    <h2 style="color: white; text-align: center; margin: 0;">Turma: {turmas_selecionadas}</h2>
</div>
""", unsafe_allow_html=True)

# Gráficos e métricas
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown("### 📈 Desempenho dos Alunos")

    # Transformar dados para formato longo (melhor para Plotly)
    df_melted = df.melt(id_vars=['Aluno'], value_vars=name_colunas,
                        var_name='Simulado', value_name='Nota')

    # Criar gráfico interativo
    fig = px.bar(df_melted,
                 x='Aluno',
                 y='Nota',
                 color='Simulado',
                 barmode='group',
                 title='Notas por Simulado',
                 labels={'Nota': 'Nota (0-10)', 'Aluno': ''},
                 height=500,
                 color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-45,
        legend_title_text='Simulados'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📊 Métricas de Desempenho")

    # Criar DataFrame para as métricas
    df_metricas = pd.DataFrame({
        'Simulado': [f"Simulado {i + 1}" for i in range(num_colunas)],
        'Média': medias_simulado,
        'Desvio Padrão': mediana_simulado
    })

    # Mostrar métricas em abas
    tab1, tab2 = st.tabs(["Médias", "Desvios Padrão"])

    with tab1:
        st.markdown("**Médias em Porcentagem**")
        for i, media in enumerate(medias_simulado):
            st.metric(
                label=f"Simulado {i + 1}",
                value=f"{media:.1f}%",
                delta=f"{media - 60:.1f}% vs meta",
                delta_color="inverse",
                help=f"Média de desempenho no Simulado {i + 1}"
            )

    with tab2:
        st.markdown("**Desvios Padrão**")
        for i, desvio in enumerate(mediana_simulado):
            st.metric(
                label=f"Simulado {i + 1}",
                value=f"{desvio:.1f}",
                help=f"Variabilidade das notas no Simulado {i + 1}"
            )

# Seção de alunos acima da média
st.markdown("### :school: Alunos com Desempenho Acima de 60%")
cols = st.columns(4)  # 4 colunas para os cards

for i, num_alunos in enumerate(alunos_acima_media):
    with cols[i % 4]:
        st.markdown(f"""
        <div style="border-radius: 10px; padding: 15px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h4 style="margin: 0 0 10px 0;">Simulado {i + 1}</h4>
            <p style="font-size: 24px; margin: 0; text-align: center;">{num_alunos}</p>
            <p style="font-size: 12px; margin: 0; text-align: center;">alunos acima da meta</p>
        </div>
        """, unsafe_allow_html=True)

# Tabela de alunos com interatividade
st.markdown("### 📋 Lista Completa de Alunos")
labels_colunas_view = ["Aluno"] + name_colunas

# Estilizar a tabela
st.dataframe(
    df[labels_colunas_view].style
    .background_gradient(cmap='Blues', subset=name_colunas)
    .format({col: "{:.1f}" for col in name_colunas}),
    use_container_width=True,
    height=500,
    column_config={
        "Aluno": st.column_config.TextColumn("Aluno", width="medium"),
        **{col: st.column_config.NumberColumn(col, format="%.1f") for col in name_colunas}
    },
    hide_index=True
)
