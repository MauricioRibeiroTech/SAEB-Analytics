# SAEB-Analytics

<p align="left">
Um aplicativo desenvolvido em Python utilizando as poderosas bibliotecas Streamlit, Pandas e NumPy para realizar a análise de dados de notas de simulados aplicados a alunos do nono ano, com foco na preparação para o Sistema de Avaliação da Educação Básica (SAEB) de 2025. Através de uma interface intuitiva e interativa, o aplicativo permite aos educadores e gestores obter *insights* valiosos sobre o desempenho dos estudantes, identificar áreas de força e fraqueza, e direcionar estratégias pedagógicas de forma mais eficaz. Para a coleta de dados e um monitoramento preciso do aprendizado, o aplicativo também se baseia no uso dos descritores, que detalham as habilidades e competências esperadas para os alunos do nono ano, permitindo um mapeamento granular do seu desenvolvimento.
Compreendendo a importância de alinhar as práticas avaliativas com as diretrizes curriculares estaduais, no Paraná, a Secretaria de Estado da Educação (SEED-PR) estabelece **descritores de ensino específicos** que detalham as expectativas de aprendizagem para cada componente curricular e ano de escolaridade. Esses descritores servem como um guia para os educadores, auxiliando no planejamento das aulas, na elaboração de instrumentos de avaliação e no monitoramento do desenvolvimento dos alunos. Ao integrar esses descritores paranaenses ao nosso aplicativo de análise, é possível refinar ainda mais a avaliação do desempenho dos alunos do nono ano em relação às habilidades e competências consideradas prioritárias no contexto educacional do estado, proporcionando insights mais alinhados com as necessidades e particularidades do sistema de ensino do Paraná. Essa integração garante que a análise dos simulados não apenas prepare para o SAEB 2025, mas também esteja intrinsecamente ligada ao currículo e às expectativas de aprendizagem definidas para os estudantes paranaenses.
</p>

## As Bibliotecas Python em Ação

A espinha dorsal deste aplicativo reside na utilização estratégica de três bibliotecas fundamentais do ecossistema Python para análise de dados:

* **[Streamlit](https://streamlit.io/)**: Esta biblioteca de código aberto simplifica drasticamente a criação de interfaces web interativas a partir de scripts Python puros. Com o Streamlit, é possível transformar *scripts* de análise de dados em aplicativos web compartilháveis com poucas linhas de código, sem a necessidade de conhecimento prévio em desenvolvimento web. No contexto deste aplicativo, o Streamlit é responsável por gerar a interface amigável onde os usuários podem carregar os dados dos simulados, interagir com filtros e visualizações, e obter os resultados da análise de forma clara e objetiva.
* **[Pandas](https://pandas.pydata.org/)**: O Pandas é uma biblioteca essencial para manipulação e análise de dados em Python. Ela fornece estruturas de dados de alto desempenho e fáceis de usar, como os *DataFrames*, que são tabelas bidimensionais com rótulos de linha e coluna. Neste aplicativo, o Pandas é crucial para:
    * **Carregar e limpar os dados** dos simulados, que podem estar em diversos formatos como CSV ou Excel.
    * **Estruturar e organizar os dados** em DataFrames para facilitar a análise, **incluindo a organização dos resultados por descritor**.
    * **Filtrar e selecionar subconjuntos de dados** com base em critérios específicos (por exemplo, turma, disciplina, descritor).
    * **Realizar cálculos estatísticos descritivos** como médias, medianas, desvios padrão, percentis, etc., **inclusive por descritor**.
    * **Agrupar e agregar dados** para obter *insights* sobre o desempenho de diferentes grupos de alunos **em relação a cada descritor**.
* **[NumPy](https://numpy.org/)**: NumPy (Numerical Python) é a biblioteca fundamental para computação numérica em Python. Ela fornece suporte para arrays multidimensionais e uma vasta coleção de funções matemáticas de alto nível otimizadas para operações com esses arrays. Embora o Pandas construa sobre o NumPy, ele é implicitamente utilizado em nosso aplicativo para:
    * **Realizar operações matemáticas eficientes** nos dados das notas **associadas a cada descritor**.
    * **Implementar cálculos estatísticos** subjacentes às funcionalidades do Pandas.
    * **Manipular arrays de dados** de forma rápida e eficaz.

### Funcionalidades Principais do Aplicativo

O aplicativo desenvolvido oferece um conjunto de funcionalidades projetadas para auxiliar na análise do desempenho dos alunos nos simulados do SAEB 2025:

* **Upload de Dados:** Uma interface simples para carregar os arquivos contendo as notas dos simulados, **incluindo informações sobre os descritores avaliados em cada questão**.
* **Visualização Tabular:** Apresentação dos dados carregados em formato de tabela para inspeção inicial, **com a possibilidade de visualizar o desempenho por descritor**.
* **Filtragem Interativa:** Possibilidade de filtrar os dados por turma, disciplina, **e também por descritor específico**, permitindo análises focadas em habilidades particulares.
* **Estatísticas Descritivas:** Cálculo e exibição de medidas estatísticas chave como média e listas de alunos acima da média limite, **e crucialmente, para cada descritor avaliado**.
* **Distribuição de Notas por Descritor:** Visualização da distribuição das notas para cada descritor através de gráficos, permitindo identificar o nível de domínio da turma em cada habilidade específica.
* **Análise por Habilidade (Descritor):** Análise detalhada do desempenho dos alunos em cada descritor individualmente, fornecendo *insights* diretos sobre as áreas que necessitam de maior atenção pedagógica.
* **Comparação entre Turmas por Descritor:** Ferramentas para comparar o desempenho médio e a distribuição de notas entre diferentes turmas para cada descritor, auxiliando na identificação de melhores práticas.
* **Identificação de Alunos com Desempenho Abaixo do Esperado por Descritor:** Destaque de alunos que não atingiram um determinado limiar de desempenho em descritores específicos, facilitando a implementação de intervenções direcionadas às necessidades individuais.

### Benefícios e Impacto

A utilização deste aplicativo para análise de dados de simulados, **com foco nos descritores**, oferece diversos benefícios:

* **Monitoramento Preciso do Aprendizado:** Permite um acompanhamento detalhado do desenvolvimento das habilidades e competências definidas pelos descritores.
* **Diagnóstico Específico de Dificuldades:** Facilita a identificação precisa das áreas em que os alunos apresentam maiores dificuldades em termos de habilidades específicas.
* **Planejamento Pedagógico Direcionado:** Informa o planejamento de aulas e atividades de reforço focadas no desenvolvimento das habilidades com menor desempenho.
* **Avaliação da Eficácia das Estratégias:** Permite avaliar o impacto das intervenções pedagógicas no desenvolvimento de habilidades específicas ao longo do tempo.
* **Preparação Otimizada para o SAEB 2025:** Ao fornecer uma visão clara do domínio dos alunos em cada descritor avaliado pelo SAEB, o aplicativo contribui para uma preparação mais estratégica e eficiente para a avaliação.

Em suma, este aplicativo desenvolvido em Python com Streamlit, Pandas e NumPy, integrando a análise por descritores, representa uma ferramenta poderosa e acessível para a análise de dados educacionais, oferecendo aos profissionais da educação *insights* valiosos para o monitoramento preciso do aprendizado, a identificação de necessidades específicas e o planejamento de ações pedagógicas mais eficazes, visando a melhoria contínua do processo de ensino-aprendizagem e uma preparação otimizada para avaliações como o SAEB 2025.
