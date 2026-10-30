# Etapa 1 — execução sem histórico

Execução real da versão da etapa 1 em 30/10/2026, com o modelo
`openai/gpt-oss-120b` pela API da Groq. O conteúdo das respostas abaixo foi
gerado pelo modelo. Novas execuções podem produzir textos diferentes.
Essa versão está preservada em `chatbot_mentor_etapa1.py`.

## Pergunta 1

Eu sou geofísico e quero migrar para a área de dados. Qual linguagem de
programação devo aprender primeiro? Responda em até 150 palavras.

## Resposta 1

Para quem vem da geofísica e quer entrar na área de dados, a melhor primeira linguagem é **Python**. Ela combina:

- **Facilidade de aprendizado**: sintaxe clara e extensa documentação.
- **Ecossistema robusto**: bibliotecas como NumPy, pandas e SciPy para manipulação e análise de dados; Matplotlib e Seaborn para visualização; Scikit-learn e TensorFlow para machine learning.
- **Integração com GIS**: pacotes como rasterio, geopandas e pyproj facilitam o trabalho com dados espaciais, algo familiar para geofísicos.
- **Comunidade ativa**: muitos tutoriais, cursos e fóruns voltados a ciência de dados e aplicações geocientíficas.

Comece com cursos introdutórios de Python para ciência de dados (por exemplo, “Python for Data Science” no Coursera ou DataCamp) e pratique usando datasets reais de sismologia ou sensoriamento remoto. Depois, explore R se precisar de análises estatísticas avançadas, mas Python já cobre a maior parte das demandas.

## Pergunta 2

E que tipo de projeto de portfólio eu poderia criar usando essa linguagem?
Responda em até 150 palavras.

## Resposta 2

Um projeto de portfólio interessante para **Python** (ou outra linguagem que você esteja estudando) é **um “Dashboard Interativo de Dados de COVID-19”**:

1. **Coleta de dados** – use APIs públicas (ex.: covid19api.com) ou arquivos CSV do Our World in Data.
2. **Processamento** – pandas para limpeza, agregação por país, região e período.
3. **Visualização** – Plotly/Dash ou Streamlit para criar gráficos interativos (linhas, mapas choropleth, heatmaps).
4. **Backend opcional** – FastAPI para expor endpoints REST que retornem dados filtrados.
5. **Deploy** – Docker + Heroku/Vercel ou GitHub Pages (via Streamlit sharing).

**Destaques no portfólio**: código bem estruturado (padrões de projeto), testes unitários, documentação com Swagger/OpenAPI, CI/CD com GitHub Actions e responsividade da UI. Esse projeto demonstra habilidades em **ETL, visualização, APIs, DevOps e UI/UX**, tornando-o atrativo para recrutadores.

## O que observar

- A primeira resposta usou o contexto de Geofísica presente na primeira pergunta.
- A segunda citou Python, mas sugeriu um projeto genérico, sem relacioná-lo à
  Geofísica. Citar a mesma linguagem não comprova memória: o modelo pode supor
  uma linguagem comum.
- A evidência de que não enviamos histórico está no programa: cada
  `modelo.invoke(pergunta)` recebe somente a pergunta atual.
- Esta execução valida a integração com a API e serve como referência para
  comparar com a etapa de histórico. Não é uma avaliação da qualidade de todas
  as recomendações geradas pelo modelo.
