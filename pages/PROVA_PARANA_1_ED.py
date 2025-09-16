import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- Configurações da Página e Estilo ---
st.set_page_config(
    page_title="Análise de Desempenho - Prova Paraná",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Aprimorado para uma Apresentação Elegante ---
st.markdown("""
<style>
    /* Estilo Geral */
    .main {
        background-color: #f8f9fa; /* Fundo principal mais suave */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50; /* Cor escura e profissional para títulos */
    }

    /* Cards de Métricas */
    .metric-card {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e3e6f0;
        padding: 25px 20px;
        background-color: #ffffff;
        border-left: 5px solid #4e73df; /* Azul primário */
        margin-bottom: 20px;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.08);
    }

    /* Títulos das Seções */
    .header-title {
        color: #2c3e50;
        font-weight: 700;
        font-size: 2.5rem;
    }
    .section-title {
        color: #4e73df;
        font-weight: 600;
        border-bottom: 2px solid #e3e6f0;
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 20px;
    }

    /* Estilo da Tabela de Dados Detalhada */
    .stDataFrame {
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-radius: 10px;
    }
    .stDataFrame thead th {
        background-color: #4e73df;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        text-align: center;
        border-bottom: 2px solid #3655a6;
    }
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #f8f9fc; /* Zebrado sutil */
    }
    .stDataFrame tbody tr:hover {
        background-color: #e9ecef;
    }
    
    /* Sidebar */
    div[data-testid="stSidebarUserContent"] {
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)


# --- Configuração Centralizada das Turmas ---
TURMAS_CONFIG = {
    "6º Ano A": {"arquivo": "PPR_6A.csv"},
    "7º Ano A": {"arquivo": "PPR_7A.csv"},
    "7º Ano B": {"arquivo": "PPR_7B.csv"},
    "8º Ano A": {"arquivo": "PPR_8A.csv"},
    "9º Ano A": {"arquivo": "PPR_9A.csv"},
}

# --- Funções do Aplicativo ---

@st.cache_data
def carregar_dados(nome_arquivo):
    """
    Carrega os dados da turma usando um método robusto para encontrar o arquivo e limpar os nomes das colunas.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_completo = os.path.join(script_dir, nome_arquivo)

        if not os.path.exists(caminho_completo):
            st.error(f"Arquivo não encontrado: '{caminho_completo}'. Certifique-se de que o CSV está na mesma pasta do script.")
            return None

        df = pd.read_csv(caminho_completo, sep=';', decimal=',')
        df.columns = [str(col).strip().upper() for col in df.columns]
        
        if 'ALUNO' not in df.columns:
            col_aluno = next((col for col in df.columns if 'ALUNO' in col or 'NOME' in col), None)
            if col_aluno:
                df.rename(columns={col_aluno: 'ALUNO'}, inplace=True)
            else:
                df.rename(columns={df.columns[0]: 'ALUNO'}, inplace=True)
        return df
    except Exception as e:
        st.error(f"Ocorreu um erro ao ler o arquivo '{nome_arquivo}': {e}")
        return None

def processar_dados(df):
    """Processa o DataFrame para calcular percentuais e identificar disciplinas."""
    colunas_nao_disciplinas = ['ALUNO', 'TURMA', 'ESCOLA', 'PERCACERTOSALUNO', 'PERCACERTOSGERAL', 'PRESENCA']
    disciplinas = [col for col in df.columns if col not in colunas_nao_disciplinas]
    
    for col in disciplinas:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    if disciplinas:
        df['PERCACERTOSALUNO'] = df[disciplinas].mean(axis=1)
    
    return df, disciplinas

def renderizar_metricas_gerais(df, disciplina_selecionada):
    """Exibe os cards com as métricas gerais de desempenho."""
    st.markdown('<h3 class="section-title">📈 Métricas Gerais de Desempenho</h3>', unsafe_allow_html=True)
    
    dados_disciplina = df[disciplina_selecionada].dropna()
    
    media_geral = dados_disciplina.mean()
    mediana_geral = dados_disciplina.median()
    num_alunos = df.shape[0]
    aprovados = sum(dados_disciplina >= 60)
    perc_aprovados = (aprovados / num_alunos) * 100 if num_alunos > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(label=f"Média em {disciplina_selecionada}", value=f"{media_geral:.1f}%" if pd.notna(media_geral) else "N/A")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(label=f"Mediana em {disciplina_selecionada}", value=f"{mediana_geral:.1f}%" if pd.notna(mediana_geral) else "N/A")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card" style="border-left-color: #1cc88a;">', unsafe_allow_html=True)
        st.metric(label="Taxa de Desempenho Satisfatório", value=f"{perc_aprovados:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card" style="border-left-color: #36b9cc;">', unsafe_allow_html=True)
        st.metric(label="Total de Alunos", value=num_alunos)
        st.markdown('</div>', unsafe_allow_html=True)

def renderizar_graficos_distribuicao(df, disciplina_selecionada):
    """Exibe os gráficos de distribuição e ranking de alunos."""
    st.markdown('<h3 class="section-title">📊 Visualizações de Desempenho</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("##### Ranking de Alunos")
        df_ranking = df[['ALUNO', disciplina_selecionada]].sort_values(by=disciplina_selecionada, ascending=False).reset_index(drop=True)
        df_ranking.index += 1
        st.dataframe(df_ranking.style.format({disciplina_selecionada: "{:.1f}%"}), height=400, use_container_width=True)

    with col2:
        tab1, tab2 = st.tabs(["Distribuição de Notas", "Box Plot Comparativo"])
        
        with tab1:
            fig_hist = px.histogram(df, x=disciplina_selecionada, nbins=10, title=f"Distribuição em {disciplina_selecionada}", color_discrete_sequence=['#4e73df'])
            fig_hist.update_layout(bargap=0.1, template="plotly_white", showlegend=False, height=400)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with tab2:
            fig_box = px.box(df, y=disciplina_selecionada, title=f"Dispersão das Notas em {disciplina_selecionada}", color_discrete_sequence=['#4e73df'])
            fig_box.update_layout(template="plotly_white", showlegend=False, height=400)
            st.plotly_chart(fig_box, use_container_width=True)

def renderizar_analise_individual(df, disciplinas):
    """Exibe a análise detalhada por aluno com o elogiado gráfico de radar."""
    st.markdown('<h3 class="section-title">👤 Análise de Desempenho Individual</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        aluno_selecionado = st.selectbox("Selecione um Aluno:", options=df['ALUNO'].unique())
        dados_aluno = df[df['ALUNO'] == aluno_selecionado][disciplinas].iloc[0]
        media_turma = df[disciplinas].mean()
        
        st.markdown(f"##### Resumo de **{aluno_selecionado}**")
        media_aluno = dados_aluno.mean()
        st.metric("Média Geral do Aluno", f"{media_aluno:.1f}%" if pd.notna(media_aluno) else "N/A")
        
        if pd.notna(media_aluno):
            melhor_disc = dados_aluno.idxmax()
            pior_disc = dados_aluno.idxmin()
            st.markdown(f"**<span style='color: #1cc88a;'>✓ Melhor desempenho:</span>** {melhor_disc} ({dados_aluno[melhor_disc]:.1f}%)", unsafe_allow_html=True)
            st.markdown(f"**<span style='color: #e74a3b;'>! Ponto de atenção:</span>** {pior_disc} ({dados_aluno[pior_disc]:.1f}%)", unsafe_allow_html=True)

    with col2:
        fig_radar = go.Figure()
        if pd.notna(dados_aluno).all():
            fig_radar.add_trace(go.Scatterpolar(r=dados_aluno.values, theta=dados_aluno.index, fill='toself', name=aluno_selecionado, line_color='#4e73df'))
        if pd.notna(media_turma).all():
            fig_radar.add_trace(go.Scatterpolar(r=media_turma.values, theta=disciplinas, fill='toself', name='Média da Turma', line_color='rgba(231, 74, 59, 0.7)'))

        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=500, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5), title=f"Radar Comparativo: {aluno_selecionado} vs. Média da Turma")
        st.plotly_chart(fig_radar, use_container_width=True)

def renderizar_tabela_detalhada(df, disciplinas):
    """Exibe a tabela completa com formatação condicional elegante e legível."""
    st.markdown('<h3 class="section-title">📋 Dados Completos da Turma</h3>', unsafe_allow_html=True)

    def style_performance(val):
        try:
            val_num = float(val)
            if val_num >= 80:
                style = 'background-color: #e9f5ee; color: #1e663a; border-left: 5px solid #28a745; font-weight: 600;'
            elif val_num >= 60:
                style = 'background-color: #fff8e1; color: #8c6c0a; border-left: 5px solid #ffc107;'
            else:
                style = 'background-color: #fdeaea; color: #a94442; border-left: 5px solid #dc3545;'
            return style
        except (ValueError, TypeError):
            return ''

    df_display = df.copy()
    colunas_para_formatar = disciplinas + ['PERCACERTOSALUNO']
    df_display['RANKING'] = df_display['PERCACERTOSALUNO'].fillna(0).rank(ascending=False, method='min').astype(int)
    
    colunas_ordenadas = ['RANKING', 'ALUNO'] + colunas_para_formatar
    
    styler = df_display[colunas_ordenadas].sort_values('RANKING').style
    format_dict = {col: '{:.1f}%' for col in colunas_para_formatar}
    
    for col in colunas_para_formatar:
        styler = styler.apply(lambda s: s.map(style_performance), subset=[col])
        
    styler = styler.format(format_dict)
    st.dataframe(styler, use_container_width=True, height=600)

# --- Aplicação Principal ---
def main():
    with st.sidebar:
        st.markdown('<h2 style="text-align: center; color: #2c3e50;">Painel de Controle</h2>', unsafe_allow_html=True)
        turma_selecionada = st.selectbox("Selecione a Turma:", options=list(TURMAS_CONFIG.keys()))
        
        st.markdown("---")
        
        if 'pagina_atual' not in st.session_state:
            st.session_state.pagina_atual = "Visão Geral"

        if st.button("📊 Visão Geral", use_container_width=True): st.session_state.pagina_atual = "Visão Geral"
        if st.button("👤 Análise Individual", use_container_width=True): st.session_state.pagina_atual = "Análise Individual"
        if st.button("📋 Dados Completos", use_container_width=True): st.session_state.pagina_atual = "Dados Completos"
        
        st.markdown("---")
        
        arquivo_csv = TURMAS_CONFIG[turma_selecionada]["arquivo"]
        df = carregar_dados(arquivo_csv)
        
        if df is not None:
            df, disciplinas_disponiveis = processar_dados(df)
            if not disciplinas_disponiveis:
                st.warning("Nenhuma disciplina encontrada no arquivo.")
                return
            disciplina_selecionada = st.selectbox("Foco da Análise:", options=disciplinas_disponiveis)
        else:
            st.info("Aguardando carregamento dos dados.")
            return

    st.markdown(f'<h1 class="header-title">Análise de Desempenho - {turma_selecionada}</h1>', unsafe_allow_html=True)
    
    if df is not None and 'disciplina_selecionada' in locals():
        if st.session_state.pagina_atual == "Visão Geral":
            renderizar_metricas_gerais(df, disciplina_selecionada)
            renderizar_graficos_distribuicao(df, disciplina_selecionada)
        elif st.session_state.pagina_atual == "Análise Individual":
            renderizar_analise_individual(df, disciplinas_disponiveis)
        elif st.session_state.pagina_atual == "Dados Completos":
            renderizar_tabela_detalhada(df, disciplinas_disponiveis)

if __name__ == "__main__":
    main()