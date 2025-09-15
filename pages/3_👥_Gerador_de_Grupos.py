import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import plotly.graph_objects as go

# --- Configuração da Página e Estilo ---
st.set_page_config(page_title="Gerador de grupos Recomposição de Aprendizagem- CESB Analytics", layout="wide", initial_sidebar_state="expanded")

# CSS para uma apresentação mais elegante dos grupos
st.markdown("""
<style>
    /* Estilo para o container do expander (card do grupo) */
    .st-expander {
        border: 1px solid #e6e6e6;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        transition: 0.3s;
        margin-bottom: 20px; /* Espaço entre os cards */
    }
    .st-expander:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }
    /* Estilo para o cabeçalho do expander */
    .st-expander header {
        font-size: 1.25rem;
        font-weight: bold;
        color: #004d40; /* Verde escuro */
    }
</style>
""", unsafe_allow_html=True)


# --- Título do Aplicativo ---
st.title("👥 Gerador de Grupos Pedagógicos")
st.markdown("Filtre por turma e selecione as habilidades para criar grupos de trabalho heterogêneos e equilibrados.")
st.markdown("---")


# --- Dicionários de Habilidades (mantidos como no original) ---
DESCRICOES_HABILIDADES = {
    "CAED1_Matemática": {
        "H01": "Utilizar informações apresentadas em tabelas ou gráficos na resolução de problemas.",
        "H02": "Utilizar o princípio multiplicativo de contagem na resolução de problema.",
        "H03": "Utilizar probabilidade na resolução de problema.",
        "H04": "Utilizar proporcionalidade entre duas grandezas na resolução de problema.",
        "H05": "Corresponder pontos do plano a pares ordenados em um sistema de coordenadas cartesianas.",
        "H06": "Utilizar o cálculo de volumes/capacidade de prismas retos e de cilindros na resolução de problema.",
        "H07": "Utilizar perímetro de figuras bidimensionais na resolução de problema.",
        "H08": "Utilizar relações métricas de um triângulo retângulo na resolução de problema.",
        "H09": "Analisar regiões de crescimento/decrescimento, domínios de validade ou zeros de funções reais representadas graficamente.",
        "H10": "Utilizar função polinomial de 1º grau na resolução de problemas.",
        "H11": "Reconhecer a representação algébrica de uma função polinomial de 2º grau a partir dos dados apresentados em uma tabela.",
        "H12": "Utilizar a medida da área total e/ou lateral de um sólido na resolução de problema.",
        "H13": "Utilizar função exponencial na resolução de problemas.",
        "H14": "Utilizar função polinomial de 2º grau na resolução de problemas.",
        "H15": "Utilizar propriedades de progressões aritméticas ou geométricas na resolução de problemas.",
        "H16": "Utilizar equação polinomial de 2º grau na resolução de problema.",
        "H17": "Reconhecer a representação gráfica das funções trigonométricas (seno, cosseno e tangente).",
        "H18": "Resolver problemas que envolvam razões trigonométricas no triângulo retângulo.",
    },
    "CAED2_Matemática": {
        "H01": "Corresponder figuras tridimensionais às suas planificações.",
        "H02": "Utilizar informações apresentadas em tabelas ou gráficos na resolução de problemas",
        "H03": "Utilizar o princípio multiplicativo de contagem na resolução de problema.",
        "H04": "Utilizar probabilidade na resolução de problema.",
        "H05": "Utilizar proporcionalidade entre duas grandezas na resolução de problema.",
        "H06": "Corresponder pontos do plano a pares ordenados em um sistema de coordenadas cartesianas.",
        "H07": "Utilizar o cálculo de volumes/capacidade de prismas retos e de cilindros na resolução de problema.",
        "H08": "Utilizar perímetro de figuras bidimensionais na resolução de problema.",
        "H09": "Utilizar porcentagem na resolução de problemas.",
        "H10": "Utilizar relações métricas de um triângulo retângulo na resolução de problema.",
        "H11": "Analisar regiões de crescimento/decrescimento, domínios de validade ou zeros de funções reais representadas graficamente.",
        "H12": "Corresponder a representação algébrica e gráfica de uma função polinomial de 1º grau.",
        "H13": "Utilizar função polinomial de 1º grau na resolução de problemas.",
        "H14": "Utilizar a medida da área total e/ou lateral de um sólido na resolução de problema.",
        "H15": "Utilizar função exponencial na resolução de problemas.",
        "H16": "Utilizar função polinomial de 2º grau na resolução de problemas.",
        "H17": "Utilizar propriedades de progressões aritméticas ou geométricas na resolução de problemas.",
        "H18": "Identificar a representação algébrica ou gráfica de uma função exponencial.",
        "H19": "Utilizar equação polinomial de 2º grau na resolução de problema.",
        "H20": "Relacionar as raízes de um polinômio com sua decomposição em fatores do 1º grau.",
        "H21": "Reconhecer a representação gráfica das funções trigonométricas (seno, cosseno e tangente).",
        "H22": "Resolver problemas que envolvam razões trigonométricas no triângulo retângulo."
    },
    "CAED1_Português": {
        "H01": "Reconhecer formas de tratar uma informação na comparação de textos que tratam do mesmo tema.",
        "H02": "Localizar informação explícita.",
        "H03": "Inferir informações em textos.",
        "H04": "Reconhecer efeito de humor ou de ironia em um texto.",
        "H05": "Distinguir ideias centrais de secundárias ou tópicos and subtópicos em um dado gênero textual.",
        "H06": "Identificar a tese de um texto.",
        "H07": "Reconhecer posições distintas relativas ao mesmo fato ou mesmo tema.",
        "H08": "Reconhecer as relações entre partes de um texto, identificando os recursos coesivos que contribuem para a sua continuidade.",
        "H09": "Distinguir um fato da opinião.",
        "H10": "Reconhecer o sentido das relações lógico-discursivas em um texto.",
        "H11": "Reconhecer o efeito de sentido decorrente da escolha de uma determinada palavra ou expressão.",
        "H12": "Estabelecer relação entre a tese e os argumentos oferecidos para sustentá-la.",
        "H13": "Estabelecer relação causa/consequência entre partes e elementos do texto.",
        "H14": "Reconhecer o efeito de sentido decorrente da exploração de recursos ortográficos e/ou morfossintáticos.",
        "H15": "Identificar as marcas linguísticas que evidenciam o locutor e o interlocutor de um texto.",
    },
    "CAED2_Português": {
        "H01": "Reconhecer formas de tratar uma informação na comparação de textos que tratam do mesmo tema.",
        "H02": "Localizar informação explícita.",
        "H03": "Inferir informações em textos.",
        "H04": "Reconhecer efeito de humor ou de ironia em um texto.",
        "H05": "Distinguir ideias centrais de secundárias ou tópicos and subtópicos em um dado gênero textual.",
        "H06": "Identificar a tese de anúncio.",
        "H07": "Reconhecer posições distintas relativas ao mesmo fato ou mesmo tema.",
        "H08": "Reconhecer as relações entre partes de um texto, identificando os recursos coesivos que contribuem para a sua continuidade.",
        "H09": "Distinguir um fato da opinião.",
        "H10": "Reconhecer o sentido das relações lógico-discursivas em anúncio.",
        "H11": "Reconhecer o efeito de sentido decorrente da escolha de uma determinada palavra ou expressão.",
        "H12": "Estabelecer relação entre a tese e os argumentos oferecidos para sustentá-la.",
        "H13": "Estabelecer relação causa/consequência entre partes e elementos do texto.",
        "H14": "Reconhecer o efeito de sentido decorrente da exploração de recursos ortográficos e/ou morfossintáticos.",
        "H15": "Identificar as marcas linguísticas que evidenciam o locutor e o interlocutor de um texto.",
    },
    "9_Matematica": {
        "H01": "Corresponder figuras tridimensionais às suas planificações.",
        "H02": "Utilizar informações apresentadas em tabelas ou gráficos na resolução de problemas.",
        "H03": "Utilizar área de figuras bidimensionais na resolução de problema.",
        "H04": "Identificar frações equivalentes.",
        "H05": "Utilizar conversão entre unidades de medida, na resolução de problema.",
        "H06": "Utilizar o princípio multiplicativo de contagem na resolução de problema.",
        "H07": "Utilizar proporcionalidade entre duas grandezas na resolução de problema.",
        "H08": "Classificar quadriláteros por meio de suas propriedades.",
        "H09": "Classificar triângulos por meio de suas propriedades.",
        "H10": "Corresponder diferentes representações de um número racional.",
        "H11": "Utilizar o cálculo de volumes/capacidade de prismas retos e de cilindros na resolução de problema.",
        "H12": "Utilizar perímetro de figuras bidimensionais na resolução de problema.",
        "H13": "Utilizar porcentagem na resolução de problemas.",
        "H14": "Identificar a expressão algébrica que expressa uma regularidade observada em sequência de números ou figuras (padrões).",
        "H15": "Executar cálculos com números reais.",
        "H16": "Utilizar o cálculo do valor numérico de expressões algébricas na resolução de problemas.",
        "H17": "Utilizar relações métricas de um triângulo retângulo na resolução de problema.",
        "H18": "Utilizar equação polinomial de 2º grau na resolução de problema.",
        "H19": "Utilizar números racionais, envolvendo diferentes significados das operações, na resolução de problemas.",
        "H20": "Identificar uma equação or inequação do 1º grau que expressa um problema."
    },
    "9_Português": {
        "H01": "Identificar a finalidade de textos de diferentes gêneros.",
        "H02": "Localizar informação explícita.",
        "H03": "Inferir informações em textos.",
        "H04": "Reconhecer efeito de humor ou de ironia em um texto.",
        "H05": "Distinguir ideias centrais de secundárias ou tópicos e subtópicos em um dado gênero textual.",
        "H06": "Reconhecer os elementos que compõem uma narrativa e o conflito gerador.",
        "H07": "Identificar a tese de um texto.",
        "H08": "Reconhecer posições distintas relativas ao mesmo fato ou mesmo tema.",
        "H09": "Reconhecer as relações entre partes de um texto, identificando os recursos coesivos que contribuem para a sua continuidade.",
        "H10": "Distinguir um fato da opinião.",
        "H11": "Reconhecer o sentido das relações lógico-discursivas em um texto.",
        "H12": "Reconhecer o efeito de sentido decorrente da escolha de uma determinada palavra or expressão.",
        "H13": "Estabelecer relação entre a tese e os argumentos oferecidos para sustentá-la.",
        "H14": "Reconhecer o efeito de sentido decorrente da exploração de recursos ortográficos e/ou morfossintáticos.",
        "H15": "Identificar as marcas linguísticas que evidenciam o locutor e o interlocutor de um texto.",
    }
}


# --- Funções do Aplicativo ---

@st.cache_data
def carregar_dados(arquivo_selecionado):
    """Carrega o arquivo CSV selecionado da mesma pasta do script"""
    try:
        # Tenta usar __file__ que é mais robusto
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, arquivo_selecionado)
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
            df.columns = df.columns.str.strip()
            return df
        else:
            st.error(f"Arquivo '{arquivo_selecionado}' não encontrado na pasta do script.")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

def get_descricao_habilidade(codigo, arquivo_nome):
    """Obtém a descrição da habilidade baseada no nome do arquivo"""
    codigo = codigo.strip().replace(' ', '')
    
    if "CAED1_3_matematica" in arquivo_nome:
        return DESCRICOES_HABILIDADES["CAED1_Matemática"].get(codigo, "N/A")
    elif "CAED2_3_matematica" in arquivo_nome:
        return DESCRICOES_HABILIDADES["CAED2_Matemática"].get(codigo, "N/A")
    elif "CAED1_3_portugues" in arquivo_nome:
        return DESCRICOES_HABILIDADES["CAED1_Português"].get(codigo, "N/A")
    elif "CAED2_3_portugues" in arquivo_nome:
        return DESCRICOES_HABILIDADES["CAED2_Português"].get(codigo, "N/A")
    elif "9_matematica" in arquivo_nome:
        return DESCRICOES_HABILIDADES["9_Matematica"].get(codigo, "N/A")
    elif "9_portugues" in arquivo_nome:
        return DESCRICOES_HABILIDADES["9_Português"].get(codigo, "N/A")
    else:
        return "Descrição não disponível"

def formar_grupos_por_niveis(alunos_df, habilidades_selecionadas, max_por_grupo):
    """
    Forma grupos heterogêneos garantindo um equilíbrio entre diferentes níveis de domínio.
    Níveis baseados na média de pontuação das habilidades selecionadas.
    """
    if alunos_df.empty or not habilidades_selecionadas:
        return []

    alunos_list = alunos_df.to_dict('records')
    
    alunos_nivel_0 = []  # Não Domina
    alunos_nivel_1 = []  # Domina
    alunos_nivel_2 = []  # Domina Plenamente

    for aluno in alunos_list:
        pontuacoes = [aluno[hab] for hab in habilidades_selecionadas if hab in aluno and isinstance(aluno[hab], (int, float))]
        media = np.mean(pontuacoes) if pontuacoes else 0
        
        aluno['media_habilidades'] = media
        
        if media < 0.8:
            alunos_nivel_0.append(aluno)
        elif media < 1.6:
            alunos_nivel_1.append(aluno)
        else:
            alunos_nivel_2.append(aluno)

    random.shuffle(alunos_nivel_0)
    random.shuffle(alunos_nivel_1)
    random.shuffle(alunos_nivel_2)
    
    num_total_alunos = len(alunos_list)
    num_grupos = (num_total_alunos + max_por_grupo - 1) // max_por_grupo
    
    if num_grupos == 0:
        return []
        
    grupos = [[] for _ in range(num_grupos)]
    
    todos_os_alunos_para_distribuir = alunos_nivel_2 + alunos_nivel_1 + alunos_nivel_0

    for i, aluno in enumerate(todos_os_alunos_para_distribuir):
        grupo_idx = i % num_grupos
        grupos[grupo_idx].append(aluno)

    return grupos

def calcular_pontuacao_grupo(grupo, habilidades_cols):
    """Calcula a pontuação média do grupo para cada habilidade"""
    if not grupo:
        return {hab: 0 for hab in habilidades_cols}
        
    grupo_df = pd.DataFrame(grupo)
    medias = {hab: grupo_df[hab].mean() for hab in habilidades_cols if hab in grupo_df}
    return medias

def encontrar_colunas_info(df):
    """Encontra as colunas de aluno e turma no DataFrame"""
    aluno_col, turma_col = None, None
    for col in df.columns:
        col_lower = col.lower()
        if 'aluno' in col_lower or 'nome' in col_lower:
            aluno_col = col
        elif 'turma' in col_lower:
            turma_col = col
    return aluno_col, turma_col

# --- Interface Principal ---
def main():
    st.sidebar.header("📁 1. Seleção de Dados")
    arquivos_csv = [
        "CAED1_3_matematica.csv", "CAED1_3_portugues.csv",
        "CAED2_3_matematica.csv", "CAED2_3_portugues.csv",
        "CAED1_9_matematica.csv", "CAED1_9_portugues.csv",
        "CAED2_9_matematica.csv", "CAED2_9_portugues.csv"
    ]
    arquivo_selecionado = st.sidebar.selectbox(
        "Selecione o arquivo CSV:",
        arquivos_csv
    )
    
    df = carregar_dados(arquivo_selecionado)
    
    if df is not None:
        aluno_col, turma_col = encontrar_colunas_info(df)
        habilidades_cols = sorted([col for col in df.columns if col.startswith('H') and col[1:].replace(' ', '').isdigit()])
        
        st.sidebar.success(f"✅ Arquivo carregado com {len(df)} alunos.")
        
        st.sidebar.header("⚙️ 2. Filtros e Configurações")
        
        if turma_col:
            turmas_disponiveis = sorted(df[turma_col].unique())
            turmas_selecionadas = st.sidebar.multiselect(
                "Selecione as turmas:",
                turmas_disponiveis,
                default=turmas_disponiveis[0] if turmas_disponiveis else []
            )
        else:
            st.sidebar.warning("Coluna 'Turma' não encontrada.")
            turmas_selecionadas = []

        opcoes_habilidades = {f"{h} - {get_descricao_habilidade(h, arquivo_selecionado)}": h for h in habilidades_cols}
        habilidades_formatadas_selecionadas = st.sidebar.multiselect(
            "Selecione as habilidades foco:",
            opcoes_habilidades.keys(),
            default=list(opcoes_habilidades.keys())
        )
        habilidades_selecionadas = [opcoes_habilidades[desc] for desc in habilidades_formatadas_selecionadas]
        
        max_alunos_por_grupo = st.sidebar.slider(
            "Máximo de alunos por grupo:",
            min_value=2, max_value=10, value=4
        )
        
        if st.sidebar.button("🚀 Gerar Grupos", type="primary", use_container_width=True):
            if not turmas_selecionadas:
                st.error("Por favor, selecione pelo menos uma turma.")
            elif not habilidades_selecionadas:
                st.error("Por favor, selecione pelo menos uma habilidade.")
            else:
                for turma in turmas_selecionadas:
                    st.subheader(f"Turma: {turma}", divider="rainbow")
                    
                    df_turma = df[df[turma_col] == turma]
                    
                    if df_turma.empty:
                        st.warning("Nenhum aluno encontrado para esta turma.")
                        continue
                        
                    with st.spinner(f"Formando grupos para a turma {turma}..."):
                        grupos = formar_grupos_por_niveis(df_turma, habilidades_selecionadas, max_alunos_por_grupo)
                        
                        if not grupos:
                            st.info("Não foi possível formar grupos para esta turma.")
                            continue

                        num_colunas = 2
                        colunas = st.columns(num_colunas)
                        
                        for i, grupo in enumerate(grupos, 1):
                            coluna_atual = colunas[(i - 1) % num_colunas]
                            with coluna_atual:
                                with st.expander(f"👥 Grupo {i} ({len(grupo)} alunos)", expanded=True):
                                    st.markdown("**🧑‍🎓 Integrantes:**")
                                    for aluno in grupo:
                                        st.write(f"- {aluno[aluno_col]}")
                                    
                                    st.markdown("---")
                                    
                                    pontuacoes = calcular_pontuacao_grupo(grupo, habilidades_selecionadas)
                                    
                                    fig = go.Figure()
                                    fig.add_trace(go.Bar(
                                        x=list(pontuacoes.keys()),
                                        y=list(pontuacoes.values()),
                                        text=[f"{v:.2f}" for v in pontuacoes.values()],
                                        textposition='auto',
                                        marker_color='#00796b'
                                    ))
                                    fig.update_layout(
                                        title_text='<b>Desempenho Médio do Grupo</b>',
                                        xaxis_title="Habilidades",
                                        yaxis_title="Pontuação Média",
                                        yaxis_range=[0, 2],
                                        height=300,
                                        margin=dict(l=20, r=20, t=40, b=20)
                                    )
                                    # AQUI ESTÁ A CORREÇÃO!
                                    st.plotly_chart(fig, use_container_width=True, key=f"chart_{turma}_{i}")

                                    pontos_fortes = [h for h, m in pontuacoes.items() if m >= 1.5]
                                    pontos_atencao = [h for h, m in pontuacoes.items() if m < 0.8]

                                    if pontos_fortes:
                                        st.success(f"**Pontos Fortes:** {', '.join(pontos_fortes)}")
                                    if pontos_atencao:
                                        st.warning(f"**Pontos de Atenção:** {', '.join(pontos_atencao)}")
# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 14px;">
    <p>Colégio Estadual São Braz - Recomposição da Aprendizagem</p>
    <p>© 2025 - Todos os direitos reservados</p>
    <p>© Desenvolvido por Mauricio A. Ribeiro</p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()