import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------
# CONFIGURAÇÃO DE PÁGINA E CSS (Mistura de estilos)
# ---------------------------------------------

# Configurações da página (Mantidas as configurações de layout e expansão)
st.set_page_config(
    page_title="CESB Analytic - Prova Paraná", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado (Combinando o estilo escuro do corpo principal com o estilo da sidebar do arquivo anexado)
st.markdown("""
<style>
    /* Estilo do Corpo Principal (Mantido do pedido anterior) */
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    
    /* Estilo para a Sidebar (Extraído do 🏠_Página_Principal.py) */
    /* Garante que o conteúdo da sidebar tenha fundo branco */
    .sidebar .sidebar-content, .st-emotion-cache-vk3ypz {
        background-color: #ffffff;
    }
    
    /* Garante que os títulos na sidebar sejam azuis (do arquivo anexado) */
    .st-emotion-cache-1ftmdp5 h1, .st-emotion-cache-1ftmdp5 h2, .st-emotion-cache-1ftmdp5 h3 {
        color: #1E40AF;
    }

    /* Estilos do Conteúdo Principal */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px 30px;
        border-radius: 12px;
        margin: 30px 0;
        border-left: 5px solid #ff6b6b;
    }
    /* Cores gerais do texto */
    h1, h2, h3, h4, h5, h6 {
        color: white; /* Garante que os títulos no corpo principal fiquem brancos */
    }
</style>
""", unsafe_allow_html=True)


# --------------------------
# SIDEBAR (Implementação IDÊNTICA ao arquivo anexado)
# --------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 24px;">CESB Analytic</h1>
        <h2 style="font-size: 18px;">Decifrando Potenciais, Transformando Aprendizagens</h2>
    </div>
    """, unsafe_allow_html=True)
  
    # Separador e Informações
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p style="font-size: 14px; color: black;">Colégio Estadual São Braz</p>
        <p style="font-size: 12px; color: black;">Recomposição da Aprendizagem</p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------
# HEADER PRINCIPAL (Ajustado para o tema escuro)
# --------------------------
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h1 style="color: white; font-weight: 700;">📊 ANÁLISE COMPARATIVA PROVA PARANÁ</h1>
    <p style="color: #e0f2fe; font-size: 18px;">Comparativo entre a 1ª e 2ª Edição</p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")


# Lista dos arquivos CSV
arquivos_csv = {
    '9A_1ED': '9A_1ED.csv', '9A_2ED': '9A_2ED.csv',
    '9B_1ED': '9B_1ED.csv', '9B_2ED': '9B_2ED.csv',
    '3A_1ED': '3A_1ED.csv', '3A_2ED': '3A_2ED.csv',
    '3B_1ED': '3B_1ED.csv', '3B_2ED': '3B_2ED.csv',
    '3C_1ED': '3C_1ED.csv', '3C_2ED': '3C_2ED.csv',
}

# Nomes padronizados para as colunas
COLUNA_ALUNO = 'nomeAluno'
COLUNA_CGM = 'cgm'

# Função para carregar e limpar os dados (Tratamento de NaN/Vazios com 0.0)
@st.cache_data
def carregar_e_limpar_dados(caminho_arquivo):
    """Carrega o CSV, padroniza as colunas de percentual, trata NaN e converte vírgula para ponto."""
    try:
        df = pd.read_csv(caminho_arquivo, sep=';', decimal=',')
        
        colunas_para_ignorar = {COLUNA_ALUNO, COLUNA_CGM, 'percAcertosAluno', 'percAcertosGeral', 'presenca'}
        colunas_percentual = [col for col in df.columns if col not in colunas_para_ignorar]
        
        for col in colunas_percentual:
            if df[col].dtype == 'object':
                 df[col] = df[col].str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # CORREÇÃO DE VAZIOS: Preenche NaN com 0.0
        df[colunas_percentual] = df[colunas_percentual].fillna(0.0)
        
        return df, colunas_percentual
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {caminho_arquivo}")
        return None, None
    except Exception as e:
        st.error(f"Erro ao processar o arquivo {caminho_arquivo}: {e}")
        return None, None

# Função para preparar os dados para o gráfico de barras (comparação por turma)
def preparar_dados_turma(df_1ed, df_2ed, turma):
    """Calcula a média de acertos por disciplina comum e prepara o DataFrame para o gráfico de barras."""
    if df_1ed is None or df_2ed is None:
        return None
    
    colunas_identificacao = {COLUNA_ALUNO, COLUNA_CGM, 'percAcertosAluno', 'percAcertosGeral', 'presenca'}
    disciplinas_1ed = set(df_1ed.columns) - colunas_identificacao
    disciplinas_2ed = set(df_2ed.columns) - colunas_identificacao
    disciplinas_comuns = sorted(list(disciplinas_1ed.intersection(disciplinas_2ed)))
    
    if not disciplinas_comuns:
        return None

    medias_1ed = df_1ed[disciplinas_comuns].mean().reset_index()
    medias_1ed.columns = ['Disciplina', 'Média de Acertos']
    medias_1ed['Edição'] = '1ª Edição'
    
    medias_2ed = df_2ed[disciplinas_comuns].mean().reset_index()
    medias_2ed.columns = ['Disciplina', 'Média de Acertos']
    medias_2ed['Edição'] = '2ª Edição'
    
    df_comparativo = pd.concat([medias_1ed, medias_2ed])
    df_comparativo['Turma'] = turma
    
    return df_comparativo

# Função para preparar os dados do aluno e da turma para o Radar
def preparar_dados_aluno_e_turma(df_1ed, df_2ed, nome_aluno):
    """Filtra os dados de um aluno e retorna os dados para os Radars (Aluno e Média da Turma)."""
    
    colunas_identificacao = {COLUNA_ALUNO, COLUNA_CGM, 'percAcertosAluno', 'percAcertosGeral', 'presenca'}
    disciplinas_1ed = set(df_1ed.columns) - colunas_identificacao
    disciplinas_2ed = set(df_2ed.columns) - colunas_identificacao
    disciplinas_comuns = sorted(list(disciplinas_1ed.intersection(disciplinas_2ed)))
    
    if not disciplinas_comuns:
        return None, None, None, None, None
        
    aluno_1ed = df_1ed[df_1ed[COLUNA_ALUNO] == nome_aluno].iloc[0]
    aluno_2ed = df_2ed[df_2ed[COLUNA_ALUNO] == nome_aluno].iloc[0]
    valores_aluno_1ed = aluno_1ed[disciplinas_comuns].tolist()
    valores_aluno_2ed = aluno_2ed[disciplinas_comuns].tolist()

    medias_turma_1ed = df_1ed[disciplinas_comuns].mean().tolist()
    medias_turma_2ed = df_2ed[disciplinas_comuns].mean().tolist()
    
    return (disciplinas_comuns, valores_aluno_1ed, valores_aluno_2ed, 
            medias_turma_1ed, medias_turma_2ed)

# Função para criar o gráfico de Radar (separado para cada edição)
def criar_grafico_radar(disciplinas, valores_aluno, medias_turma, edicao, aluno, turma):
    """Cria e retorna um objeto Plotly Figure para o Radar de uma única edição."""
    fig_radar = go.Figure()
    
    # Aluno (Linha Sólida - Vermelha)
    fig_radar.add_trace(go.Scatterpolar(
        r=valores_aluno,
        theta=disciplinas,
        fill='toself',
        name=f'Aluno - {aluno}',
        line=dict(color='red', width=3)
    ))

    # Média da Turma (Linha Tracejada - Ciano/Azul Claro)
    fig_radar.add_trace(go.Scatterpolar(
        r=medias_turma,
        theta=disciplinas,
        name=f'Média da Turma',
        line=dict(color='cyan', dash='dash', width=2)
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=np.arange(0, 101, 20),
                ticktext=[f'{i}%' for i in np.arange(0, 101, 20)],
            )),
        showlegend=True,
        title=f"**{edicao}** | Desempenho de {aluno} vs. Média da Turma {turma}",
        height=550,
        template='plotly_dark' # Aplica o tema escuro ao gráfico
    )
    return fig_radar

# Processamento de dados de todas as turmas
turmas_9 = ['9A', '9B']
turmas_3 = ['3A', '3B', '3C']
dados_turmas = {} 

for turma in turmas_9 + turmas_3:
    arquivo_1ed = arquivos_csv.get(f'{turma}_1ED')
    arquivo_2ed = arquivos_csv.get(f'{turma}_2ED')
    
    df_1ed, _ = carregar_e_limpar_dados(arquivo_1ed)
    df_2ed, _ = carregar_e_limpar_dados(arquivo_2ed)
    
    if df_1ed is not None and df_2ed is not None:
        dados_turmas[turma] = (df_1ed, df_2ed)


# --- SEÇÃO 1: COMPARATIVO POR TURMA (GRÁFICO DE BARRAS) ---
st.markdown('<div class="section-header"><h3>1. Comparativo de Médias por Turma (1ª Edição vs 2ª Edição)</h3></div>', unsafe_allow_html=True)
st.markdown("O gráfico de barras mostra a média de acertos de cada disciplina, comparando as duas edições da prova. A análise é feita apenas sobre as **disciplinas comuns** a ambas as edições.")

# 9º Ano
st.markdown("#### Turmas do 9º Ano (Ensino Fundamental)")
df_turmas_9_list = [preparar_dados_turma(dados_turmas[t][0], dados_turmas[t][1], t) for t in turmas_9 if t in dados_turmas and dados_turmas[t] is not None]

if df_turmas_9_list and all(df is not None for df in df_turmas_9_list):
    df_comparativo_9 = pd.concat(df_turmas_9_list).sort_values(by=['Turma', 'Disciplina'])
    
    fig_9 = px.bar(df_comparativo_9, x="Disciplina", y="Média de Acertos", color="Edição", facet_col="Turma", barmode="group",
                   category_orders={"Edição": ["1ª Edição", "2ª Edição"]}, text_auto=".2f", labels={"Média de Acertos": "Média de Acertos (%)"}, height=500)
    fig_9.update_yaxes(range=[0, 100], title_text="Média de Acertos (%)")
    fig_9.update_layout(template='plotly_dark')
    st.plotly_chart(fig_9, use_container_width=True)
else:
    st.warning("Dados incompletos ou disciplinas não-comuns suficientes para a comparação das turmas do 9º ano.")


# 3º Ano
st.markdown("#### Turmas do 3º Ano (Ensino Médio)")
df_turmas_3_list = [preparar_dados_turma(dados_turmas[t][0], dados_turmas[t][1], t) for t in turmas_3 if t in dados_turmas and dados_turmas[t] is not None]

if df_turmas_3_list and all(df is not None for df in df_turmas_3_list):
    df_comparativo_3 = pd.concat(df_turmas_3_list).sort_values(by=['Turma', 'Disciplina'])
    
    fig_3 = px.bar(df_comparativo_3, x="Disciplina", y="Média de Acertos", color="Edição", facet_col="Turma", barmode="group",
                   category_orders={"Edição": ["1ª Edição", "2ª Edição"]}, text_auto=".2f", labels={"Média de Acertos": "Média de Acertos (%)"}, height=500)
    fig_3.update_yaxes(range=[0, 100], title_text="Média de Acertos (%)")
    fig_3.update_layout(template='plotly_dark')
    st.plotly_chart(fig_3, use_container_width=True)
else:
    st.warning("Dados incompletos ou disciplinas não-comuns suficientes para a comparação das turmas do 3º ano.")

st.markdown("---")


# --- SEÇÃO 2: EVOLUÇÃO INDIVIDUAL POR ALUNO (GRÁFICOS DE RADAR SEPARADOS) ---
st.markdown('<div class="section-header"><h3>2. Comparativo Aluno vs. Média da Turma (Gráficos de Radar por Edição)</h3></div>', unsafe_allow_html=True)
st.markdown("Os gráficos de radar mostram o percentual de acertos de um aluno selecionado em comparação com a média da turma, em cada edição separadamente.")

# Seleção de Turma 
todas_as_turmas = sorted(list(dados_turmas.keys()))
turma_selecionada = st.selectbox("Selecione a Turma para Análise Individual", todas_as_turmas)

if turma_selecionada:
    df1, df2 = dados_turmas[turma_selecionada]
    alunos_comuns = sorted(list(set(df1[COLUNA_ALUNO]).intersection(set(df2[COLUNA_ALUNO]))))
    
    if alunos_comuns:
        # Seleção do Aluno
        aluno_selecionado = st.selectbox(f"Selecione o Aluno da Turma {turma_selecionada}", alunos_comuns)
        
        # Prepara os dados do aluno e da turma
        disciplinas_radar, valores_aluno_1ed, valores_aluno_2ed, medias_turma_1ed, medias_turma_2ed = (
            preparar_dados_aluno_e_turma(df1, df2, aluno_selecionado)
        )
        
        if disciplinas_radar:
            
            # Divide o espaço em duas colunas para os gráficos de radar
            col1, col2 = st.columns(2)
            
            # GRÁFICO DE RADAR - 1ª EDIÇÃO
            with col1:
                fig_radar_1ed = criar_grafico_radar(
                    disciplinas_radar, valores_aluno_1ed, medias_turma_1ed, 
                    "1ª EDIÇÃO (1ED)", aluno_selecionado, turma_selecionada
                )
                st.plotly_chart(fig_radar_1ed, use_container_width=True)

            # GRÁFICO DE RADAR - 2ª EDIÇÃO
            with col2:
                fig_radar_2ed = criar_grafico_radar(
                    disciplinas_radar, valores_aluno_2ed, medias_turma_2ed, 
                    "2ª EDIÇÃO (2ED)", aluno_selecionado, turma_selecionada
                )
                st.plotly_chart(fig_radar_2ed, use_container_width=True)
            
            st.markdown(f"**Legenda dos Gráficos de Radar:**")
            st.markdown("- Linha **sólida vermelha**: Desempenho Individual do Aluno.")
            st.markdown("- Linha **tracejada ciano**: Média de Acertos da Turma.")

        else:
            st.warning(f"Não foi possível gerar os gráficos de radar para o aluno {aluno_selecionado}. Verifique se há disciplinas comuns nas duas edições.")
    else:
        st.warning(f"Não há alunos em comum nas 1ª e 2ª edições da turma {turma_selecionada} para análise de evolução.")

# Fim da Aplicação
st.markdown("---")
st.success("Análise estatística comparativa concluída.")
