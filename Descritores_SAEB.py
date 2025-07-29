import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def per_aluno(A, B):
    p = (A / B) * 100
    return p


# Configuração da página com estilo melhorado
st.set_page_config(
    page_title="SAEB Analytics",
    page_icon=":book:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/MauricioRibeiroTech',
        'Report a bug': "https://github.com/MauricioRibeiroTech",
        'About': "# Aplicativo para os Índices dos Simulados do SAEB-HD"
    }
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
    h1, h2, h3 {
        color: #2c3e50;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar melhorada
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #2c3e50; font-size: 24px;">Simulados SAEB 2025</h1>
        <h2 style="color: #3498db; font-size: 18px;">Escola Estadual Helena Dionysio</h2>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("main.py", label="🏠 Página Inicial")
    st.page_link("pages/3_Relatorios_Mensais.py", label="📅 Relatório Mensal")
    st.page_link("pages/Descritores_SAEB.py", label="📊 Relatório SAEB Descritores")
    st.page_link("pages/1_SAEB_Metodologia.py", label="📈 Desempenho percentual")

    with st.container():
        st.markdown("### Configurações do Relatório")
        try:
            # Corrigido o nome do arquivo para "descritores.csv"
            df = pd.read_csv("pages/descritores2.csv", sep=";")

            # Verifica se as colunas necessárias existem
            if 'Simulados' not in df.columns or 'Componentes' not in df.columns:
                st.error("O arquivo CSV não contém as colunas necessárias ('Simulados' e 'Componentes')")
                st.stop()

            salas_distintas = df["Simulados"].unique().tolist()
            if not salas_distintas:
                st.error("Nenhum simulado encontrado no arquivo CSV")
                st.stop()

            salas_selecionadas = st.selectbox("Selecione o Simulado", salas_distintas)
            componente_selecionada = st.radio("Componente Curricular", ["Matematica", "Portugues"])

            if componente_selecionada:
                df = df[df["Simulados"] == salas_selecionadas]
                df = df[df["Componentes"] == componente_selecionada]

                if df.empty:
                    st.error("Nenhum dado encontrado para a combinação selecionada")
                    st.stop()

        except FileNotFoundError:
            st.error(
                "Arquivo 'descritores.csv' não encontrado. Por favor, verifique se o arquivo está no diretório correto.")
            st.stop()
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")
            st.stop()

    st.markdown("---")
    st.markdown("### Links Importantes")
    col1, col2 = st.columns(2)
    with col1:
        st.page_link(
            "https://download.inep.gov.br/educacao_basica/prova_brasil_saeb/menu_do_professor/o_que_cai_nas_provas/Matriz_de_Referencia_de_Matematica.pdf",
            label="Matemática", icon="📊")
    with col2:
        st.page_link(
            "https://download.inep.gov.br/educacao_basica/prova_brasil_saeb/menu_do_professor/o_que_cai_nas_provas/Matriz_de_Referencia_de_Lingua_Portuguesa.pdf",
            label="Português", icon="📚")

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p style="color: #7f8c8d; font-size: 14px;">Desenvolvido por Mauricio A. Ribeiro</p>
        <p style="color: #7f8c8d; font-size: 12px;">mau.ap.ribeiro@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

# Conteúdo principal
st.markdown(f"""
<div style="background-color: #3498db; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; text-align: center; margin: 0;">Relatório de {componente_selecionada}</h1>
    <h2 style="color: white; text-align: center; margin: 0;">Simulado: {salas_selecionadas} (Descritores)</h2>
</div>
""", unsafe_allow_html=True)

try:
    # Processamento dos dados com tratamento de erros
    df1 = df.iloc[:, 3:38].copy()
    num_NaN = df1.iloc[0].isna().sum() if len(df1) > 0 else 0
    Num_descritores_contemplados = len(df1.columns) - num_NaN

    df_alunos = df.iloc[:, 0].copy()
    Num_alunos = len(df_alunos)

    if Num_alunos == 0:
        st.warning("Nenhum aluno encontrado para os filtros selecionados")
        st.stop()

    df_analise_alunos = pd.DataFrame()
    df_descritores = pd.DataFrame()

    # Calcular porcentagens com tratamento para divisão por zero
    df2 = df1.sum(axis=1)
    df_analise_alunos['Nomes'] = df_alunos
    df_analise_alunos['Porcentagem'] = df2.apply(
        lambda x: (x / Num_descritores_contemplados * 100) if Num_descritores_contemplados > 0 else 0)

    df_acima_de_60 = df_analise_alunos[df_analise_alunos['Porcentagem'] >= 60]

    # Preparar dados de descritores
    df_descritores['Descritor'] = df1.columns.tolist()
    df_descritores['Porcentagem'] = df1.sum(axis=0).tolist()
    df_descritores['Porcentagem'] = df_descritores['Porcentagem'].apply(
        lambda x: (x / Num_alunos * 100) if Num_alunos > 0 else 0)
    df_descritores_mean = df_descritores[df_descritores['Porcentagem'] != 0.0]

    # Gráficos interativos com Plotly melhorados
    st.markdown("## 📊 Desempenho dos Alunos")
    if not df_analise_alunos.empty:
        fig_alunos = px.bar(df_analise_alunos,
                            x='Nomes',
                            y='Porcentagem',
                            color='Porcentagem',
                            color_continuous_scale='Viridis',
                            text='Porcentagem',
                            labels={'Porcentagem': 'Desempenho (%)', 'Nomes': 'Alunos'},
                            height=500,
                            template='plotly_white')

        # Adicionando linha de média e meta
        media_alunos = df_analise_alunos['Porcentagem'].mean()
        fig_alunos.add_hline(y=media_alunos, line_dash="dot",
                             line_color="red",
                             annotation_text=f"Média: {media_alunos:.1f}%",
                             annotation_position="bottom right")
        fig_alunos.add_hline(y=60, line_dash="dash",
                             line_color="green",
                             annotation_text="Meta: 60%",
                             annotation_position="top right")

        fig_alunos.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_alunos.update_layout(
            xaxis_tickangle=-45,
            yaxis_range=[0, 100],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified",
            title={
                'text': f"Desempenho Individual - {salas_selecionadas}",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        st.plotly_chart(fig_alunos, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de desempenho dos alunos")

    # Gráfico de descritores com subplots
    st.markdown(f"## 📈 Desempenho por Descritor - {salas_selecionadas}")

    if not df_descritores_mean.empty:
        # Criando subplots
        fig_descritores = make_subplots(rows=1, cols=2,
                                        specs=[[{"type": "bar"}, {"type": "pie"}]],
                                        column_widths=[0.7, 0.3],
                                        subplot_titles=('Desempenho por Descritor', 'Distribuição de Desempenho'))

        # Gráfico de barras
        fig_descritores.add_trace(
            go.Bar(
                x=df_descritores_mean['Porcentagem'],
                y=df_descritores_mean['Descritor'],
                orientation='h',
                marker=dict(
                    color=df_descritores_mean['Porcentagem'],
                    colorscale='Plasma',
                    showscale=True
                ),
                text=df_descritores_mean['Porcentagem'].round(1).astype(str) + '%',
                textposition='auto',
                hoverinfo='text',
                name='Desempenho'
            ),
            row=1, col=1
        )

        # Gráfico de pizza (distribuição)
        bins = [0, 30, 60, 80, 100]
        labels = ['0-30%', '30-60%', '60-80%', '80-100%']
        df_descritores_mean['Categoria'] = pd.cut(df_descritores_mean['Porcentagem'], bins=bins, labels=labels)
        distribuicao = df_descritores_mean['Categoria'].value_counts().sort_index()

        fig_descritores.add_trace(
            go.Pie(
                labels=distribuicao.index,
                values=distribuicao.values,
                hole=.4,
                marker=dict(colors=['#EF553B', '#00CC96', '#636EFA', '#AB63FA']),
                hoverinfo='label+percent',
                textinfo='percent',
                name='Distribuição'
            ),
            row=1, col=2
        )

        # Atualizando layout
        fig_descritores.update_layout(
            height=600,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title={
                'text': f"Análise por Descritor - {salas_selecionadas}",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

        fig_descritores.update_yaxes(autorange="reversed", row=1, col=1)
        st.plotly_chart(fig_descritores, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de descritores")

    # Métricas em colunas com KPI cards
    st.markdown("## 📌 Indicadores Principais")
    col1, col2, col3, col4 = st.columns(4)

    media_descritores = df_descritores_mean['Porcentagem'].mean().round(2) if not df_descritores_mean.empty else 0
    dif1 = media_descritores - 60
    media_alunos = df_analise_alunos['Porcentagem'].mean().round(2) if not df_analise_alunos.empty else 0
    dif2 = media_alunos - 60
    alunos_acima_meta = len(df_acima_de_60)
    perc_acima_meta = (alunos_acima_meta / Num_alunos) * 100 if Num_alunos > 0 else 0

    with col1:
        st.markdown("""
        <div style="background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h3 style="color: #2c3e50; margin-top: 0;">Média Descritores</h3>
            <h1 style="color: #3498db; margin-bottom: 5px;">{:.1f}%</h1>
            <p style="color: {}; margin-bottom: 0;">{}{:.1f}% vs meta</p>
        </div>
        """.format(
            media_descritores,
            "#e74c3c" if dif1 < 0 else "#2ecc71",
            "▼ " if dif1 < 0 else "▲ ",
            abs(dif1)
        ), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h3 style="color: #2c3e50; margin-top: 0;">Média Alunos</h3>
            <h1 style="color: #3498db; margin-bottom: 5px;">{:.1f}%</h1>
            <p style="color: {}; margin-bottom: 0;">{}{:.1f}% vs meta</p>
        </div>
        """.format(
            media_alunos,
            "#e74c3c" if dif2 < 0 else "#2ecc71",
            "▼ " if dif2 < 0 else "▲ ",
            abs(dif2))
            , unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h3 style="color: #2c3e50; margin-top: 0;">Alunos acima da meta</h3>
            <h1 style="color: #3498db; margin-bottom: 5px;">{}</h1>
            <p style="color: #2c3e50; margin-bottom: 0;">{:.1f}% da turma</p>
        </div>
        """.format(alunos_acima_meta, perc_acima_meta), unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style="background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h3 style="color: #2c3e50; margin-top: 0;">Descritores avaliados</h3>
            <h1 style="color: #3498db; margin-bottom: 5px;">{}</h1>
            <p style="color: #2c3e50; margin-bottom: 0;">Total de alunos: {}</p>
        </div>
        """.format(Num_descritores_contemplados, Num_alunos), unsafe_allow_html=True)

    # Tabelas com estilo melhorado
    if not df_acima_de_60.empty:
        st.markdown(f"## 🏆 Melhores Alunos - {salas_selecionadas}")
        st.dataframe(
            df_acima_de_60.round(2).style
            .background_gradient(cmap='Greens', subset=['Porcentagem'])
            .format({'Porcentagem': '{:.1f}%'})
            .set_properties(**{'text-align': 'center'})
            .set_table_styles([{
                'selector': 'th',
                'props': [('background-color', '#3498db'),
                          ('color', 'white'),
                          ('text-align', 'center')]
            }]),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("Nenhum aluno atingiu a meta de 60% ou mais")

    if not df_descritores_mean.empty:
        st.markdown(f"## 📋 Descritores por Desempenho - {salas_selecionadas}")
        st.dataframe(
            df_descritores_mean.sort_values('Porcentagem', ascending=False)
            .round(2).style
            .background_gradient(cmap='Purples', subset=['Porcentagem'])
            .format({'Porcentagem': '{:.1f}%'})
            .set_properties(**{'text-align': 'center'})
            .set_table_styles([{
                'selector': 'th',
                'props': [('background-color', '#3498db'),
                          ('color', 'white'),
                          ('text-align', 'center')]
            }]),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("Nenhum dado disponível para exibir a tabela de descritores")

except Exception as e:
    st.error(f"Ocorreu um erro ao processar os dados: {str(e)}")