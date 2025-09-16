import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import plotly.graph_objects as go
import plotly.express as px

# --- Configuração da Página e Estilo ---
st.set_page_config(
    page_title="Painel de Recomposição - CESB Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS para uma apresentação mais elegante ---
st.markdown("""
<style>
    /* Estilo para o container do expander (card do grupo) */
    .st-expander {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.05);
        transition: 0.3s;
        margin-bottom: 20px;
    }
    .st-expander:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.1);
        border: 1px solid #004d40;
    }
    /* Estilo para o cabeçalho do expander */
    .st-expander header {
        font-size: 1.3rem;
        font-weight: bold;
        color: #ffffff;
        background-color: #004d40;
        border-radius: 8px 8px 0 0;
    }
    /* Estilo para o ícone do expander */
    .st-expander header svg {
        fill: #ffffff;
    }
</style>
""", unsafe_allow_html=True)


# --- Dicionário de Habilidades Unificado ---
DESCRICOES_HABILIDADES = {
    "CAED1_9_matematica": {
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
    "CAED2_9_matematica": {
        "H01":"Corresponder figuras tridimensionais às suas planificações.",
        "H02":"Utilizar informações apresentadas em tabelas ou gráficos na resolução de problemas.",
        "H03":"Utilizar área de figuras bidimensionais na resolução de problema.",
        "H04":"Corresponder números racionais a pontos da reta numérica.",
        "H05":"Identificar frações equivalentes.",
        "H06":"Reconhecer fração como representação associada a diferentes significados.",
        "H07":"Utilizar conversão entre unidades de medida, na resolução de problema.",
        "H08":"Utilizar proporcionalidade entre duas grandezas na resolução de problema.",
        "H09":"Classificar quadriláteros por meio de suas propriedades.",
        "H10":"Classificar triângulos por meio de suas propriedades.",
        "H11":"Corresponder pontos do plano a pares ordenados em um sistema de coordenadas cartesianas.",
        "H12":"Utilizar perímetro de figuras bidimensionais na resolução de problema.",
        "H13":"Utilizar porcentagem na resolução de problemas.",
        "H14":"Corresponder números inteiros a pontos da reta numérica.",
        "H15":"Identificar a expressão algébrica que expressa uma regularidade observada em sequência de números ou figuras (padrões).",
        "H16":"Utilizar o cálculo do valor numérico de expressões algébricas na resolução de problemas.",
        "H17":"Utilizar relações métricas de um triângulo retângulo na resolução de problema.",
        "H18":"Corresponder um sistema de equações polinomiais de 1º grau à uma situação problema descrita textualmente.",
        "H19":"Utilizar equação polinomial de 2º grau na resolução de problema.",
        "H20":"Efetuar cálculos simples com valores aproximados de radicais.",
        "H21":"Utilizar números racionais, envolvendo diferentes significados das operações, na resolução de problemas.",
        "H22":"Identificar uma equação ou inequação do 1º grau que expressa um problema."
    },
    "CAED1_9_portugues": {
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
        "H11": "Reconhecer o sentido das relações lógico-discursivas em anexo.",
        "H12": "Reconhecer o efeito de sentido decorrente da escolha de uma determinada palavra or expressão.",
        "H13": "Estabelecer relação entre a tese e os argumentos oferecidos para sustentá-la.",
        "H14": "Reconhecer o efeito de sentido decorrente da exploração de recursos ortográficos e/ou morfossintáticos.",
        "H15": "Identificar as marcas linguísticas que evidenciam o locutor e o interlocutor de um texto.",
    },
    "CAED2_9_portugues": { # Supondo que sejam as mesmas de CAED1, ajuste se necessário
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
        "H11": "Reconhecer o sentido das relações lógico-discursivas em anexo.",
        "H12": "Reconhecer o efeito de sentido decorrente da escolha de uma determinada palavra or expressão.",
        "H13": "Estabelecer relação entre a tese e os argumentos oferecidos para sustentá-la.",
        "H14": "Reconhecer o efeito de sentido decorrente da exploração de recursos ortográficos e/ou morfossintáticos.",
        "H15": "Identificar as marcas linguísticas que evidenciam o locutor e o interlocutor de um texto.",
    }
}

# --- Funções Utilitárias ---

@st.cache_data
def carregar_dados(nome_arquivo):
    """Carrega um arquivo CSV com tratamento de erros e encoding."""
    try:
        # Tenta encontrar o arquivo na mesma pasta do script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, nome_arquivo)
        
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(csv_path, sep=';', encoding='latin-1')
            
            df.columns = df.columns.str.strip()
            return df
        else:
            # st.error(f"Arquivo '{nome_arquivo}' não encontrado.") # Removido para não poluir a tela inicial
            return None
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo '{nome_arquivo}': {e}")
        return None

def encontrar_colunas_info(df):
    """Encontra as colunas de aluno e turma no DataFrame."""
    aluno_col, turma_col = None, None
    for col in df.columns:
        col_lower = col.lower()
        if 'aluno' in col_lower or 'nome' in col_lower or 'estudante' in col_lower:
            aluno_col = col
        if 'turma' in col_lower or 'classe' in col_lower:
            turma_col = col
    if aluno_col is None and len(df.columns) > 0: aluno_col = df.columns[0]
    if turma_col is None and len(df.columns) > 1: turma_col = df.columns[1]
    return aluno_col, turma_col

def get_descricao_habilidade(codigo, avaliacao_selecionada):
    """Obtém a descrição da habilidade com base na avaliação."""
    return DESCRICOES_HABILIDADES.get(avaliacao_selecionada, {}).get(codigo.strip(), "N/A")

# --- Lógica de Geração de Grupos ---

def formar_grupos_heterogeneos(alunos_df, habilidades_selecionadas, max_por_grupo, aluno_col):
    """Forma grupos heterogêneos priorizando um núcleo com diferentes níveis de domínio."""
    if alunos_df.empty or not habilidades_selecionadas:
        return []

    alunos_list = alunos_df.to_dict('records')
    alunos_por_nivel = {0: [], 1: [], 2: []}

    for aluno in alunos_list:
        pontuacoes = [aluno.get(hab, 0) for hab in habilidades_selecionadas if pd.notna(aluno.get(hab))]
        media = np.mean(pontuacoes) if pontuacoes else 0
        aluno['media_habilidades'] = media
        
        if media < 0.8: alunos_por_nivel[0].append(aluno)
        elif media < 1.6: alunos_por_nivel[1].append(aluno)
        else: alunos_por_nivel[2].append(aluno)

    for nivel in alunos_por_nivel:
        random.shuffle(alunos_por_nivel[nivel])
    
    num_total_alunos = len(alunos_list)
    num_grupos = max(1, (num_total_alunos + max_por_grupo - 1) // max_por_grupo)
    grupos = [[] for _ in range(num_grupos)]
    
    # Etapa 1: Formar o núcleo heterogêneo
    grupo_idx = 0
    while all(len(v) > 0 for v in alunos_por_nivel.values()):
        if len(grupos[grupo_idx]) < max_por_grupo: grupos[grupo_idx].append(alunos_por_nivel[2].pop())
        if len(grupos[grupo_idx]) < max_por_grupo: grupos[grupo_idx].append(alunos_por_nivel[1].pop())
        if len(grupos[grupo_idx]) < max_por_grupo: grupos[grupo_idx].append(alunos_por_nivel[0].pop())
        grupo_idx = (grupo_idx + 1) % num_grupos

    # Etapa 2: Distribuir os alunos restantes
    alunos_restantes = [aluno for nivel in sorted(alunos_por_nivel.keys(), reverse=True) for aluno in alunos_por_nivel[nivel]]
    
    while alunos_restantes:
        grupos.sort(key=len)
        grupo_alvo = next((g for g in grupos if len(g) < max_por_grupo), None)
        if grupo_alvo is not None:
            grupo_alvo.append(alunos_restantes.pop(0))
        else: break
            
    return [g for g in grupos if g]

def analisar_composicao_grupos(grupos):
    """Cria um DataFrame com a composição de cada grupo."""
    composicao = []
    for i, grupo in enumerate(grupos, 1):
        niveis = {0: 0, 1: 0, 2: 0}
        for aluno in grupo:
            media = aluno.get('media_habilidades', 0)
            if media < 0.8: niveis[0] += 1
            elif media < 1.6: niveis[1] += 1
            else: niveis[2] += 1
        composicao.append({
            'Grupo': i,
            'Não Domina': niveis[0],
            'Domina': niveis[1],
            'Domina Plenamente': niveis[2],
            'Total': len(grupo)
        })
    return pd.DataFrame(composicao).set_index('Grupo')


# --- Funções para Renderizar as Páginas ---

def render_visao_geral(df_filtrado, habilidades_cols, avaliacao_selecionada, turmas_selecionadas, turma_col):
    """Renderiza a página de Visão Geral com estatísticas agregadas."""
    st.header("📈 Visão Geral da Turma")
    st.markdown("Análise consolidada do desempenho nas habilidades, destacando pontos fortes e de atenção.")

    if not habilidades_cols:
        st.warning("Nenhuma coluna de habilidade (H01, H02, etc.) foi encontrada no arquivo carregado.")
        return

    st.subheader("Habilidades com Maior e Menor Domínio")
    dominio_por_habilidade = []
    for hab in habilidades_cols:
        # Domínio é considerado quando a pontuação é maior que 0
        dominio = (df_filtrado[hab] > 0).mean() * 100
        dominio_por_habilidade.append({
            "Habilidade": hab,
            "Domínio (%)": dominio,
            "Descrição": get_descricao_habilidade(hab, avaliacao_selecionada)
        })
    
    df_dominio = pd.DataFrame(dominio_por_habilidade).sort_values("Domínio (%)", ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**✅ Top 5 - Maior Domínio**")
        st.dataframe(df_dominio.head(5), hide_index=True, use_container_width=True)
    with col2:
        st.write("**❌ Top 5 - Menor Domínio**")
        st.dataframe(df_dominio.tail(5).sort_values("Domínio (%)", ascending=True), hide_index=True, use_container_width=True)

    # --- INÍCIO DA ALTERAÇÃO ---
    st.subheader("Comparativo de Desempenho por Habilidade e Turma")
    desempenho_data = []
    for turma in turmas_selecionadas:
        df_turma = df_filtrado[df_filtrado[turma_col] == turma]
        for hab in habilidades_cols:
            dominio = (df_turma[hab] > 0).mean() * 100
            desempenho_data.append({"Turma": turma, "Habilidade": hab, "Domínio (%)": dominio})
    
    df_desempenho = pd.DataFrame(desempenho_data)
    if not df_desempenho.empty:
        fig = px.bar(
            df_desempenho,
            x="Habilidade",
            y="Domínio (%)",
            color="Turma",
            barmode='group',
            labels={'Domínio (%)': 'Percentual de Domínio', 'Habilidade': 'Habilidades'},
            title="Percentual de Domínio por Habilidade entre as Turmas",
            text_auto='.0f'  # Adiciona o valor percentual (formatado como inteiro) em cima da barra
        )
        fig.update_layout(
            yaxis_range=[0, 105],  # Deixa um espaço no topo do gráfico
            legend_title_text='Turmas',
            title_x=0.5 # Centraliza o título
        )
        fig.update_traces(
            textangle=0, 
            textposition='outside' # Garante que o texto fique fora da barra
        )
        st.plotly_chart(fig, use_container_width=True)
    # --- FIM DA ALTERAÇÃO ---


def render_analise_individual(df_filtrado, habilidades_cols, avaliacao_selecionada, aluno_col):
    """Renderiza a página de Análise Individual com o gráfico de radar."""
    st.header("🧑‍🎓 Análise Individual por Aluno")
    
    alunos_disponiveis = sorted(df_filtrado[aluno_col].unique())
    aluno_selecionado = st.selectbox("Selecione um aluno:", alunos_disponiveis)
    
    if aluno_selecionado:
        aluno_data = df_filtrado[df_filtrado[aluno_col] == aluno_selecionado].iloc[0]
        
        st.subheader(f"Perfil de Habilidades de {aluno_selecionado}")

        # --- CORREÇÃO APLICADA AQUI ---
        # Verifica se a lista de habilidades não está vazia antes de criar o gráfico
        if not habilidades_cols:
            st.warning("Não foram encontradas habilidades para gerar o gráfico de radar.")
            return

        valores = [aluno_data.get(hab, 0) for hab in habilidades_cols]
        
        # Gráfico de Radar
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=valores + [valores[0]], # Adiciona o primeiro valor no final para fechar o radar
            theta=habilidades_cols + [habilidades_cols[0]], # Idem para o theta
            fill='toself',
            name='Desempenho',
            line_color='royalblue'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 2])),
            title=f"Radar de Desempenho - {aluno_selecionado}",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detalhes das habilidades em colunas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.error("❌ Não Domina (Nota 0)")
            for hab in [h for h in habilidades_cols if aluno_data.get(h, 0) == 0]:
                st.write(f"**{hab}**: {get_descricao_habilidade(hab, avaliacao_selecionada)}")
        with col2:
            st.warning("⚠️ Domina (Nota 1)")
            for hab in [h for h in habilidades_cols if aluno_data.get(h, 0) == 1]:
                 st.write(f"**{hab}**: {get_descricao_habilidade(hab, avaliacao_selecionada)}")
        with col3:
            st.success("✅ Domina Plenamente (Nota 2)")
            for hab in [h for h in habilidades_cols if aluno_data.get(h, 0) >= 2]:
                 st.write(f"**{hab}**: {get_descricao_habilidade(hab, avaliacao_selecionada)}")

def render_gerador_grupos(df_filtrado, habilidades_cols, avaliacao_selecionada, aluno_col):
    """Renderiza a página do Gerador de Grupos."""
    st.header("👥 Gerador de Grupos Pedagógicos")
    st.markdown("Selecione as **habilidades foco** para criar grupos de trabalho heterogêneos e equilibrados.")
    
    if not habilidades_cols:
        st.warning("Nenhuma coluna de habilidade (H01, H02, etc.) foi encontrada para formar grupos.")
        return

    opcoes_habilidades = {f"{h.strip()} - {get_descricao_habilidade(h, avaliacao_selecionada)}": h for h in habilidades_cols}
    habilidades_formatadas = st.multiselect(
        "Selecione as habilidades foco:",
        options=opcoes_habilidades.keys(),
        default=list(opcoes_habilidades.keys())[:3] if opcoes_habilidades else []
    )
    habilidades_selecionadas = [opcoes_habilidades[desc] for desc in habilidades_formatadas]
    
    max_alunos_por_grupo = st.slider("Máximo de alunos por grupo:", 2, 8, 4)
    
    if st.button("🚀 Gerar Grupos", type="primary", use_container_width=True):
        if not habilidades_selecionadas:
            st.error("Por favor, selecione pelo menos uma habilidade foco.")
        elif df_filtrado.empty:
            st.warning("Nenhum aluno selecionado no filtro de turmas.")
        else:
            with st.spinner("Analisando perfis e formando os melhores grupos..."):
                grupos = formar_grupos_heterogeneos(df_filtrado, habilidades_selecionadas, max_alunos_por_grupo, aluno_col)
                
                if not grupos:
                    st.info("Não foi possível formar grupos com os alunos selecionados.")
                    return

                st.markdown("---")
                st.subheader("📊 Composição dos Grupos")
                composicao_df = analisar_composicao_grupos(grupos)
                st.dataframe(
                    composicao_df.style.background_gradient(cmap='Greens'),
                    use_container_width=True
                )

                st.subheader("📋 Detalhes dos Grupos Formados")
                num_colunas = 2 
                colunas = st.columns(num_colunas)
                
                for i, grupo in enumerate(grupos):
                    col = colunas[i % num_colunas]
                    with col:
                        with st.expander(f"Grupo {i+1} ({len(grupo)} alunos)", expanded=True):
                            st.markdown("**🧑‍🎓 Integrantes:**")
                            for aluno in sorted(grupo, key=lambda x: x['media_habilidades'], reverse=True):
                                if aluno['media_habilidades'] < 0.8: nivel_str = "❌ Não Domina"
                                elif aluno['media_habilidades'] < 1.6: nivel_str = "✅ Domina"
                                else: nivel_str = "🎯 Domina Plenamente"
                                st.markdown(f"- **{aluno[aluno_col]}** (*{nivel_str}*)")

                            # Gráfico de desempenho do grupo
                            pontuacoes = pd.DataFrame(grupo)[habilidades_selecionadas].mean().to_dict()
                            fig = go.Figure(go.Bar(
                                x=list(pontuacoes.keys()), y=list(pontuacoes.values()),
                                text=[f"{v:.2f}" for v in pontuacoes.values()],
                                textposition='auto', marker_color='#00796b'
                            ))
                            fig.update_layout(
                                title_text='<b>Desempenho Médio do Grupo</b>', yaxis_range=[0, 2.1], height=300,
                                margin=dict(l=20, r=20, t=40, b=20), title_font_size=16
                            )
                            st.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")


# --- Aplicação Principal ---
def main():
    st.sidebar.title("Painel de Controle")
   
    # --- Seleção de Dados ---
    mapa_avaliacoes = {
        "CAED 1 - Matemática 9º Ano": "CAED1_9_matematica",
        "CAED 2 - Matemática 9º Ano": "CAED2_9_matematica",
        "CAED 1 - Português 9º Ano": "CAED1_9_portugues",
        "CAED 2 - Português 9º Ano": "CAED2_9_portugues",
    }
    
    avaliacao_label = st.sidebar.selectbox(
        "Selecione a Avaliação:",
        options=list(mapa_avaliacoes.keys())
    )
    avaliacao_selecionada = mapa_avaliacoes[avaliacao_label]
    nome_arquivo = f"{avaliacao_selecionada}.csv"
    
    df = carregar_dados(nome_arquivo)

    if df is not None:
        aluno_col, turma_col = encontrar_colunas_info(df)
        habilidades_cols = sorted([col for col in df.columns if col.strip().startswith('H') and col.strip()[1:].isdigit()], 
                                  key=lambda x: int(x.strip()[1:]))

        st.sidebar.markdown("---")
        
        # --- Filtro de Turma ---
        turmas_disponiveis = sorted(df[turma_col].astype(str).unique())
        turmas_selecionadas = st.sidebar.multiselect(
            "Filtro de Turmas:",
            options=turmas_disponiveis,
            default=turmas_disponiveis
        )
        df_filtrado = df[df[turma_col].isin(turmas_selecionadas)]

        st.sidebar.info(f"**{len(df_filtrado)}** alunos selecionados em **{len(turmas_selecionadas)}** turmas.")
        st.sidebar.markdown("---")

        # --- Navegação ---
        paginas = {
            "Visão Geral": render_visao_geral,
            "Análise Individual": render_analise_individual,
            "Gerador de Grupos": render_gerador_grupos,
        }
        pagina_selecionada = st.sidebar.radio("Selecione a Análise:", options=list(paginas.keys()))

        # --- Título Principal Dinâmico ---
        st.title(f"Recomposição de Aprendizagem - {pagina_selecionada}")
        st.markdown(f"**Avaliação:** {avaliacao_label}")
        st.markdown("---")

        # --- Renderiza a página selecionada ---
        if not df_filtrado.empty:
            if pagina_selecionada == "Visão Geral":
                paginas[pagina_selecionada](df_filtrado, habilidades_cols, avaliacao_selecionada, turmas_selecionadas, turma_col)
            else: 
                paginas[pagina_selecionada](df_filtrado, habilidades_cols, avaliacao_selecionada, aluno_col)
        else:
            st.warning("Nenhum aluno corresponde aos filtros selecionados. Por favor, ajuste o filtro de turmas na barra lateral.")
    else:
        st.warning(f"Não foi possível carregar os dados. Verifique se o arquivo **{nome_arquivo}** está na mesma pasta do seu script.")

    # --- Rodapé ---
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 14px;">
        <p>© 2025 - Todos os direitos reservados</p>
        <p>Desenvolvido por Mauricio A. Ribeiro</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()