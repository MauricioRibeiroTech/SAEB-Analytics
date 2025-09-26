import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import scipy.stats as stats

# Configurações da página
st.set_page_config(
    page_title="Dashboard Comparativo - 9º Ano A",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para um visual mais moderno e atraente
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    .metric-card {
        border-radius: 15px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-title {
        font-size: 12px;
        color: #a8b2d1;
        margin-bottom: 5px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px 30px;
        border-radius: 12px;
        margin: 30px 0;
        border-left: 5px solid #ff6b6b;
    }
    .sidebar-info {
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        font-size: 12px;
    }
    .disciplina-destaque {
        background: linear-gradient(135deg, #ff6b6b, #feca57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def load_and_clean_data():
    """Carrega e limpa os dados dos dois arquivos CSV."""
    try:
        df_1ed = pd.read_csv('pages/PPR_9A.csv', sep=';', decimal=',', encoding='utf-8-sig')
        df_2ed = pd.read_csv('pages/PPR_9A_2ED.csv', sep=';', decimal=',', encoding='utf-8-sig')

        for df in [df_1ed, df_2ed]:
            df.columns = df.columns.str.strip()
            df.rename(columns={'ALUNO': 'Aluno', 'ALUNO ': 'Aluno'}, inplace=True)

        disciplinas = ['CIÊNCIAS', 'GEO', 'HIST', 'INGLÊS', 'PORT', 'MAT']
        
        disciplinas_1ed = [col for col in disciplinas if col in df_1ed.columns]
        disciplinas_2ed = [col for col in disciplinas if col in df_2ed.columns]

        for col in disciplinas_1ed + ['percAcertosAluno']:
            if col in df_1ed.columns:
                df_1ed[col] = pd.to_numeric(df_1ed[col].astype(str).str.replace(',', '.'), errors='coerce')
        
        for col in disciplinas_2ed + ['percAcertosAluno']:
            if col in df_2ed.columns:
                df_2ed[col] = pd.to_numeric(df_2ed[col].astype(str).str.replace(',', '.'), errors='coerce')

        return df_1ed, df_2ed, disciplinas_1ed, disciplinas_2ed

    except FileNotFoundError:
        st.error("❌ Arquivos CSV não encontrados! Certifique-se de que 'PPR_9A.csv' e 'PPR_9A_2ED.csv' estão na mesma pasta.")
        st.stop()
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os dados: {e}")
        st.stop()

def calcular_estatisticas(df_1ed, df_2ed, disciplinas_1ed, disciplinas_2ed):
    """Calcula um dicionário de estatísticas comparativas."""
    stats_dict = {}
    disciplinas_comuns = sorted(list(set(disciplinas_1ed) & set(disciplinas_2ed)))
    stats_dict['disciplinas_comuns'] = disciplinas_comuns

    stats_dict['medias_1ed'] = {disc: df_1ed[disc].mean() for disc in disciplinas_comuns}
    stats_dict['medias_2ed'] = {disc: df_2ed[disc].mean() for disc in disciplinas_comuns}
    
    stats_dict['evolucao_disciplinas'] = {
        disc: stats_dict['medias_2ed'][disc] - stats_dict['medias_1ed'][disc] 
        for disc in disciplinas_comuns
    }

    stats_dict['media_geral_1ed'] = df_1ed['percAcertosAluno'].mean()
    stats_dict['media_geral_2ed'] = df_2ed['percAcertosAluno'].mean()
    stats_dict['evolucao_geral'] = stats_dict['media_geral_2ed'] - stats_dict['media_geral_1ed']

    alunos_comuns = sorted(list(set(df_1ed['Aluno']) & set(df_2ed['Aluno'])))
    stats_dict['alunos_comuns'] = alunos_comuns

    notas_1ed, notas_2ed = [], []
    for aluno in alunos_comuns:
        notas_1ed.append(df_1ed.loc[df_1ed['Aluno'] == aluno, 'percAcertosAluno'].iloc[0])
        notas_2ed.append(df_2ed.loc[df_2ed['Aluno'] == aluno, 'percAcertosAluno'].iloc[0])

    stats_dict['alunos_melhoraram'] = sum(n2 > n1 for n1, n2 in zip(notas_1ed, notas_2ed))
    stats_dict['percent_melhoraram'] = (stats_dict['alunos_melhoraram'] / len(alunos_comuns)) * 100 if alunos_comuns else 0

    if len(notas_1ed) > 1 and len(notas_2ed) > 1:
        stats_dict['t_test'] = stats.ttest_rel(notas_1ed, notas_2ed)
        stats_dict['cohen_d'] = (np.mean(notas_2ed) - np.mean(notas_1ed)) / np.sqrt((np.std(notas_1ed, ddof=1)**2 + np.std(notas_2ed, ddof=1)**2) / 2)
    else:
        stats_dict['t_test'] = type('obj', (), {'pvalue': 1.0})
        stats_dict['cohen_d'] = 0
        
    return stats_dict

def criar_grafico_barras_comparativo(stats_dict):
    """Cria um gráfico de barras comparando as médias por disciplina."""
    disciplinas = stats_dict['disciplinas_comuns']
    df_plot = pd.DataFrame({
        'Disciplina': disciplinas,
        '1ª Edição': [stats_dict['medias_1ed'][d] for d in disciplinas],
        '2ª Edição': [stats_dict['medias_2ed'][d] for d in disciplinas],
        'Evolução': [stats_dict['evolucao_disciplinas'][d] for d in disciplinas]
    })

    fig = go.Figure()
    fig.add_trace(go.Bar(name='1ª Edição', x=df_plot['Disciplina'], y=df_plot['1ª Edição'], marker_color='#FF6B6B'))
    fig.add_trace(go.Bar(name='2ª Edição', x=df_plot['Disciplina'], y=df_plot['2ª Edição'], marker_color='#4ECDC4'))

    for i, row in df_plot.iterrows():
        evolucao = row['Evolução']
        cor_anotacao = "#10b981" if evolucao > 0 else "#ef4444"
        fig.add_annotation(
            x=row['Disciplina'], y=max(row['1ª Edição'], row['2ª Edição']) + 3,
            text=f"{evolucao:+.1f}%", showarrow=False,
            font=dict(color=cor_anotacao, size=12, weight="bold")
        )

    fig.update_layout(
        title="📊 Comparativo de Desempenho por Disciplina",
        yaxis_title="Percentual de Acerto (%)", template='plotly_dark', height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def criar_grafico_radar_turma(stats_dict, edicao):
    """Cria um gráfico de radar para o desempenho da turma em uma edição específica."""
    disciplinas = stats_dict['disciplinas_comuns']
    
    if edicao == 1:
        medias = [stats_dict['medias_1ed'][d] for d in disciplinas]
        cor_linha, cor_fill = '#FF6B6B', 'rgba(255, 107, 107, 0.4)'
        titulo = "🎯 Desempenho da Turma - 1ª Edição"
    else:
        medias = [stats_dict['medias_2ed'][d] for d in disciplinas]
        cor_linha, cor_fill = '#4ECDC4', 'rgba(78, 205, 196, 0.4)'
        titulo = "🎯 Desempenho da Turma - 2ª Edição"

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=medias, theta=disciplinas, fill='toself', name=f'{edicao}ª Edição',
        line=dict(color=cor_linha), fillcolor=cor_fill
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title=titulo, template='plotly_dark', height=450, showlegend=False
    )
    return fig

# --- NOVAS FUNÇÕES PARA GRÁFICOS INDIVIDUAIS ---
def criar_grafico_radar_individual_1ed(df_1ed, stats_dict, aluno):
    """Cria um gráfico de radar individual para a 1ª Edição."""
    disciplinas = stats_dict['disciplinas_comuns']
    aluno_scores = [df_1ed.loc[df_1ed['Aluno'] == aluno, d].iloc[0] for d in disciplinas]
    turma_scores = [stats_dict['medias_1ed'][d] for d in disciplinas]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=turma_scores, theta=disciplinas, fill='none', name='Média da Turma',
        line=dict(color='#FF6B6B', dash='dash', width=2)
    ))
    fig.add_trace(go.Scatterpolar(
        r=aluno_scores, theta=disciplinas, fill='toself', name=aluno,
        line=dict(color='#FFD700', width=3), fillcolor='rgba(255, 215, 0, 0.3)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title=f"👤 {aluno} vs. Turma - 1ª Edição",
        template='plotly_dark', height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def criar_grafico_radar_individual_2ed(df_2ed, stats_dict, aluno):
    """Cria um gráfico de radar individual para a 2ª Edição."""
    disciplinas = stats_dict['disciplinas_comuns']
    aluno_scores = [df_2ed.loc[df_2ed['Aluno'] == aluno, d].iloc[0] for d in disciplinas]
    turma_scores = [stats_dict['medias_2ed'][d] for d in disciplinas]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=turma_scores, theta=disciplinas, fill='none', name='Média da Turma',
        line=dict(color='#4ECDC4', dash='dash', width=2)
    ))
    fig.add_trace(go.Scatterpolar(
        r=aluno_scores, theta=disciplinas, fill='toself', name=aluno,
        line=dict(color='#32CD32', width=3), fillcolor='rgba(50, 205, 50, 0.3)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title=f"👤 {aluno} vs. Turma - 2ª Edição",
        template='plotly_dark', height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def criar_grafico_heatmap_evolucao(df_1ed, df_2ed, stats_dict):
    """Cria um heatmap mostrando a evolução individual por disciplina."""
    dados_heatmap = []
    for aluno in stats_dict['alunos_comuns']:
        evolucoes_aluno = [
            df_2ed.loc[df_2ed['Aluno'] == aluno, d].iloc[0] - df_1ed.loc[df_1ed['Aluno'] == aluno, d].iloc[0]
            for d in stats_dict['disciplinas_comuns']
        ]
        dados_heatmap.append(evolucoes_aluno)

    fig = px.imshow(
        dados_heatmap, x=stats_dict['disciplinas_comuns'], y=stats_dict['alunos_comuns'],
        color_continuous_scale='RdYlGn', aspect='auto',
        title="🔥 Mapa de Calor da Evolução (2ª Edição - 1ª Edição)",
        labels=dict(x="Disciplina", y="Aluno", color="Variação (%)")
    )
    fig.update_layout(template='plotly_dark', height=max(400, len(stats_dict['alunos_comuns']) * 20))
    return fig

def main():
    df_1ed, df_2ed, disciplinas_1ed, disciplinas_2ed = load_and_clean_data()
    stats_dict = calcular_estatisticas(df_1ed, df_2ed, disciplinas_1ed, disciplinas_2ed)

    # --- HEADER ---
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: white; font-weight: 700;">📈 ANÁLISE COMPARATIVA - 9º ANO A</h1>
        <p style="color: #e0f2fe; font-size: 18px;">Comparativo de Desempenho entre a 1ª e 2ª Edição da Prova Paraná</p>
    </div>
    """, unsafe_allow_html=True)

    # --- SEÇÃO 1: ÍNDICES COMPARATIVOS GERAIS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        evolucao = stats_dict['evolucao_geral']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Evolução Média da Turma</div>
            <div class="metric-value">{evolucao:+.1f}%</div>
            <div style="font-size: 11px; color: {'#10b981' if evolucao > 0 else '#ef4444'}">
                {stats_dict['media_geral_1ed']:.1f}% → {stats_dict['media_geral_2ed']:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Alunos em Evolução</div>
            <div class="metric-value">{stats_dict['alunos_melhoraram']}</div>
            <div style="font-size: 11px; color: #10b981">{stats_dict['percent_melhoraram']:.1f}% da turma</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Alunos Analisados</div>
            <div class="metric-value">{len(stats_dict['alunos_comuns'])}</div>
            <div style="font-size: 11px; color: #a8b2d1">Presentes em ambas as edições</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        cohen_d = stats_dict['cohen_d']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Tamanho do Efeito (d)</div>
            <div class="metric-value">{cohen_d:.2f}</div>
            <div style="font-size: 11px; color: {'#10b981' if abs(cohen_d) >= 0.8 else '#f59e0b'}">
                {'Grande' if abs(cohen_d) >= 0.8 else 'Médio' if abs(cohen_d) >= 0.5 else 'Pequeno'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- SEÇÃO 2: ANÁLISE GERAL DA TURMA ---
    st.markdown('<div class="section-header"><h3>Turma: Análise Geral do Desempenho</h3></div>', unsafe_allow_html=True)
    st.plotly_chart(criar_grafico_barras_comparativo(stats_dict), use_container_width=True)
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.plotly_chart(criar_grafico_radar_turma(stats_dict, edicao=1), use_container_width=True)
    with col_r2:
        st.plotly_chart(criar_grafico_radar_turma(stats_dict, edicao=2), use_container_width=True)

    # --- SEÇÃO 3: ANÁLISE INDIVIDUAL ---
    st.markdown('<div class="section-header"><h3>Aluno: Análise Individual Comparativa</h3></div>', unsafe_allow_html=True)
    aluno_selecionado = st.selectbox(
        "Selecione um aluno para uma análise detalhada:",
        options=stats_dict['alunos_comuns'],
        index=0
    )
    if aluno_selecionado:
        # Layout atualizado com os dois gráficos de radar individuais
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            st.plotly_chart(criar_grafico_radar_individual_1ed(df_1ed, stats_dict, aluno_selecionado), use_container_width=True)
        with col_i2:
            st.plotly_chart(criar_grafico_radar_individual_2ed(df_2ed, stats_dict, aluno_selecionado), use_container_width=True)

    # --- SEÇÃO 4: ANÁLISE SAEB E ESTATÍSTICA ---
    st.markdown('<div class="section-header"><h3>🔍 Análise SAEB e Veredito Estatístico</h3></div>', unsafe_allow_html=True)
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        if 'MAT' in stats_dict['disciplinas_comuns'] and 'PORT' in stats_dict['disciplinas_comuns']:
            st.markdown("#### 🎯 Desempenho nas Disciplinas Foco (SAEB)")
            evol_mat = stats_dict['evolucao_disciplinas']['MAT']
            evol_port = stats_dict['evolucao_disciplinas']['PORT']
            
            c1, c2 = st.columns(2)
            c1.metric("📐 MATEMÁTICA (2ª Ed)", f"{stats_dict['medias_2ed']['MAT']:.1f}%", f"{evol_mat:+.1f}%")
            c2.metric("📚 LÍNGUA PORTUGUESA (2ª Ed)", f"{stats_dict['medias_2ed']['PORT']:.1f}%", f"{evol_port:+.1f}%")

            if evol_mat > 0 and evol_port > 0:
                st.success("✅ **Evolução Positiva em Foco:** Ambas as disciplinas SAEB apresentaram melhora.")
            elif evol_mat > 0 or evol_port > 0:
                st.warning("⚠️ **Evolução Mista em Foco:** Apenas uma das disciplinas SAEB evoluiu positivamente.")
            else:
                st.error("❌ **Atenção ao Foco:** Ambas as disciplinas SAEB precisam de intervenção.")
    
    with col_s2:
        st.markdown("#### 🔬 Veredito Estatístico")
        p_value = stats_dict['t_test'].pvalue
        st.metric("Significância (p-value)", f"{p_value:.4f}")
        if p_value < 0.05:
            st.success("A melhora geral da turma é **estatisticamente significativa**.")
        else:
            st.warning("A variação geral da turma **não é estatisticamente significativa**.")

    # --- SEÇÃO 5: MAPA DE CALOR ---
    st.markdown('<div class="section-header"><h3>🔥 Mapa de Calor da Evolução Individual</h3></div>', unsafe_allow_html=True)
    st.info("O mapa abaixo mostra a variação de desempenho de cada aluno em cada disciplina. **Verde** significa melhora, e **vermelho** significa piora.")
    st.plotly_chart(criar_grafico_heatmap_evolucao(df_1ed, df_2ed, stats_dict), use_container_width=True)

if __name__ == "__main__":
    main()
