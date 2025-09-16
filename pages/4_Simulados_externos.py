import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

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

# Função para processar os dados do CSV
def processar_dados(df):
    # Renomear colunas para padronização
    df.columns = ['Aluno', 'SAEB ACERTA BRASIL', 'CAEd 1', 'CAEd 2']
    
    # Converter vírgulas para pontos e transformar em float
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
    
    return df

# Sidebar moderna
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #2c3e50; font-size: 24px;">Relatório Parcial SAEB 2025</h1>
        <h2 style="color: #3498db; font-size: 18px;">Escola Estadual Helena Dionysio</h2>
    </div>
    """, unsafe_allow_html=True)

    #st.page_link("main.py", label="🏠 Página Inicial")
    #st.page_link("pages/3_Relatorios_Mensais.py", label="📅 Relatório Mensal")
    #st.page_link("pages/2_SAEB_Descritores.py", label="📊 Relatório SAEB Descritores")
    #st.page_link("pages/1_SAEB_Metodologia.py", label="📈 Desempenho percentual")

    # Carregar dados
    df = pd.read_csv("pages/Simulados_ - CAED-.csv", sep=",")
    
    # Processar dados
    df = processar_dados(df)
    
    # Seleção de componente
    componente_selecionada = st.selectbox("Componente Curricular", ["Matemática", "Português"])
    
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

# Layout principal com cabeçalho destacado
st.markdown(f"""
<div style="background-color: #3498db; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
    <h1 style="text-align: center; margin: 0;">Desemppenho nos </h1>
    <h2 style="text-align: center; margin: 0;">Simulados Externos</h2>
</div>
""", unsafe_allow_html=True)

## Seção 1: Visão Geral em Cards
st.markdown("### 📊 Visão Geral do Desempenho")

# Criar métricas em colunas
col1, col2, col3, col4 = st.columns(4)

# Calcular estatísticas
simulados = ['SAEB ACERTA BRASIL', 'CAEd 1', 'CAEd 2']
medias = df[simulados].mean()
media_geral = medias.mean().round(1)
melhor_simulado = medias.idxmax()
pior_simulado = medias.idxmin()
evolucao = (df['CAEd 2'].mean() - df['SAEB ACERTA BRASIL'].mean()).round(1)

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

with col4:
    st.metric(
        "Evolução",
        f"{evolucao}%",
        help="Diferença entre primeiro e último simulado"
    )

## Seção 2: Gráfico de Evolução Aprimorado
st.markdown("### 📈 Evolução do Desempenho Médio")

# Preparar dados para o gráfico
medias_simulados = df[simulados].mean().reset_index()
medias_simulados.columns = ['Simulado', 'Porcentagem']

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
    hovertemplate='%{x}<br>Média: %{y:.1f}%'
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
    hovertemplate="<b>%{y}</b><br>%{x}<br>%{z:.1f}%<extra></extra>",
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
tabs = st.tabs(simulados)

for sim, tab in zip(simulados, tabs):
    with tab:
        col_sim, col_graph = st.columns([1, 2])

        # Filtro para alunos acima de 60%
        df_filtrado = df[df[sim] >= 60].sort_values(sim, ascending=False)

        # Tabela estilizada
        with col_sim:
            st.dataframe(
                df_filtrado[['Aluno', sim]].style
                .background_gradient(cmap='Blues', subset=[sim])
                .format({sim: "{:.1f}%"}),
                height=400,
                use_container_width=True
            )

        # Gráfico de barras
        with col_graph:
            if not df_filtrado.empty:
                fig = px.bar(
                    df_filtrado,
                    y='Aluno',
                    x=sim,
                    orientation='h',
                    title=f'Desempenho no {sim}',
                    color=sim,
                    color_continuous_scale='Blues',
                    labels={sim: 'Porcentagem de Acertos (%)'},
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
                st.warning(f"Nenhum aluno atingiu 60% no {sim}", icon="⚠️")

## Seção 6: Análise de Evolução Individual
st.markdown("### 📊 Evolução Individual dos Alunos")

# Selecionar alunos para análise
alunos_selecionados = st.multiselect(
    "Selecione os alunos para análise detalhada:",
    options=df['Aluno'].unique(),
    default=df.nlargest(3, 'Média Aluno')['Aluno'].tolist()
)

if alunos_selecionados:
    df_selecionados = df[df['Aluno'].isin(alunos_selecionados)]
    df_melted_selecionados = df_selecionados.melt(
        id_vars=['Aluno'], 
        value_vars=simulados, 
        var_name='Simulado', 
        value_name='Porcentagem'
    )
    
    fig_evolucao = px.line(
        df_melted_selecionados,
        x='Simulado',
        y='Porcentagem',
        color='Aluno',
        markers=True,
        title='Evolução Individual por Simulado',
        template='plotly_white'
    )
    
    fig_evolucao.update_layout(
        height=500,
        yaxis_title="Porcentagem de Acertos (%)",
        yaxis_range=[0, 100]
    )
    
    st.plotly_chart(fig_evolucao, use_container_width=True)
else:
    st.info("Selecione pelo menos um aluno para visualizar a evolução individual.")

## Seção 7: Estatísticas Descritivas
st.markdown("### 📋 Estatísticas Descritivas")

# Calcular estatísticas para cada simulado
estatisticas = pd.DataFrame()
for sim in simulados:
    estatisticas[sim] = [
        df[sim].min().round(2),
        df[sim].max().round(2),
        df[sim].mean().round(2),
        df[sim].median().round(2),
        df[sim].std().round(2)
    ]

estatisticas.index = ['Mínimo', 'Máximo', 'Média', 'Mediana', 'Desvio Padrão']

# Exibir tabela
st.dataframe(estatisticas.style.format("{:.2f}%"), use_container_width=True)

## Seção 8: Gráfico de Estatísticas Descritivas
st.markdown("### 📊 Visualização das Estatísticas Descritivas")

# Preparar dados para o gráfico
estatisticas_melted = estatisticas.reset_index().melt(
    id_vars='index', 
    value_vars=simulados, 
    var_name='Simulado', 
    value_name='Valor'
)
estatisticas_melted.rename(columns={'index': 'Estatística'}, inplace=True)

# Criar gráfico de barras agrupadas
fig_estatisticas = px.bar(
    estatisticas_melted,
    x='Simulado',
    y='Valor',
    color='Estatística',
    barmode='group',
    title='Estatísticas Descritivas por Simulado',
    labels={'Valor': 'Valor (%)', 'Simulado': 'Simulado'},
    template='plotly_white',
    height=500
)

# Adicionar valores nas barras
fig_estatisticas.update_traces(
    texttemplate='%{y:.1f}%',
    textposition='outside'
)

fig_estatisticas.update_layout(
    xaxis_title="Simulado",
    yaxis_title="Valor (%)",
    legend_title="Estatística",
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

st.plotly_chart(fig_estatisticas, use_container_width=True)

## Seção 9: Boxplot de Distribuição
st.markdown("### 📦 Distribuição de Notas por Simulado")

# Criar boxplot
fig_boxplot = px.box(
    df.melt(value_vars=simulados, var_name='Simulado', value_name='Porcentagem'),
    x='Simulado',
    y='Porcentagem',
    color='Simulado',
    title='Distribuição de Notas por Simulado',
    template='plotly_white',
    height=500
)

fig_boxplot.update_layout(
    xaxis_title="Simulado",
    yaxis_title="Porcentagem de Acertos (%)",
    showlegend=False
)

# Adicionar pontos individuais
fig_boxplot.add_trace(go.Scatter(
    x=df.melt(value_vars=simulados, var_name='Simulado', value_name='Porcentagem')['Simulado'],
    y=df.melt(value_vars=simulados, var_name='Simulado', value_name='Porcentagem')['Porcentagem'],
    mode='markers',
    marker=dict(color='rgba(0,0,0,0.3)', size=5),
    name='Alunos',
    hovertemplate='<b>%{x}</b><br>Nota: %{y:.1f}%<extra></extra>'
))

st.plotly_chart(fig_boxplot, use_container_width=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 14px;">
    <p>Escola Estadual Helena Dionysio - Recomposição da Aprendizagem - Plano de Ação</p>
    <p>© 2025 HD Analytic - Todos os direitos reservados</p>
</div>
""", unsafe_allow_html=True)
