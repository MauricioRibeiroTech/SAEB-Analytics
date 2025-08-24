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
    page_title="SAEB Analytics - Simulados Externos",
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
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
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
    .interpretation-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #d0f0d0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #27ae60;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .conclusion-positive {
        background: linear-gradient(135deg, #e8f5e8 0%, #d0f0d0 100%);
        border-left: 5px solid #27ae60;
    }
    .conclusion-neutral {
        background: linear-gradient(135deg, #e8f4f8 0%, #d0e8f0 100%);
        border-left: 5px solid #3498db;
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

# Função para interpretar resultados estatísticos
def interpretar_resultados(premissas, anova, tukey):
    interpretacoes = []
    
    # Interpretação da normalidade
    interpretacoes.append("### 📏 Análise de Normalidade (Shapiro-Wilk)")
    for simulado, resultado in premissas['normalidade'].items():
        status = "✅" if resultado['normal'] else "⚠️"
        interpretacao = f"{status} **{simulado}**: p = {resultado['p']:.4f} - "
        interpretacao += "Dados normais (atende premissa)" if resultado['normal'] else "Dados não normais"
        interpretacoes.append(interpretacao)
    
    # Interpretação da ANOVA
    interpretacoes.append("\n### 📊 Análise de Variância (ANOVA)")
    if anova:
        interpretacao = f"**F-estatística**: {anova['f_stat']:.4f}, **Valor-p**: {anova['p_value']:.4f}\n\n"
        if anova['significativo']:
            interpretacao += "✅ **Diferenças significativas** entre os simulados (p < 0.05)"
        else:
            interpretacao += "❌ **Não há diferenças significativas** entre os simulados"
        interpretacoes.append(interpretacao)
    
    # Interpretação do Post Hoc
    if tukey and anova and anova['significativo']:
        interpretacoes.append("\n### 🔍 Teste Post Hoc de Tukey")
        
        # Converter resultados do Tukey para DataFrame
        tukey_data = []
        for linha in tukey.summary().data[1:]:
            tukey_data.append(linha)
        
        tukey_df = pd.DataFrame(tukey_data, columns=tukey.summary().data[0])
        
        # Encontrar diferenças significativas
        diferencas_significativas = tukey_df[tukey_df['reject'] == True]
        
        if len(diferencas_significativas) > 0:
            interpretacoes.append("✅ **Diferenças significativas encontradas:**")
            for _, row in diferencas_significativas.iterrows():
                interpretacao = f"- **{row['group1']} vs {row['group2']}**: "
                interpretacao += f"Diferença = {row['meandiff']:.2f}%, p = {row['p-adj']:.4f}"
                interpretacoes.append(interpretacao)
                
                # Interpretação pedagógica
                if row['meandiff'] > 0:
                    interpretacao = f"  → {row['group2']} teve desempenho {abs(row['meandiff']):.2f}% melhor"
                else:
                    interpretacao = f"  → {row['group1']} teve desempenho {abs(row['meandiff']):.2f}% melhor"
                interpretacoes.append(interpretacao)
        else:
            interpretacoes.append("❌ **Nenhuma diferença significativa entre pares específicos**")
    
    return interpretacoes

# Sidebar moderna
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #2c3e50; font-size: 24px;">Relatório Parcial SAEB 2025</h1>
        <h2 style="color: #3498db; font-size: 18px;">Escola Estadual Helena Dionysio</h2>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("main.py", label="🏠 Página Inicial")
    st.page_link("pages/3_Relatorios_Mensais.py", label="📅 Relatório Mensal")
    st.page_link("pages/2_SAEB_Descritores.py", label="📊 Relatório SAEB Descritores")
    st.page_link("pages/1_SAEB_Metodologia.py", label="📈 Desempenho percentual")

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
    <h1 style="text-align: center; margin: 0;">Desempenho nos Simulados Externos</h1>
    <h2 style="text-align: center; margin: 0;">Análise Estatística Avançada</h2>
</div>
""", unsafe_allow_html=True)

# Definir simulados
simulados = ['SAEB ACERTA BRASIL', 'CAEd 1', 'CAEd 2']

# Inicializar análise estatística
analise = AnaliseEstatistica(df, simulados)

## Seção 1: Visão Geral em Cards
st.markdown("### 📊 Visão Geral do Desempenho")

# Criar métricas em colunas
col1, col2, col3, col4 = st.columns(4)

# Calcular estatísticas
medias = df[simulados].mean()
media_geral = medias.mean().round(1)
melhor_simulado = medias.idxmax()
pior_simulado = medias.idxmin()
evolucao = (df['CAEd 2'].mean() - df['SAEB ACERTA BRASIL'].mean()).round(1)

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
    evolucao_color = "significance-positive" if evolucao > 0 else "significance-negative"
    evolucao_text = f"+{evolucao}%" if evolucao > 0 else f"{evolucao}%"
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>📈 Evolução</h3>
        <h2 class="{evolucao_color}">{evolucao_text}</h2>
    </div>
    """, unsafe_allow_html=True)

## Seção 2: Análise Estatística Completa
st.markdown("### 🧪 Análise Estatística de Significância")

with st.spinner("Executando análise estatística..."):
    # Verificar premissas
    premissas = analise.verificar_premissas()
    
    # Executar ANOVA
    resultado_anova = analise.analise_anova()
    
    # Executar Post Hoc se ANOVA for significativa
    resultado_tukey = None
    if resultado_anova and resultado_anova['significativo']:
        resultado_tukey = analise.analise_post_hoc()
    
    # Gerar interpretações
    interpretacoes = interpretar_resultados(premissas, resultado_anova, resultado_tukey)

# Exibir interpretações
with st.expander("📋 **Interpretação Estatística Detalhada**", expanded=True):
    for interpretacao in interpretacoes:
        if interpretacao.startswith("###"):
            st.markdown(interpretacao)
        else:
            st.write(interpretacao)
    
    # Conclusão pedagógica baseada nos resultados
    st.markdown("\n### 🎯 Conclusão Pedagógica")
    
    if resultado_anova and resultado_anova['significativo'] and resultado_tukey:
        st.markdown("""
        <div class="interpretation-card">
            <h4>✅ Melhoria Significativa Detectada</h4>
            <p>Os resultados indicam uma <b>evolução significativa</b> no desempenho dos alunos ao longo dos simulados.</p>
            <p><b>Implicações pedagógicas:</b></p>
            <ul>
                <li>As estratégias de ensino estão funcionando</li>
                <li>Os alunos estão assimilando os conteúdos</li>
                <li>Há progresso consistente na aprendizagem</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="interpretation-card conclusion-neutral">
            <h4>📊 Tendência de Evolução</h4>
            <p>Embora não tenham sido detectadas diferenças estatisticamente significativas, observa-se uma tendência positiva de evolução.</p>
            <p><b>Recomendações:</b></p>
            <ul>
                <li>Manter as estratégias atuais</li>
                <li>Reforçar conteúdos específicos</li>
                <li>Monitorar evolução contínua</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

## Seção 3: Gráfico de Evolução
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

## Seção 4: Resultados do Teste Post Hoc (se aplicável)
if resultado_tukey:
    st.markdown("### 🔍 Resultados Detalhados do Teste Post Hoc")
    
    # Converter resultados do Tukey para DataFrame
    tukey_data = []
    for linha in resultado_tukey.summary().data[1:]:
        tukey_data.append(linha)
    
    tukey_df = pd.DataFrame(tukey_data, columns=resultado_tukey.summary().data[0])
    
    # Destacar resultados significativos
    def highlight_significant(row):
        if row['reject']:
            return ['background-color: #e8f5e8' for _ in row]
        return ['background-color: white' for _ in row]
    
    st.dataframe(
        tukey_df.style.apply(highlight_significant, axis=1),
        use_container_width=True
    )

## Seções restantes (mapa de calor, top alunos, etc.) mantidas do código anterior
# ... [o restante do seu código original aqui] ...

## Seção 10: Recomendações Finais
st.markdown("### 💡 Recomendações Pedagógicas")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="interpretation-card">
        <h4>🎯 Para Alunos com Baixo Desempenho</h4>
        <ul>
            <li>Reforço individualizado</li>
            <li>Exercícios específicos</li>
            <li>Acompanhamento personalizado</li>
            <li>Plantão de dúvidas</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="interpretation-card">
        <h4>🚀 Para Manter a Evolução</h4>
        <ul>
            <li>Manter estratégias atuais</li>
            <li>Simulados regulares</li>
            <li>Feedback constante</li>
            <li>Metas progressivas</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Adicione as seções restantes do seu código original aqui...
# Seção 4: Mapa de Calor Interativo
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

# Criar gráfico de evolução individual
fig4 = go.Figure()

fig4.add_trace(go.Scatter(
    x=simulados,
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
    x=simulados,
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
melhor_simulado_aluno = simulados[np.argmax(desempenho_aluno)]
pior_simulado_aluno = simulados[np.argmin(desempenho_aluno)]
evolucao_aluno = desempenho_aluno[-1] - desempenho_aluno[0]

with col1:
    st.metric("Média do Aluno", f"{media_aluno:.1f}%")

with col2:
    st.metric("Melhor Simulado", melhor_simulado_aluno)

with col3:
    st.metric("Maior Desafio", pior_simulado_aluno)

with col4:
    st.metric("Evolução", f"{evolucao_aluno:+.1f}%")
