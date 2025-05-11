import streamlit as st
from PIL import Image
import os
# Configurações da página
try:
    st.set_page_config(
        page_title="SAEB Analytics",
        page_icon=":book:",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception as e:
    st.warning(f"Erro na configuração da página: {str(e)}")

# CSS personalizado com fallback
custom_css = """
<style>
    .main {
        background-color: #f8f9fa;
    }
    .header {
        background-color: #3498db;
        padding: 3rem;
        border-radius: 10px;
        margin-bottom: 2rem;
      }
    .feature-card {
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .st-emotion-cache-1v0mbdj {
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar de navegação
with st.sidebar:
    try:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2c3e50; font-size: 24px;">SAEB Analytics</h1>
            <h2 style="color: #3498db; font-size: 18px;">Escola Estadual Helena Dionysio</h2>
        </div>
        """, unsafe_allow_html=True)

        # Menu de navegação
        st.page_link("main.py", label="🏠 Página Inicial")
        st.page_link("pages/3_Relatorios_Mensais.py", label="📅 Relatório Mensal")
        st.page_link("pages/2_SAEB_Descritores.py", label="📊 Relatório SAEB Descritores")
        st.page_link("pages/1_SAEB_Metodologia.py", label="📈 Desempenho percentual")


        #st.markdown("---")
        #st.markdown("### Professor Responsável")
        #st.markdown("👨‍🏫 **Mauricio A. Ribeiro**")

        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <p style="color: #7f8c8d; font-size: 14px;">Desenvolvido por Mauricio A. Ribeiro</p>
            <p style="color: #7f8c8d; font-size: 12px;">mau.ap.ribeiro@gmail.com</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro na barra lateral: {str(e)}")

# Conteúdo principal
try:
    st.markdown("""
    <div class="header">
        <h1 style="color: white; text-align: center; margin: 0;">SAEB Analytics</h1>
        <h2 style="color: white; text-align: center; margin: 0;">Plataforma de Análise Educacional</h2>
    </div>
    """, unsafe_allow_html=True)

    # Introdução
    st.markdown("""
    Bem-vindo à plataforma **SAEB Analytics**, uma solução completa para análise e acompanhamento 
    do desempenho educacional nos simulados SAEB. Esta ferramenta foi desenvolvida para fornecer 
    insights valiosos sobre o progresso dos alunos e auxiliar na tomada de decisões pedagógicas.
    """)

    # Seção de recursos
    st.markdown("## ✨ Recursos Principais")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📅 Relatório Mensal</h3>
            <p>Acompanhe o desempenho por simulado ao longo dos meses com gráficos interativos e análises comparativas.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Relatório SAEB</h3>
            <p>Análise detalhada por descritores e componentes curriculares com visualizações intuitivas.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📈 Análise de Desempenho</h3>
            <p>Identifique padrões, alunos destaque e áreas que precisam de reforço com métricas precisas.</p>
        </div>
        """, unsafe_allow_html=True)

   # Como usar
    st.markdown("## 📌 Como Utilizar")

    st.markdown("""
    1. **Navegue** entre os relatórios usando o menu lateral
    2. **Selecione** o componente curricular e turma desejada
    3. **Explore** os gráficos interativos
    4. **Exporte** os dados quando necessário
    5. **Utilize** os insights para planejamento pedagógico
    """)

    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 14px;">
        <p>Plataforma desenvolvida por Mauricio A. Ribeiro</p>
        <p>© 2025 SAEB Analytics - Todos os direitos reservados</p>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {str(e)}")
    st.info("Por favor, recarregue a página ou tente novamente mais tarde.")
