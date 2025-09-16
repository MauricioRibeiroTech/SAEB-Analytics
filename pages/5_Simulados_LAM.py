import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Configurações da página
st.set_page_config(
    page_title="Dashboard LAM - Análise de Simulados",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado moderno
st.markdown("""
<style>
    .main {background-color: #0f1116; color: #ffffff;}
    
    /* Cards de métricas */
    .metric-card {
        border-radius: 16px;
        padding: 20px;
        background: linear-gradient(135deg, #1e293b, #334155);
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid #334155;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
    }
    .metric-title {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 8px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #ffffff;
        margin: 10px 0;
    }
    .metric-subtitle {
        font-size: 12px;
        color: #10b981;
        font-weight: 500;
    }
    .metric-negative {
        font-size: 12px;
        color: #ef4444;
        font-weight: 500;
    }
    
    /* Cabeçalhos */
    h1, h2, h3, h4 {
        color: #ffffff;
        font-weight: 600;
    }
    .section-header {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        padding: 18px 25px;
        border-radius: 12px;
        margin: 25px 0;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
    }
    
    /* Cards de simulados */
    .simulado-card {
        background: #1e293b;
        padding: 25px;
        border-radius: 16px;
        margin: 15px 0;
        border: 1px solid #334155;
        border-left: 5px solid #2563eb;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    .simulado-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }
    
    /* Progress bars */
    .progress-container {
        background: #334155;
        height: 10px;
        border-radius: 5px;
        margin: 15px 0;
        overflow: hidden;
        position: relative;
    }
    .progress-fill {
        height: 100%;
        border-radius: 5px;
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
        position: relative;
        transition: width 1s ease-in-out;
    }
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background-image: linear-gradient(
            -45deg,
            rgba(255, 255, 255, 0.2) 25%,
            transparent 25%,
            transparent 50%,
            rgba(255, 255, 255, 0.2) 50%,
            rgba(255, 255, 255, 0.2) 75%,
            transparent 75%,
            transparent
        );
        background-size: 20px 20px;
        animation: move 1s linear infinite;
    }
    @keyframes move {
        0% { background-position: 0 0; }
        100% { background-position: 20px 20px; }
    }
    
    /* Destaques */
    .highlight-good {
        color: #10b981;
        font-weight: bold;
    }
    .highlight-bad {
        color: #ef4444;
        font-weight: bold;
    }
    
    /* Badges */
    .badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin: 5px 0;
    }
    .badge-success {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-warning {
        background: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-danger {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("pages/Simulados_ - LAM.csv")
    df.columns = ['Aluno', 'Série', 'Turma', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7']
    return df

# Definir pontuação máxima de cada simulado
MAX_SCORES = {'S1': 15, 'S2': 10, 'S3': 15, 'S4': 15, 'S5': 15, 'S6': 25, 'S7': 25}
SIMULADOS = list(MAX_SCORES.keys())
SIMULADOS_PERCENT = [f'{s}_%' for s in SIMULADOS]

# Funções auxiliares
def calcular_porcentagens(df):
    """Calcula porcentagens baseadas nas pontuações máximas"""
    df_percent = df.copy()
    for sim, max_score in MAX_SCORES.items():
        df_percent[f'{sim}_%'] = (df[sim] / max_score) * 100
    return df_percent

def calcular_estatisticas_simulados(df_percent):
    """Calcula estatísticas para cada simulado"""
    estatisticas = []
    for sim in SIMULADOS:
        coluna_percent = f'{sim}_%'
        media = df_percent[coluna_percent].mean()
        desvio = df_percent[coluna_percent].std()
        acima_60 = (df_percent[coluna_percent] >= 60).sum()
        total_alunos = len(df_percent)
        percent_acima_60 = (acima_60 / total_alunos) * 100
        
        estatisticas.append({
            'Simulado': sim,
            'Média': media,
            'Desvio_Padrao': desvio,
            'Acima_60': acima_60,
            'Percent_Acima_60': percent_acima_60,
            'Max_Score': MAX_SCORES[sim]
        })
    
    return pd.DataFrame(estatisticas)

def criar_grafico_comparativo(df_estatisticas):
    """Cria gráfico comparativo entre simulados"""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_estatisticas['Simulado'],
        y=df_estatisticas['Média'],
        name='Média (%)',
        marker_color='#3b82f6',
        text=df_estatisticas['Média'].round(1),
        textposition='auto',
        texttemplate='%{text}%',
        hovertemplate='<b>%{x}</b><br>Média: %{y:.1f}%<br>Alunos acima de 60%: %{customdata[0]}<extra></extra>',
        customdata=df_estatisticas[['Acima_60']]
    ))

    fig.add_trace(go.Scatter(
        x=df_estatisticas['Simulado'],
        y=df_estatisticas['Percent_Acima_60'],
        name='% acima de 60%',
        mode='lines+markers+text',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8, color='#10b981'),
        text=df_estatisticas['Percent_Acima_60'].round(1),
        textposition='top center',
        texttemplate='%{text}%',
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>% acima de 60%: %{y:.1f}%<extra></extra>'
    ))

    fig.update_layout(
        template='plotly_dark',
        height=500,
        title='Comparativo entre Simulados - Média vs % de Alunos acima de 60%',
        xaxis_title="Simulado",
        yaxis_title="Média de Acerto (%)",
        yaxis2=dict(
            title="% de Alunos acima de 60%",
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    fig.add_hline(y=60, line_dash="dash", line_color="#ef4444", annotation_text="Meta: 60%")
    
    return fig

def formatar_tabela(df):
    """Formata a tabela com gradientes de cores"""
    def format_table(styler):
        return (styler
            .format({
                'Média': '{:.1f}%',
                'Desvio Padrão': '{:.1f}%',
                '% Acima de 60%': '{:.1f}%'
            })
            .background_gradient(subset=['Média', '% Acima de 60%'], cmap='RdYlGn', vmin=0, vmax=100)
            .background_gradient(subset=['Desvio Padrão'], cmap='RdYlGn_r', vmin=0, vmax=30)
            .set_properties(**{
                'background-color': '#1e293b',
                'color': 'white',
                'border': '1px solid #334155'
            })
            .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#2563eb'), ('color', 'white'), ('font-weight', 'bold')]},
                {'selector': 'tr:hover', 'props': [('background-color', '#334155')]}
            ])
        )
    
    return format_table(df.style)

# Carregar e processar dados
df = load_data()
df_percent = calcular_porcentagens(df)
df_percent['Media_Geral_%'] = df_percent[SIMULADOS_PERCENT].mean(axis=1)

# Header principal
st.markdown("""
<div style="background: linear-gradient(135deg, #2563eb, #1d4ed8); padding: 35px; border-radius: 18px; margin-bottom: 35px; text-align: center; box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3);">
    <h1 style="color: white; margin: 0; font-size: 36px; font-weight: 700;">🎯 Dashboard de Desempenho - Turma LAM</h1>
    <p style="color: #e0f2fe; margin: 10px 0 0 0; font-size: 18px;">Análise detalhada dos simulados SAEB 2025 - 9º Ano</p>
</div>
""", unsafe_allow_html=True)

# SEÇÃO 1: MÉTRICAS GERAIS
st.markdown('<div class="section-header"><h3>📈 Métricas Gerais de Desempenho</h3></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    media_geral = df_percent[SIMULADOS_PERCENT].mean().mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Média Geral</div>
        <div class="metric-value">{media_geral:.1f}%</div>
        <div class="metric-subtitle">Percentual médio de acerto</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    desvio_padrao = df_percent[SIMULADOS_PERCENT].mean(axis=1).std()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Desvio Padrão</div>
        <div class="metric-value">{desvio_padrao:.1f}%</div>
        <div class="metric-subtitle">Variabilidade entre alunos</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    media_s1 = df_percent['S1_%'].mean()
    media_s6 = df_percent['S6_%'].mean()
    taxa_crescimento = ((media_s6 - media_s1) / media_s1 * 100) if media_s1 > 0 else 0
    cor = "metric-subtitle" if taxa_crescimento >= 0 else "metric-negative"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Taxa de Crescimento</div>
        <div class="metric-value">{taxa_crescimento:+.1f}%</div>
        <div class="{cor}">S1 ({media_s1:.1f}%) → S6 ({media_s6:.1f}%)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    participacao = (df[SIMULADOS] > 0).sum().sum() / (len(df) * len(SIMULADOS)) * 100
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Participação</div>
        <div class="metric-value">{participacao:.1f}%</div>
        <div class="metric-subtitle">Taxa de engajamento</div>
    </div>
    """, unsafe_allow_html=True)

# SEÇÃO 2: TOP 3 ALUNOS - VERSÃO SIMPLIFICADA
st.markdown('<div class="section-header"><h3>🏆 Top 3 Alunos - Destaques</h3></div>', unsafe_allow_html=True)

# Identificar top 3 alunos
top3_alunos = df_percent.nlargest(3, 'Media_Geral_%')

col5, col6, col7 = st.columns(3)
medalhas = ["🥇", "🥈", "🥉"]
nomes_medalhas = ["OURO", "PRATA", "BRONZE"]

for i, (idx, row) in enumerate(top3_alunos.iterrows()):
    with [col5, col6, col7][i]:
        # Calcular evolução (S1 vs S6)
        evolucao = row['S6_%'] - row['S1_%']
        evolucao_texto = f"{evolucao:+.1f}%"
        
        # Encontrar melhor e pior simulado
        desempenhos = [row[f'{s}_%'] for s in SIMULADOS]
        melhor_sim = SIMULADOS[np.argmax(desempenhos)]
        pior_sim = SIMULADOS[np.argmin(desempenhos)]
        melhor_nota = max(desempenhos)
        pior_nota = min(desempenhos)
        
        # Card simplificado usando st.metric e st.progress
        st.markdown(f"### {medalhas[i]} {row['Aluno']}")
        st.markdown(f"**{nomes_medalhas[i]} • Média Geral: {row['Media_Geral_%']:.1f}%**")
        
        # Barra de progresso
        st.progress(row['Media_Geral_%'] / 100)
        
        # Melhor e pior desempenho
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("⭐ MELHOR", f"{melhor_sim}: {melhor_nota:.1f}%")
        with col_b:
            st.metric("📉 DESAFIO", f"{pior_sim}: {pior_nota:.1f}%")
        
        # Evolução
        st.metric("📈 Evolução S1→S6", evolucao_texto, 
                 delta_color="normal" if evolucao >= 0 else "inverse")
        
        st.markdown("---")

# SEÇÃO 3: ANÁLISE DETALHADA POR SIMULADO
st.markdown('<div class="section-header"><h3>🔍 Análise Detalhada por Simulado</h3></div>', unsafe_allow_html=True)

# Calcular estatísticas para cada simulado
df_estatisticas = calcular_estatisticas_simulados(df_percent)

# Gráfico comparativo entre simulados
fig_comparativo_simulados = criar_grafico_comparativo(df_estatisticas)
st.plotly_chart(fig_comparativo_simulados, use_container_width=True)

# Identificar simulados com melhor e pior desempenho
melhor_simulado = df_estatisticas.loc[df_estatisticas['Média'].idxmax()]
pior_simulado = df_estatisticas.loc[df_estatisticas['Média'].idxmin()]
melhor_participacao = df_estatisticas.loc[df_estatisticas['Percent_Acima_60'].idxmax()]

col8, col9, col10 = st.columns(3)

with col8:
    st.markdown(f"""
    <div class="simulado-card">
        <h4>🎯 Melhor Desempenho</h4>
        <div style="font-size: 28px; font-weight: bold; color: #10b981; margin: 10px 0;">{melhor_simulado['Simulado']}</div>
        <div class="badge badge-success">Média: {melhor_simulado['Média']:.1f}%</div>
        <div style="margin: 15px 0;">
            <span>{melhor_simulado['Acima_60']} alunos acima de 60%</span><br>
            <span>({melhor_simulado['Percent_Acima_60']:.1f}% da turma)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col9:
    st.markdown(f"""
    <div class="simulado-card">
        <h4>⚠️ Maior Desafio</h4>
        <div style="font-size: 28px; font-weight: bold; color: #ef4444; margin: 10px 0;">{pior_simulado['Simulado']}</div>
        <div class="badge badge-danger">Média: {pior_simulado['Média']:.1f}%</div>
        <div style="margin: 15px 0;">
            <span>{pior_simulado['Acima_60']} alunos acima de 60%</span><br>
            <span>({pior_simulado['Percent_Acima_60']:.1f}% da turma)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col10:
    st.markdown(f"""
    <div class="simulado-card">
        <h4>⭐ Maior Sucesso</h4>
        <div style="font-size: 28px; font-weight: bold; color: #f59e0b; margin: 10px 0;">{melhor_participacao['Simulado']}</div>
        <div class="badge badge-warning">{melhor_participacao['Percent_Acima_60']:.1f}% acima de 60%</div>
        <div style="margin: 15px 0;">
            <span>{melhor_participacao['Acima_60']} alunos atingiram a meta</span><br>
            <span>Média: {melhor_participacao['Média']:.1f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tabela detalhada por simulado
st.markdown("### 📋 Estatísticas Detalhadas por Simulado")

df_display = df_estatisticas.copy()
df_display = df_display[['Simulado', 'Max_Score', 'Média', 'Desvio_Padrao', 'Acima_60', 'Percent_Acima_60']]
df_display.columns = ['Simulado', 'Pontuação Máx', 'Média', 'Desvio Padrão', 'Acima de 60%', '% Acima de 60%']

st.dataframe(
    formatar_tabela(df_display),
    use_container_width=True,
    height=300
)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 14px;">
    <p>Escola Estadual Helena Dionysio - Recomposição da Aprendizagem - Plano de Ação</p>
    <p>© 2025 HD Analytic - Todos os direitos reservados</p>
</div>
""", unsafe_allow_html=True)
