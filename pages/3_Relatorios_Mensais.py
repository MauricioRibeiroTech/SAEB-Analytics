import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="SAEB Analytics - Relatório Mensal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
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
    .card {
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #2c3e50; font-size: 24px;">Simulados SAEB 2025</h1>
        <h2 style="color: #3498db; font-size: 18px;">Escola Estadual Helena Dionysio</h2>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("main.py", label="🏠 Página Inicial")
    st.page_link("pages/3_Relatorios_Mensais.py", label="📅 Relatório Mensal", disabled=True)
    st.page_link("pages/2_SAEB_Descritores.py", label="📊 Relatório SAEB Descritores")
    st.page_link("pages/1_SAEB_Metodologia.py", label="📈 Desempenho percentual")

    # Carregar dados
    try:
        df = pd.read_csv("pages/todos.csv", sep=';')

        # Converter colunas de notas para numérico (tratando possíveis erros)
        for col in df.columns:
            if col.startswith('Sim'):
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Converter Turma para string para evitar problemas de ordenação
        df['Turma'] = df['Turma'].astype(str)

    except Exception as e:
        st.error(f"Erro ao carregar ou processar o arquivo: {str(e)}")
        st.stop()

    # Filtros
    with st.container():
        st.markdown("### Configurações do Relatório")
        componente_selecionada = st.selectbox("Componente", ["Matemática", "Português"])

        # Ordenar turmas corretamente como strings
        turmas_disponiveis = sorted(df["Turma"].unique(), key=lambda x: (len(x), x))
        turma_selecionada = st.selectbox("Turma:", turmas_disponiveis)

    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p style="color: #7f8c8d; font-size: 14px;">Desenvolvido por Mauricio A. Ribeiro</p>
        <p style="color: #7f8c8d; font-size: 12px;">mau.ap.ribeiro@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

# Filtrar dados
df_filtrado = df[(df["Turma"] == turma_selecionada) & (df["Componente"] == componente_selecionada)]

# Verificar se há dados
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

# Processar dados
colunas_simulados = [col for col in df_filtrado.columns if col.startswith('Sim')]
df_filtrado = df_filtrado[['Aluno'] + colunas_simulados]

# Calcular métricas
medias = df_filtrado[colunas_simulados].mean().round(1)
desvios = df_filtrado[colunas_simulados].std().round(1)
alunos_acima_60 = (df_filtrado[colunas_simulados] >= 6).sum()

# Converter para porcentagem
df_porcentagem = df_filtrado.copy()
for col in colunas_simulados:
    df_porcentagem[col] = (df_filtrado[col] * 10).round(1)

# Header
st.markdown(f"""
<div style="background-color: #3498db; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; text-align: center; margin: 0;">Relatório de {componente_selecionada}</h1>
    <h2 style="color: white; text-align: center; margin: 0;">Turma: {turma_selecionada}</h2>
</div>
""", unsafe_allow_html=True)

# Layout principal
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown("### 📈 Desempenho dos Alunos")

    # Gráfico de barras agrupadas
    fig = px.bar(
        df_filtrado.melt(id_vars='Aluno', var_name='Simulado', value_name='Nota'),
        x='Aluno',
        y='Nota',
        color='Simulado',
        barmode='group',
        title=f'Notas por Simulado - {turma_selecionada}',
        labels={'Nota': 'Nota (0-10)', 'Aluno': ''},
        height=500,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-45,
        legend_title_text='Simulados'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📊 Métricas de Desempenho")

    # Abas para métricas
    tab1, tab2 = st.tabs(["Médias", "Desvios Padrão"])

    with tab1:
        st.markdown("**Médias das Notas**")
        for i, (simulado, media) in enumerate(medias.items()):
            delta = (media - 6)  # Meta de 6.0
            st.metric(
                label=simulado,
                value=f"{media:.1f}",
                delta=f"{delta:.1f} vs meta",
                delta_color="inverse",
                help=f"Média de desempenho no {simulado}"
            )

    with tab2:
        st.markdown("**Desvios Padrão**")
        for i, (simulado, desvio) in enumerate(desvios.items()):
            st.metric(
                label=simulado,
                value=f"{desvio:.1f}",
                help=f"Variabilidade das notas no {simulado}"
            )

# Seção de alunos acima da média
st.markdown("### 🏆 Alunos com Desempenho Acima da Média (≥ 6.0)")
cols = st.columns(4)

for i, (simulado, num_alunos) in enumerate(alunos_acima_60.items()):
    with cols[i % 4]:
        st.markdown(f"""
        <div class="card">
            <h4 style="margin: 0 0 10px 0;color: #000000;">{simulado}</h4>
            <p style="font-size: 24px; margin: 0; text-align: center; color: #000000;">{num_alunos}</p>
            <p style="font-size: 12px; margin: 0; text-align: center;">alunos acima da meta</p>
        </div>
        """, unsafe_allow_html=True)

# Gráfico de evolução das médias
st.markdown("### 📉 Evolução das Médias por Simulado")
fig_evolucao = px.line(
    x=colunas_simulados,
    y=medias.values,
    markers=True,
    labels={'x': 'Simulado', 'y': 'Média'},
    title='Evolução da Média da Turma',
    height=400
)
fig_evolucao.update_traces(line_color='#3498db', line_width=2.5)
fig_evolucao.add_hline(y=6, line_dash="dash", line_color="red", annotation_text="Meta",
                       annotation_position="bottom right")
fig_evolucao.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_evolucao, use_container_width=True)

# Tabela de alunos
st.markdown("### 📋 Lista Completa de Alunos")
st.dataframe(
    df_porcentagem.style
    .background_gradient(cmap='Blues', subset=colunas_simulados)
    .format({col: "{:.1f}%" for col in colunas_simulados}),
    use_container_width=True,
    height=500,
    column_config={
        "Aluno": st.column_config.TextColumn("Aluno", width="medium"),
        **{col: st.column_config.NumberColumn(col, format="%.1f%%") for col in colunas_simulados}
    },
    hide_index=True
)

# Análise individual por aluno
st.markdown("### 🔍 Análise Individual por Aluno")
aluno_selecionado = st.selectbox("Selecione um aluno:", df_filtrado['Aluno'].unique())

if aluno_selecionado:
    dados_aluno = df_filtrado[df_filtrado['Aluno'] == aluno_selecionado].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### Desempenho de {aluno_selecionado}")
        fig_aluno = px.bar(
            x=colunas_simulados,
            y=dados_aluno[colunas_simulados].values,
            labels={'x': 'Simulado', 'y': 'Nota'},
            text_auto=True,
            color=colunas_simulados,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_aluno.update_layout(showlegend=False)
        fig_aluno.add_hline(y=6, line_dash="dash", line_color="red", annotation_text="Meta")
        st.plotly_chart(fig_aluno, use_container_width=True)

    with col2:
        st.markdown("#### Notas Detalhadas")
        for simulado, nota in dados_aluno[colunas_simulados].items():
            st.metric(
                label=simulado,
                value=f"{nota:.1f}",
                delta=f"{(nota - 6):.1f} vs meta" if nota else None,
                delta_color="inverse" if nota and nota < 6 else "normal"
            )