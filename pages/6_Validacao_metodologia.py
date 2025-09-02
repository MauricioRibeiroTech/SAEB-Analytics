import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import shapiro, levene, f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import plotly.express as px
import plotly.graph_objects as go
import re
import warnings
warnings.filterwarnings('ignore')

# Configurações da página com estilo moderno
st.set_page_config(
    page_title="SAEB Analytics - Estatística",
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
    .metric-card {
        background: #000000;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #3498db;
        margin: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
    .significance-positive {
        color: #2ecc71;
        font-weight: 700;
        font-size: 1.1em;
    }
    .significance-negative {
        color: #e74c3c;
        font-weight: 700;
        font-size: 1.1em;
    }
    .premissa-ok {
        color: #27ae60;
        font-weight: 600;
    }
    .premissa-nok {
        color: #e74c3c;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Função para calcular porcentagens - agora genérica
def calcular_porcentagens(df, disciplina):
    # Dicionário de divisores por disciplina
    DIVISORES = {
        "Matemática": {
            'Sim1': 10, 'Sim2': 10, 'Sim3': 12,
            'Sim4': 15, 'Sim5': 18, 'Sim6': 18,
            'Sim7': 20, 'Sim8': 16, 'Sim9': 26,
            'Sim10': 16, 'Sim11': 18, 'Sim12': 16,
            'Sim13': 16,'Sim14': 23,'Sim15': 16,'Sim16': 24,'Sim17': 25
        },
        "Português": {
            'Sim1': 10, 'Sim2': 10, 'Sim3': 10,
            'Sim4': 15, 'Sim5': 18, 'Sim6': 18,
            'Sim7': 14, 'Sim8': 16, 'Sim9': 26,
            'Sim10': 16, 'Sim11': 18, 'Sim12': 16,
            'Sim13': 16,'Sim14': 16,'Sim15': 16,'Sim16': 15,'Sim17': 15
        }
    }

    # Encontra automaticamente todas as colunas de simulado
    colunas_sim = [col for col in df.columns if re.match(r'Sim\d+', col)]

    # Calcula as porcentagens apenas para as colunas existentes com divisores definidos
    for col in colunas_sim:
        if col in DIVISORES[disciplina]:
            df[f'Porcentagem {col}'] = (df[col] / DIVISORES[disciplina][col]) * 100

    return df

# Classe para análise estatística
class AnaliseEstatistica:
    def __init__(self, df, simulados):
        self.df = df
        self.simulados = simulados
    
    def verificar_premissas(self):
        resultados = {'normalidade': {}, 'homogeneidade': {}}
        
        # Teste de Normalidade (Shapiro-Wilk)
        for simulado in self.simulados:
            # Remover valores NaN para o teste
            dados_limpos = self.df[simulado].dropna()
            if len(dados_limpos) > 3:  # Shapiro-Wilk requer pelo menos 3 observações
                stat, p = shapiro(dados_limpos)
                resultados['normalidade'][simulado] = {
                    'stat': stat, 
                    'p': p, 
                    'normal': p > 0.05
                }
        
        # Teste de Homogeneidade de Variâncias (Levene)
        dados_lista = [self.df[simulado].dropna() for simulado in self.simulados]
        if all(len(d) > 0 for d in dados_lista):
            stat, p = levene(*dados_lista)
            resultados['homogeneidade'] = {
                'stat': stat, 
                'p': p, 
                'homogeneo': p > 0.05
            }
        
        return resultados
    
    def analise_anova(self):
        dados_lista = [self.df[simulado].dropna() for simulado in self.simulados]
        if all(len(d) > 0 for d in dados_lista):
            f_stat, p_value = f_oneway(*dados_lista)
            return {
                'f_stat': f_stat, 
                'p_value': p_value, 
                'significativo': p_value < 0.05
            }
        return None
    
    def analise_post_hoc(self):
        dados_long = []
        for simulado in self.simulados:
            for valor in self.df[simulado].dropna():
                dados_long.append({'simulado': simulado, 'porcentagem': valor})
        
        if len(dados_long) > 0:
            dados_long_df = pd.DataFrame(dados_long)
            tukey = pairwise_tukeyhsd(
                endog=dados_long_df['porcentagem'],
                groups=dados_long_df['simulado'],
                alpha=0.05
            )
            return tukey
        return None

# Sidebar moderna
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #2c3e50; font-size: 24px;">Análise Estatística SAEB</h1>
        <h2 style="color: #3498db; font-size: 18px;">Escola Estadual Helena Dionysio</h2>
    </div>
    """, unsafe_allow_html=True)

    # Carregar dados
    df = pd.read_csv("pages/Dados_simples_simulados.csv", sep=",")

    # Corrigir nome da coluna Componente
    df['Componente'] = df['Componente'].replace({
        'Matematica': 'Matemática',
        'Portugues': 'Português'
    })

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
simulados = [col for col in df.columns if col.startswith('Porcentagem Sim')]

# Layout principal com cabeçalho destacado
st.markdown(f"""
<div style="background-color: #3498db; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
    <h1 style="text-align: center; margin: 0;">Análise Estatística de {componente_selecionada}</h1>
    <h2 style="text-align: center; margin: 0;">Testes de Significância e Evolução</h2>
</div>
""", unsafe_allow_html=True)

# Inicializar análise estatística
analise = AnaliseEstatistica(df, simulados)

## Seção 1: Visão Geral em Cards
st.markdown("### 📊 Visão Geral do Desempenho")

# Criar métricas em colunas
col1, col2, col3, col4 = st.columns(4)

# Calcular médias, tratando possíveis valores NaN
medias = df[simulados].mean()
media_geral = medias.mean().round(1)

# Encontrar melhor e pior simulado
if not medias.empty:
    melhor_simulado = medias.idxmax().replace('Porcentagem ', '') if not medias.isna().all() else "N/A"
    pior_simulado = medias.idxmin().replace('Porcentagem ', '') if not medias.isna().all() else "N/A"
else:
    melhor_simulado = "N/A"
    pior_simulado = "N/A"

# Calcular evolução (diferença entre primeiro e último simulado)
if len(simulados) >= 2:
    evolucao = (medias.iloc[-1] - medias.iloc[0]).round(1)
else:
    evolucao = "N/A"

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📊 Média Geral</h3>
        <h2>{media_geral}%</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>🏆 Melhor Simulado</h3>
        <h2>{melhor_simulado}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📉 Maior Desafio</h3>
        <h2>{pior_simulado}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    evolucao_color = "significance-positive" if (isinstance(evolucao, (int, float)) and evolucao > 0) else "significance-negative"
    evolucao_text = f"+{evolucao}%" if (isinstance(evolucao, (int, float)) and evolucao > 0) else f"{evolucao}%"
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>📈 Evolução</h3>
        <h2 class="{evolucao_color}">{evolucao_text if evolucao != "N/A" else "N/A"}</h2>
    </div>
    """, unsafe_allow_html=True)

## Seção 2: Gráfico de Evolução com Análise Estatística
st.markdown("### 📈 Evolução do Desempenho com Análise Estatística")

# Preparar dados para o gráfico
medias_simulados = df[simulados].mean().reset_index()
medias_simulados.columns = ['Simulado', 'Porcentagem']
medias_simulados['Simulado'] = medias_simulados['Simulado'].str.replace('Porcentagem ', '')

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

## Seção 3: Análise Estatística
st.markdown("### 🧪 Análise Estatística de Significância")

with st.spinner("Executando análise estatística..."):
    # Verificar premissas
    premissas = analise.verificar_premissas()
    
    # Executar ANOVA
    resultado_anova = analise.analise_anova()
    
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📏 Teste de Normalidade (Shapiro-Wilk)")
    if premissas['normalidade']:
        for simulado, resultado in premissas['normalidade'].items():
            sim_nome = simulado.replace('Porcentagem ', '')
            status = "✅" if resultado['normal'] else "⚠️"
            cor_classe = "premissa-ok" if resultado['normal'] else "premissa-nok"
            st.markdown(f"{status} <span class='{cor_classe}'>{sim_nome}: p = {resultado['p']:.4f}</span>", 
                    unsafe_allow_html=True)
    else:
        st.info("ℹ️ Não foi possível executar o teste de normalidade")

with col2:
    st.markdown("#### 📊 Análise de Variância (ANOVA)")
    
    if resultado_anova:
        st.markdown(f"""
        <div style='background: #000000; 
                    padding: 1.5rem; border-radius: 10px; border-left: 5px solid #3498db;'>
            <h4 style='margin-top: 0;'>Resultados da ANOVA</h4>
            <p><b>F-estatística:</b> {resultado_anova['f_stat']:.4f}</p>
            <p><b>Valor-p:</b> {resultado_anova['p_value']:.4f}</p>
            <p><b>Significância:</b> <span class="{'significance-positive' if resultado_anova['significativo'] else 'significance-negative'}">
                {'✅ SIGNIFICATIVO' if resultado_anova['significativo'] else '❌ NÃO SIGNIFICATIVO'}
            </span></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Teste Post Hoc se ANOVA for significativa
        if resultado_anova['significativo']:
            with st.spinner("Executando teste Post Hoc..."):
                tukey = analise.analise_post_hoc()
            
            if tukey:
                st.markdown("#### 🔍 Teste Post Hoc de Tukey")
                st.write("Comparações pareadas entre simulados:")
                
                # Converter resultados do Tukey para DataFrame
                tukey_data = []
                for linha in tukey.summary().data[1:]:
                    tukey_data.append(linha)
                
                tukey_df = pd.DataFrame(tukey_data, columns=tukey.summary().data[0])
                st.dataframe(tukey_df, use_container_width=True)
    else:
        st.info("ℹ️ Não foi possível executar a ANOVA")

## Seção 4: Mapa de Calor Interativo
st.markdown("### 👥 Desempenho Individual por Simulado")

# Gráfico de heatmap aprimorado
df_melted = df.melt(id_vars=['Aluno'],
                    value_vars=simulados,
                    var_name='Simulado',
                    value_name='Porcentagem')

df_melted['Simulado'] = df_melted['Simulado'].str.replace('Porcentagem ', '')

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

## Seção 5: Top Alunos com Gráfico de Medalhas
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

## Seção 6: Análise de Evolução Individual
st.markdown("### 📈 Evolução Individual dos Alunos")

# Selecionar aluno para análise detalhada
aluno_selecionado = st.selectbox(
    "Selecione um aluno para análise detalhada:",
    options=df['Aluno'].unique(),
    index=0
)

# Dados do aluno selecionado
aluno_data = df[df['Aluno'] == aluno_selecionado].iloc[0]

# Preparar dados para o gráfico individual
desempenho_aluno = [aluno_data[sim] for sim in simulados]
nomes_simulados = [sim.replace('Porcentagem ', '') for sim in simulados]

# Criar gráfico de evolução individual
fig4 = go.Figure()

fig4.add_trace(go.Scatter(
    x=nomes_simulados,
    y=desempenho_aluno,
    mode='lines+markers+text',
    name='Desempenho do Aluno',
    line=dict(color='#e74c3c', width=3),
    marker=dict(size=10, color='#e74c3c'),
    text=desempenho_aluno,
    textposition="top center",
    texttemplate='%{text:.1f}%',
    hovertemplate='%{x}<br>Desempenho: %{y:.1f}%'
))

# Adicionar linha de média geral para comparação
fig4.add_trace(go.Scatter(
    x=nomes_simulados,
    y=medias_simulados['Porcentagem'],
    mode='lines',
    name='Média da Turma',
    line=dict(color='#3498db', width=2, dash='dash'),
    hovertemplate='%{x}<br>Média: %{y:.1f}%'
))

# Layout do gráfico
fig4.update_layout(
    template='plotly_white',
    height=500,
    xaxis_title="Simulado",
    yaxis_title="Porcentagem de Acertos (%)",
    yaxis_range=[0, 100],
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=40, r=40, t=40, b=40)
)

st.plotly_chart(fig4, use_container_width=True)

# Métricas do aluno selecionado
col1, col2, col3, col4 = st.columns(4)

media_aluno = np.mean(desempenho_aluno)
melhor_simulado_aluno = nomes_simulados[np.argmax(desempenho_aluno)]
pior_simulado_aluno = nomes_simulados[np.argmin(desempenho_aluno)]
evolucao_aluno = desempenho_aluno[-1] - desempenho_aluno[0]

with col1:
    st.metric("Média do Aluno", f"{media_aluno:.1f}%")

with col2:
    st.metric("Melhor Simulado", melhor_simulado_aluno)

with col3:
    st.metric("Maior Desafio", pior_simulado_aluno)

with col4:
    st.metric("Evolução", f"{evolucao_aluno:+.1f}%")

## Seção 7: Alunos acima de 60% em Abas Estilizadas
st.markdown("### ✅ Alunos com Desempenho Acima de 60%")

# Criar abas para cada simulado
tabs = st.tabs([sim.replace('Porcentagem ', '') for sim in simulados])

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
                    title=f'Desempenho no {sim.replace("Porcentagem ", "")}',
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
                st.warning(f"Nenhum aluno atingiu 60% no {sim.replace('Porcentagem ', '')}", icon="⚠️")
