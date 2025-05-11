import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configurações da página com estilo moderno
st.set_page_config(
    page_title="SAEB Analytics",
    page_icon=":book:",
    layout="wide",
    initial_sidebar_state="expanded"
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        background-color: gray;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3498db;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# Função para calcular porcentagens
def calcular_porcentagens(df, disciplina):
    if disciplina == "Matemática":
        divisores = {1: 10, 2: 10, 3: 12, 4: 15, 5: 18, 6: 18, 7: 20, 8: 16, 9: 26}
    else:  # Português
        divisores = {1: 10, 2: 10, 3: 10, 4: 15, 5: 18, 6: 18, 7: 14, 8: 16, 9: 26}

    for i in range(1, 10):
        df[f'Porcentagem Simulado {i}'] = (df[f'Sim{i}'] / divisores[i]) * 100
    return df


# Sidebar moderna
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #2c3e50; font-size: 24px;">Relatório Parcial SAEB 2025</h1>
        <h2 style="color: #3498db; font-size: 18px;">Escola Estadual Helena Dionysio</h2>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("main.py", label="🏠 Página Inicial")
    st.page_link("pages/3-Relatorios Mensais.py", label="📅 Relatório Mensal")
    st.page_link("pages/2-SAEB Descritores.py", label="📊 Relatório SAEB Descritores")
    st.page_link("pages/1-SAEB Metodologia.py", label="📈 Desempenho percentual")

    # Carregar dados
    df = pd.read_csv("pages/Dados_simples_simulados.csv", sep=",")

    # Seleção de componente
    componente_selecionada = st.selectbox("Componente Curricular", ["Matemática", "Português"])
    df = df[df["Componente"] == componente_selecionada]

    # Professor responsável
    with st.container():
        st.markdown("### Professor Responsável")
        if componente_selecionada == "Matemática":
            st.markdown("👨‍🏫 **Mauricio A. Ribeiro**")
        else:
            st.markdown("👩‍🏫 **Mikela**")

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p style="color: #7f8c8d; font-size: 14px;">Desenvolvido por Mauricio A. Ribeiro</p>
        <p style="color: #7f8c8d; font-size: 12px;">mau.ap.ribeiro@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

# Processamento dos dados
df = calcular_porcentagens(df, componente_selecionada)
simulados = [f'Porcentagem Simulado {i}' for i in range(1, 10)]

# Layout principal com cabeçalho destacado
st.markdown(f"""
<div style="background-color: #3498db; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
    <h1 style="text-align: center; margin: 0;">Relatório de {componente_selecionada}</h1>
    <h2 style="text-align: center; margin: 0;">Análise de Desempenho nos Simulados</h2>
</div>
""", unsafe_allow_html=True)

## Seção 1: Visão Geral em Cards
st.markdown("### 📊 Visão Geral do Desempenho")

# Criar métricas em colunas
col1, col2, col3 = st.columns(3)
media_geral = df[simulados].mean().mean().round(2)
melhor_simulado = df[simulados].mean().idxmax().replace('Porcentagem Simulado ', 'Simulado ')
pior_simulado = df[simulados].mean().idxmin().replace('Porcentagem Simulado ', 'Simulado ')

with col1:
    st.metric(
        "Média Geral",
        f"{media_geral}%",
        help="Média de todos os simulados"
    )

with col2:
    st.metric(
        "Melhor Simulado",
        melhor_simulado,
        help="Simulado com maior média de acertos"
    )

with col3:
    st.metric(
        "Maior Desafio",
        pior_simulado,
        help="Simulado com menor média de acertos"
    )

## Seção 2: Gráfico de Evolução Aprimorado
st.markdown("### 📈 Evolução do Desempenho Médio")

# Preparar dados para o gráfico
medias_simulados = df[simulados].mean().reset_index()
medias_simulados.columns = ['Simulado', 'Porcentagem']
medias_simulados['Simulado'] = medias_simulados['Simulado'].str.replace('Porcentagem Simulado ', '')

# Criar figura com Plotly
fig1 = go.Figure()

# Adicionar linha principal
fig1.add_trace(go.Scatter(
    x=medias_simulados['Simulado'],
    y=medias_simulados['Porcentagem'],
    mode='lines+markers+text',
    name='Média de Acertos',
    line=dict(color='#3498db', width=3),
    marker=dict(size=10, color='#3498db'),
    text=medias_simulados['Porcentagem'].round(1),
    textposition="top center",
    texttemplate='%{text}%',
    hovertemplate='Simulado %{x}<br>Média: %{y:.1f}%'
))

# Adicionar área sombreada
fig1.add_trace(go.Scatter(
    x=medias_simulados['Simulado'],
    y=medias_simulados['Porcentagem'],
    fill='tozeroy',
    fillcolor='rgba(52, 152, 219, 0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo='skip',
    showlegend=False
))

# Linha de referência (meta de 60%)
fig1.add_hline(y=60, line_dash="dot",
               annotation_text="Meta: 60%",
               annotation_position="bottom right",
               line_color="#e74c3c")

# Layout do gráfico
fig1.update_layout(
    template='plotly_white',
    height=500,
    xaxis_title="Simulado",
    yaxis_title="Porcentagem de Acertos (%)",
    yaxis_range=[0, 100],
    hovermode="x unified",
    showlegend=False,
    margin=dict(l=40, r=40, t=40, b=40)
)

st.plotly_chart(fig1, use_container_width=True)

## Seção 3: Mapa de Calor Interativo
st.markdown("### 👥 Desempenho Individual por Simulado")

# Gráfico de heatmap aprimorado
df_melted = df.melt(id_vars=['Aluno'],
                    value_vars=simulados,
                    var_name='Simulado',
                    value_name='Porcentagem')

df_melted['Simulado'] = df_melted['Simulado'].str.replace('Porcentagem Simulado ', '')

fig2 = px.density_heatmap(
    df_melted,
    x='Simulado',
    y='Aluno',
    z='Porcentagem',
    color_continuous_scale='Viridis',
    template='plotly_white',
    labels={'Porcentagem': 'Acertos (%)'},
    height=600
)

# Adicionar anotações para valores
fig2.update_traces(
    hovertemplate="<b>%{y}</b><br>Simulado %{x}<br>%{z:.1f}%<extra></extra>",
    showscale=True
)

fig2.update_layout(
    xaxis_title="Simulado",
    yaxis_title="Aluno",
    yaxis={'categoryorder': 'total ascending'},
    coloraxis_colorbar=dict(title="% Acertos")
)

st.plotly_chart(fig2, use_container_width=True)

## Seção 4: Top Alunos com Gráfico de Medalhas
st.markdown("### 🏆 Top 5 Alunos")

# Calcular média por aluno
df['Média Aluno'] = df[simulados].mean(axis=1)
top_alunos = df.nlargest(5, 'Média Aluno')[['Aluno', 'Média Aluno']].round(2)

# Criar gráfico de medalhas
fig3 = go.Figure()

fig3.add_trace(go.Bar(
    x=top_alunos['Média Aluno'],
    y=top_alunos['Aluno'],
    orientation='h',
    marker=dict(
        color=['#FFD700', '#C0C0C0', '#CD7F32', '#A8A8A8', '#8B4513'],
        line=dict(color='rgba(0,0,0,0.5)', width=1)
    ),
    text=top_alunos['Média Aluno'],
    textposition='inside',
    texttemplate='%{text}%',
    hovertemplate='<b>%{y}</b><br>Média: %{x:.1f}%<extra></extra>'
))

fig3.update_layout(
    template='plotly_white',
    height=400,
    xaxis_title="Média de Acertos (%)",
    yaxis_title="Aluno",
    yaxis={'categoryorder': 'total ascending'},
    showlegend=False,
    margin=dict(l=100, r=40, t=40, b=40)
)

st.plotly_chart(fig3, use_container_width=True)

## Seção 5: Alunos acima de 60% em Abas Estilizadas
st.markdown("### ✅ Alunos com Desempenho Acima de 60%")

# Criar abas para cada simulado
tabs = st.tabs([f"Simulado {i}" for i in range(1, 10)])

for i, tab in enumerate(tabs, start=1):
    with tab:
        col_sim, col_graph = st.columns([1, 2])

        # Filtro para alunos acima de 60%
        sim_col = f'Porcentagem Simulado {i}'
        df_filtrado = df[df[sim_col] >= 60].sort_values(sim_col, ascending=False)

        # Tabela estilizada
        with col_sim:
            st.dataframe(
                df_filtrado[['Aluno', sim_col]].style
                .background_gradient(cmap='Blues', subset=[sim_col])
                .format({sim_col: "{:.1f}%"}),
                height=400,
                use_container_width=True
            )

        # Gráfico de barras
        with col_graph:
            if not df_filtrado.empty:
                fig = px.bar(
                    df_filtrado,
                    y='Aluno',
                    x=sim_col,
                    orientation='h',
                    title=f'Desempenho no Simulado {i}',
                    color=sim_col,
                    color_continuous_scale='Blues',
                    labels={sim_col: 'Porcentagem de Acertos (%)'},
                    height=400
                )

                fig.update_layout(
                    template='plotly_white',
                    yaxis={'categoryorder': 'total ascending'},
                    showlegend=False,
                    coloraxis_showscale=False
                )

                fig.update_traces(
                    hovertemplate='<b>%{y}</b><br>%{x:.1f}%<extra></extra>',
                    texttemplate='%{x:.1f}%',
                    textposition='inside'
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"Nenhum aluno atingiu 60% no Simulado {i}", icon="⚠️")

## Seção 6: Comparação entre Componentes (se disponível)
if 'Componente' in df.columns and len(df['Componente'].unique()) > 1:
    st.markdown("### 📚 Comparação entre Componentes")

    fig_comp = px.box(
        df,
        x='Componente',
        y=simulados[0],
        color='Componente',
        points="all",
        template='plotly_white',
        labels={simulados[0]: 'Porcentagem de Acertos (%)'},
        height=500
    )

    fig_comp.update_layout(
        xaxis_title="Componente Curricular",
        showlegend=False
    )

    st.plotly_chart(fig_comp, use_container_width=True)
