import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configurações da página
st.set_page_config(
    page_title="Análise PPR 7º B Ano",
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
    .header {
        background-color: #3498db;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        color: white;
    }
    .metric-card {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 15px;
        background-color: blue;
        margin-bottom: 15px;
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        background-color: #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3498db;
        color: white;
    }
    .highlight-good {
        background-color: #d4edda !important;
        color: #155724;
    }
    .highlight-bad {
        background-color: #f8d7da !important;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)


# Carregar e processar dados
@st.cache_data
def load_data():
    # Carregar dados do arquivo CSV
    df = pd.read_csv("pages/PPR_7B.csv", sep=";", decimal=",", encoding='utf-8-sig')

    # Remover linhas vazias
    df = df.dropna(how='all')

    # Corrigir nomes de colunas
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(' ', '')

    # Converter porcentagens para valores numéricos
    for col in df.columns[1:-3]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Converter colunas de média para numéricas
    df['percAcertosAluno'] = pd.to_numeric(df['percAcertosAluno'], errors='coerce')
    df['percAcertosGeral'] = pd.to_numeric(df['percAcertosGeral'], errors='coerce')

    return df


# Carregar dados
df = load_data()

# Obter lista de disciplinas disponíveis
disciplinas_disponiveis = [col for col in df.columns if
                           col not in ['ALUNO', 'percAcertosAluno', 'percAcertosGeral', 'presenca']]

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #2c3e50; font-size: 24px;">Análise PPR 7º B Ano</h1>
        <h2 style="color: #3498db; font-size: 18px;">Escola Estadual Helena Dionysio</h2>
    </div>
    """, unsafe_allow_html=True)

    # Seleção de disciplina
    disciplina_selecionada = st.selectbox(
        "Selecione a Disciplina",
        options=disciplinas_disponiveis,
        index=0
    )

    # Tipo de análise
    analise_tipo = st.radio(
        "Tipo de Análise",
        options=["Desempenho Geral", "Análise Individual"],
        index=0
    )

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p style="color: #7f8c8d; font-size: 14px;">Ferramenta de Análise Pedagógica</p>
        <p style="color: #7f8c8d; font-size: 12px;">Atualizado em Julho 2025</p>
    </div>
    """, unsafe_allow_html=True)

# Layout principal
st.markdown(f"""
<div class="header">
    <h1 style="text-align: center; margin: 0;">Análise de Desempenho - {disciplina_selecionada}</h1>
    <h2 style="text-align: center; margin: 0;">7º B Ano - PPR 2025</h2>
</div>
""", unsafe_allow_html=True)

if analise_tipo == "Desempenho Geral":
    # Seção 1: Métricas Gerais
    st.markdown("### 📊 Indicadores Gerais")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        media = float(df[disciplina_selecionada].mean())
        st.metric("Média da Turma", f"{media:.1f}%",
                  help="Média aritmética das notas da turma")

    with col2:
        mediana = float(df[disciplina_selecionada].median())
        st.metric("Mediana", f"{mediana:.1f}%",
                  help="Valor que divide a turma em duas partes iguais")

    with col3:
        desvio_padrao = float(df[disciplina_selecionada].std())
        st.metric("Desvio Padrão", f"{desvio_padrao:.1f}%",
                  help="Medida de dispersão dos dados - quanto maior, mais variados os desempenhos")

    with col4:
        aprovacao = float((df[disciplina_selecionada] >= 60).mean() * 100)
        st.metric("Taxa de Aprovação", f"{aprovacao:.1f}%",
                  help="Percentual de alunos com nota ≥ 60%")

    # Seção 2: Distribuição de Notas
    st.markdown("### 📈 Distribuição de Desempenho")

    fig_dist = px.histogram(
        df,
        x=disciplina_selecionada,
        nbins=10,
        color_discrete_sequence=['#3498db'],
        labels={disciplina_selecionada: 'Nota (%)'},
        title=f'Distribuição de Notas em {disciplina_selecionada}'
    )

    fig_dist.update_layout(
        template='plotly_white',
        bargap=0.1,
        xaxis_range=[0, 100],
        yaxis_title="Número de Alunos",
        showlegend=False
    )

    # Linhas de referência
    fig_dist.add_vline(x=60, line_dash="dot", line_color="#e74c3c",
                       annotation_text="Mínimo para Aprovação",
                       annotation_position="top right")
    fig_dist.add_vline(x=media, line_dash="dash", line_color="#2ecc71",
                       annotation_text=f"Média: {media:.1f}%",
                       annotation_position="bottom right")

    st.plotly_chart(fig_dist, use_container_width=True)

    # Seção 3: Comparação entre Disciplinas
    st.markdown("### 📚 Comparação entre Disciplinas")

    medias_disciplinas = [float(df[disc].mean()) for disc in disciplinas_disponiveis]

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=disciplinas_disponiveis,
        y=medias_disciplinas,
        marker_color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c'],
        text=[f"{m:.1f}%" for m in medias_disciplinas],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Média: %{y:.1f}%<extra></extra>'
    ))

    fig_comp.update_layout(
        template='plotly_white',
        title='Média por Disciplina',
        yaxis_title="Média de Acertos (%)",
        yaxis_range=[0, 100],
        xaxis_title="Disciplina",
        hovermode="x"
    )

    st.plotly_chart(fig_comp, use_container_width=True)

    # Seção 4: Top e Bottom Alunos
    st.markdown("### 🏆 Top 5 e 🔻 Bottom 5 Alunos")
    col_top, col_bottom = st.columns(2)

    with col_top:
        top_alunos = df.nlargest(5, disciplina_selecionada)[['ALUNO', disciplina_selecionada]]
        st.markdown("#### Melhores Desempenhos")
        fig_top = px.bar(
            top_alunos,
            x=disciplina_selecionada,
            y='ALUNO',
            orientation='h',
            color=disciplina_selecionada,
            color_continuous_scale='Blues',
            labels={disciplina_selecionada: 'Nota (%)'},
            text=disciplina_selecionada
        )
        fig_top.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='inside',
            hovertemplate='<b>%{y}</b><br>Nota: %{x:.1f}%<extra></extra>'
        )
        fig_top.update_layout(
            template='plotly_white',
            showlegend=False,
            coloraxis_showscale=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with col_bottom:
        bottom_alunos = df.nsmallest(5, disciplina_selecionada)[['ALUNO', disciplina_selecionada]]
        st.markdown("#### Desempenhos que Precisam de Atenção")
        fig_bottom = px.bar(
            bottom_alunos,
            x=disciplina_selecionada,
            y='ALUNO',
            orientation='h',
            color=disciplina_selecionada,
            color_continuous_scale='Reds_r',
            labels={disciplina_selecionada: 'Nota (%)'},
            text=disciplina_selecionada
        )
        fig_bottom.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='inside',
            hovertemplate='<b>%{y}</b><br>Nota: %{x:.1f}%<extra></extra>'
        )
        fig_bottom.update_layout(
            template='plotly_white',
            showlegend=False,
            coloraxis_showscale=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_bottom, use_container_width=True)

    # Seção 5: Correlação entre Disciplinas
    st.markdown("### 🔗 Correlação entre Disciplinas")
    corr_matrix = df[disciplinas_disponiveis].corr()

    fig_corr = go.Figure()
    fig_corr.add_trace(go.Heatmap(
        z=corr_matrix,
        x=disciplinas_disponiveis,
        y=disciplinas_disponiveis,
        colorscale='Blues',
        zmin=0,
        zmax=1,
        text=np.round(corr_matrix.values, 2),
        texttemplate="%{text}",
        hovertemplate='<b>%{y} vs %{x}</b><br>Correlação: %{z:.2f}<extra></extra>'
    ))

    fig_corr.update_layout(
        template='plotly_white',
        title='Matriz de Correlação entre Disciplinas',
        height=600,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        yaxis_autorange='reversed'
    )

    st.plotly_chart(fig_corr, use_container_width=True)

else:
    # Modo de Análise Individual
    st.markdown("### 👤 Análise Individual por Aluno")

    aluno_selecionado = st.selectbox(
        "Selecione o Aluno",
        options=df['ALUNO'].sort_values(),
        index=0
    )

    aluno_data = df[df['ALUNO'] == aluno_selecionado].iloc[0]

    # Cartões com métricas do aluno
    col1, col2, col3 = st.columns(3)

    with col1:
        nota = float(aluno_data[disciplina_selecionada])
        st.markdown(f"""
        <div class="metric-card">
            <h3>Desempenho em {disciplina_selecionada}</h3>
            <h1 style="color: {'#2ecc71' if nota >= 60 else '#e74c3c'};">
                {nota:.1f}%
            </h1>
            <p>{'✅ Acima da média' if nota >= 60 else '❌ Abaixo da média'}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        media_aluno = float(aluno_data['percAcertosAluno'])
        media_turma = float(aluno_data['percAcertosGeral'])
        st.markdown(f"""
        <div class="metric-card">
            <h3>Média Geral do Aluno</h3>
            <h1 style="color: {'#2ecc71' if media_aluno >= 60 else '#e74c3c'};">
                {media_aluno:.1f}%
            </h1>
            <p>Média da turma: {media_turma:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        disciplinas_numericas = {k: float(v) for k, v in aluno_data.items() if k in disciplinas_disponiveis}
        melhor_disciplina = max(disciplinas_numericas, key=disciplinas_numericas.get)
        pior_disciplina = min(disciplinas_numericas, key=disciplinas_numericas.get)

        st.markdown(f"""
        <div class="metric-card">
            <h3>Pontos Fortes e Fracos</h3>
            <p><span class="highlight-good">Melhor: {melhor_disciplina} ({disciplinas_numericas[melhor_disciplina]:.1f}%)</span></p>
            <p><span class="highlight-bad">Pior: {pior_disciplina} ({disciplinas_numericas[pior_disciplina]:.1f}%)</span></p>
        </div>
        """, unsafe_allow_html=True)

    # Radar plot das habilidades
    st.markdown("### 📊 Perfil Multidisciplinar")

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[float(aluno_data[disc]) for disc in disciplinas_disponiveis],
        theta=disciplinas_disponiveis,
        fill='toself',
        name=aluno_selecionado,
        line=dict(color='#3498db')
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[float(df[disc].mean()) for disc in disciplinas_disponiveis],
        theta=disciplinas_disponiveis,
        fill='toself',
        name='Média da Turma',
        line=dict(color='#e74c3c')
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        template='plotly_white',
        height=500
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Seção 6: Dados Detalhados
st.markdown("### 📋 Dados Completos da Turma")


def colorize(val):
    try:
        val_num = float(val)
        if val_num >= 80:
            color = '#d4edda'
        elif val_num >= 60:
            color = '#fff3cd'
        else:
            color = '#f8d7da'
        return f'background-color: {color}'
    except:
        return ''


def format_value(val):
    try:
        return f"{float(val):.1f}%"
    except:
        return str(val)


# Criar DataFrame para exibição
df_display = df.copy()
for col in disciplinas_disponiveis + ['percAcertosAluno']:
    df_display[col] = df_display[col].apply(format_value)

# Aplicar estilo
styled_df = df_display.sort_values(disciplina_selecionada, ascending=False)[
    ['ALUNO'] + disciplinas_disponiveis + ['percAcertosAluno']].style \
    .applymap(colorize, subset=disciplinas_disponiveis + ['percAcertosAluno'])

st.dataframe(
    styled_df,
    hide_index=True,
    use_container_width=True,
    height=600
)

# Seção 7: Exportar Relatório
st.markdown("---")
st.download_button(
    label="📥 Exportar Relatório em Excel",
    data=df.to_csv(index=False, sep=";", decimal=",").encode('utf-8'),
    file_name=f"relatorio_ppr_8ano_{disciplina_selecionada}.csv",
    mime="text/csv"
)