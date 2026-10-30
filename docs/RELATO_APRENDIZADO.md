# Relato de aprendizado — GeoAI Mentor

Texto sugerido para revisar e adaptar antes de compartilhar no fórum ou nas redes.

Neste desafio da Alura, construí o GeoAI Mentor, um chatbot que orienta
profissionais de Geociências na transição para Ciência de Dados e IA.

Comecei com perguntas independentes ao modelo. Depois usei `ChatPromptTemplate`
para definir o papel de mentor e organizei o processamento com LCEL:
`prompt | modelo | StrOutputParser()`.

O principal aprendizado foi distinguir encadeamento de memória. Conectar as
peças da cadeia não faz o modelo receber mensagens de chamadas anteriores.
Para isso, acrescentei `RunnableWithMessageHistory`, um histórico em memória
para cada `session_id` e uma função que recupera o histórico correto.

Assim, a segunda pergunta passou a ser enviada junto com a primeira pergunta
e sua resposta. Testes locais confirmam esse fluxo e a separação entre sessões.
Também aprendi que repetir uma linguagem comum, como Python, não comprova
memória: é preciso observar as mensagens efetivamente enviadas ao modelo.

Adaptei o desafio para usar a API da Groq com `openai/gpt-oss-120b`, mantendo
a chave fora do código. Um próximo exercício é explorar persistência com
LangGraph para conservar conversas entre execuções.

Repositório: https://github.com/vitorlimeira22/geoai-mentor

O README inclui uma animação baseada na execução real e exemplos antes e depois.
