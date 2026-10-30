# GeoAI Mentor — desafio Alura

Projeto de estudo: construir um chatbot que ajuda profissionais de Geociências
a planejar sua transição para Ciência de Dados e Inteligência Artificial.

O desenvolvimento será feito por etapas, com explicação de cada conceito.
A integração com o modelo usará a API da Groq e o modelo
`openai/gpt-oss-120b`, em lugar da API da OpenAI apresentada no desafio.

## Aula 0 — preparar o ambiente

Objetivo: ter um Python isolado para este projeto e instalar as bibliotecas
necessárias antes de escrever a primeira chamada ao modelo.

### Papel de cada componente

| Componente | Função |
| --- | --- |
| Python | Executa nosso programa. |
| `.venv/` | Guarda o ambiente virtual e as bibliotecas deste projeto. |
| `python-dotenv` | Carrega as configurações de um arquivo `.env` para o processo Python. |
| `langchain-core` | Fornece mensagens, templates de prompt, parsers e cadeias. |
| `langchain-groq` | Fornece `ChatGroq`, que conecta o LangChain à API da Groq. |
| `requirements.txt` | Registra as versões das bibliotecas usadas no projeto. |
| `.env.example` | Mostra o nome da configuração necessária, sem incluir uma chave real. |
| `.gitignore` | Define arquivos que o Git deve ignorar, como `.env` e `.venv/`. |

O modelo será executado nos servidores da Groq. Nosso computador executa o
programa que envia as mensagens e recebe as respostas pela API.

### Como reproduzir a preparação no PowerShell

Abra o terminal na pasta do projeto. Se o comando `py` estiver disponível:

```powershell
py -3.13 -m venv .venv
```

Se o Python não estiver no PATH, use o caminho da instalação encontrada neste PC:

```powershell
python -m venv .venv
```

Execute apenas uma das duas alternativas acima. Depois instale as bibliotecas:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Usar o executável dentro de `.venv` garante que a instalação aconteça no ambiente
do projeto. Não é necessário ativar o ambiente para usar esse comando.

Se a chave não estiver configurada como variável de ambiente, crie o arquivo local:

```powershell
Copy-Item .env.example .env
```

Abra `.env` no editor e preencha `GROQ_API_KEY` com sua chave da Groq. Não coloque
a chave em arquivos Python, no README ou no chat. O arquivo `.env` será ignorado
pelo Git.

### Conferência local

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -c "from dotenv import load_dotenv; from langchain_groq import ChatGroq; from langchain_core.prompts import ChatPromptTemplate; print('Importacoes OK')"
```

Esses comandos verificam o ambiente. Eles não enviam mensagens à Groq nem
validam a chave da API.

## Aula 1 — primeira chamada ao modelo, sem histórico

Objetivo: obter respostas para duas perguntas independentes, usando `ChatGroq`
no lugar de `ChatOpenAI`. A versão desta aula está preservada no arquivo
`chatbot_mentor_etapa1.py`; o arquivo principal acompanha a etapa atual.

```powershell
.\.venv\Scripts\python.exe chatbot_mentor_etapa1.py
```

### Entenda o programa

1. `load_dotenv(...)` carrega o arquivo `.env` ao lado do script. Por padrão,
   preserva variáveis que já existam no processo.
2. `os.getenv(...)` lê a chave carregada. O programa para com uma orientação
   caso a chave esteja vazia.
3. `ChatGroq(...)` configura o modelo e a conexão. Criar esse objeto ainda não
   envia uma pergunta à API.
4. `perguntas` é uma lista de strings. O `for` percorre essa lista, e
   `enumerate(..., start=1)` também fornece o número de cada pergunta.
5. `modelo.invoke(pergunta)` faz a chamada à API e aguarda a resposta.
6. `resposta.content` contém o texto da resposta. O objeto também inclui
   metadados, como uso de tokens e motivo de encerramento da geração.
7. `if __name__ == "__main__"` inicia a execução quando rodamos o arquivo
   diretamente. Importar o módulo em outro programa não dispara as perguntas.

### Por que ainda não existe memória?

Cada `invoke` recebe apenas uma string com a pergunta atual. O programa não
envia as perguntas e respostas anteriores junto com ela. Reutilizar o objeto
`modelo` mantém sua configuração, mas não acrescenta um histórico automaticamente.

Na segunda pergunta, a expressão "essa linguagem" depende da primeira resposta.
Observe se o modelo pede esclarecimento, responde de forma genérica ou supõe uma
linguagem. Uma suposição correta, sozinha, não demonstra que ele recebeu o histórico.

O [registro da primeira execução](../exemplos/etapa_1_sem_memoria.md) guarda as duas
respostas reais para compararmos depois com a versão que terá histórico.

As perguntas pedem respostas de até 150 palavras para facilitar a comparação.
Esse pedido é uma instrução ao modelo, sem garantia de contagem exata.

### Parâmetros usados

| Parâmetro | Significado |
| --- | --- |
| `model="openai/gpt-oss-120b"` | Identifica o modelo executado pela Groq. |
| `temperature=0.7` | Ajusta a variação na escolha das próximas palavras; não mede precisão. |
| `max_tokens=2000` | Limita a geração, incluindo tokens de raciocínio do GPT OSS. Tokens são unidades de texto, diferentes de palavras. |
| `reasoning_effort="low"` | Usa o nível baixo de esforço de raciocínio, suficiente para esta demonstração simples. |
| `timeout=30` | Define um tempo de espera de 30 segundos por tentativa de requisição. |
| `max_retries=1` | Permite uma tentativa adicional nos erros que a biblioteca considera recuperáveis. |

Os tratamentos de erro mostram mensagens para falhas de conexão, chave recusada
e limite de uso, sem imprimir a chave ou os detalhes da requisição.

## Aula 2 — personalidade e cadeia LCEL

Objetivo: orientar o chatbot a atuar como GeoAI Mentor e organizar a execução
em três componentes: template de prompt, modelo e parser de saída.
Essa versão está preservada em `chatbot_mentor_etapa2.py`.

```powershell
.\.venv\Scripts\python.exe chatbot_mentor_etapa2.py
```

Não foi necessário instalar novas bibliotecas. Os imports desta etapa são:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
```

O print do curso usa `langchain.prompts`. Na versão instalada neste projeto,
usamos `langchain_core.prompts`.

### 1. Criar o template de conversa

A função `criar_prompt()` usa `ChatPromptTemplate.from_messages(...)` para
construir um molde de mensagens. Ela fica separada para podermos inspecionar
o prompt sem carregar a chave nem chamar a API.

O método recebe uma lista de três tuplas. Cada tupla contém um papel e um
conteúdo:

| Entrada | O que faz | Por que usamos |
| --- | --- | --- |
| `("system", texto)` | Define o papel do GeoAI Mentor, o tom didático e o foco em Geociências. | Envia as mesmas orientações em cada chamada, sem precisar repeti-las em cada pergunta. |
| `("placeholder", "{historico}")` | Reserva uma posição para inserir uma lista de mensagens anteriores. | Prepara o template para o histórico que será gerenciado na etapa 3. |
| `("human", "{query}")` | Representa a pergunta atual do usuário. | Permite reaproveitar o mesmo template com perguntas diferentes. |

`{query}` e `{historico}` são campos do template. Seus nomes correspondem às
chaves do dicionário passado para `invoke`. `query` é um nome escolhido por nós;
poderia ser `pergunta`, desde que o nome fosse alterado nos dois lugares.

O placeholder insere mensagens no lugar reservado. Ele não cria uma mensagem
com o papel "placeholder" na requisição e não salva conversas por conta própria.

A personalidade é uma orientação enviada ao modelo em cada requisição. Seu
texto pede respostas em português, sugestões ligadas a Geociências e perguntas
de esclarecimento quando faltar uma informação necessária.

### 2. Conectar os componentes com LCEL

```python
prompt = criar_prompt()
cadeia = prompt | modelo | StrOutputParser()
```

LCEL significa LangChain Expression Language. Nessa expressão, `|` conecta os
componentes em sequência, passando a saída de um como entrada do próximo.
Escrever essa linha monta a cadeia; a requisição acontece ao chamar `invoke`.

| Componente | Entrada | Saída |
| --- | --- | --- |
| `prompt` | Dicionário com `query` e `historico`. | Mensagens organizadas para o modelo (`ChatPromptValue`). |
| `modelo` | Mensagens já preenchidas. | Objeto de resposta (`AIMessage`), com texto e metadados. |
| `StrOutputParser()` | Resposta do modelo. | Texto da resposta como string (`str`). |

O parser extrai o texto, sem fazer outra chamada ao modelo. Por isso, agora
imprimimos `resposta` diretamente. Na etapa 1, recebíamos o objeto do modelo e
acessávamos `resposta.content`.

A saída final desta cadeia não inclui os metadados. Por isso, o aviso baseado
em `response_metadata` da etapa 1 fica apenas na versão preservada daquela aula.

### 3. Executar com os campos do template

```python
resposta = cadeia.invoke({"query": pergunta, "historico": []})
```

`query` fornece a pergunta atual. `historico: []` fornece uma lista vazia, que
não adiciona nenhuma mensagem na posição do placeholder.

Assim, em cada chamada o modelo recebe a mensagem de sistema e a pergunta
atual. Na segunda pergunta ele continua recebendo o papel de mentor, mas não
recebe a primeira pergunta nem a primeira resposta. Um pedido de esclarecimento
é um resultado coerente quando "essa linguagem" não está identificada nas
mensagens recebidas. Uma suposição também pode ocorrer; o prompt orienta o
comportamento do modelo, sem garantir que ele sempre cumpra as instruções.

### Resultado observado e validação

As duas perguntas foram executadas com sucesso na API da Groq. A
[saída completa](../exemplos/etapa_2_persona_sem_memoria.txt) foi salva para
comparação. Também há um [exemplo do prompt formatado](../exemplos/etapa_2_prompt_formatado.txt)
que mostra as mensagens produzidas pelo template para a segunda pergunta.

| Observação | Etapa 1 | Etapa 2 |
| --- | --- | --- |
| Orientação de sistema | Ausente. | Papel de mentor com foco em Geociências. |
| Histórico enviado | Nenhum. | Lista vazia. |
| Projeto sugerido na segunda resposta desta execução | Dashboard de COVID-19. | Análise de dados sísmicos. |

A segunda resposta da etapa 2 também mencionou Python. A linguagem não estava
na segunda pergunta nem no texto de sistema: ela foi uma suposição do modelo.
O foco em Geociências, por sua vez, estava nas instruções de sistema enviadas
em cada chamada. Assim, esse resultado não demonstra memória da conversa.

A conferência local, sem API, validou o preenchimento de `query`, a presença
de apenas `system` e `human` com histórico vazio, a inserção de mensagens quando
fornecidas ao placeholder e o retorno final como `str`. Esses exemplos
de histórico foram usados apenas na conferência local; a execução real desta
aula continuou passando `historico: []`.

## Aula 3 — histórico por sessão

Objetivo: incluir os turnos anteriores na próxima chamada da mesma conversa,
mantendo históricos separados quando o `session_id` for diferente.

```powershell
.\.venv\Scripts\python.exe chatbot_mentor.py
```

### 1. Importar as peças do histórico

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
```

O primeiro import usa o caminho disponível na versão instalada, em lugar de
`langchain.memory`, mostrado no curso. Não foi necessário instalar bibliotecas.

### 2. Guardar um histórico para cada conversa

```python
memoria_sessoes = {}

def obter_historico_por_sessao(session_id: str):
    if session_id not in memoria_sessoes:
        memoria_sessoes[session_id] = InMemoryChatMessageHistory()
    return memoria_sessoes[session_id]
```

| Peça | Função | Por que usamos |
| --- | --- | --- |
| `memoria_sessoes` | Associa IDs de conversa a objetos de histórico. | Permite localizar o histórico de cada sessão. |
| `session_id` | Identifica uma conversa. | O mesmo ID recupera as mensagens anteriores; um ID novo começa uma conversa vazia. |
| `InMemoryChatMessageHistory()` | Armazena uma lista de mensagens na memória do programa. | Guarda mensagens do usuário e do assistente, preservando seus papéis. |
| `if session_id not in memoria_sessoes` | Cria o objeto somente quando ainda não existe. | Evita apagar o histórico a cada pergunta. |
| `return memoria_sessoes[session_id]` | Devolve o objeto correspondente ao ID. | Permite que o gerenciador leia e atualize o mesmo histórico. |

A variável fica fora das funções para que o dicionário continue existindo
entre as chamadas feitas no mesmo processo. A expressão `session_id: str`
é uma anotação de tipo que indica a expectativa de receber uma string.

O enunciado chama essa lógica de singleton. Mais precisamente, aqui reutilizamos
uma instância por ID de sessão, com instâncias distintas para IDs diferentes.

### 3. Envolver a cadeia da etapa 2

Na função `criar_cadeia_com_memoria(modelo)`, mantemos a cadeia que já conhecemos:

```python
cadeia = prompt | modelo | StrOutputParser()
```

Depois criamos o gerenciador que a envolve:

```python
RunnableWithMessageHistory(
    runnable=cadeia,
    get_session_history=obter_historico_por_sessao,
    input_messages_key="query",
    history_messages_key="historico",
)
```

| Parâmetro | O que informa ao gerenciador |
| --- | --- |
| `runnable` | Qual cadeia será executada. |
| `get_session_history` | Qual função busca ou cria o histórico da sessão. Passamos a função, sem chamá-la com parênteses. |
| `input_messages_key="query"` | Em qual campo está a pergunta atual, que será registrada como mensagem humana. |
| `history_messages_key="historico"` | Em qual campo do template devem ser inseridas as mensagens anteriores. |

Os nomes `query` e `historico` correspondem aos campos `{query}` e `{historico}`
do template. O gerenciador lê o histórico antes de executar a cadeia e registra
a pergunta e a resposta quando o turno termina com sucesso. Como nossa cadeia
retorna uma string, essa saída é guardada como uma mensagem do assistente.

### 4. Informar o ID na execução

```python
session_id = "sessao_geofisico_01"
config = {"configurable": {"session_id": session_id}}

resposta = cadeia_com_memoria.invoke({"query": pergunta}, config=config)
```

O primeiro dicionário fornece o conteúdo da conversa. `config` configura a
execução; seu `session_id` é passado à função que localiza o histórico. Esse
ID não é acrescentado como uma mensagem do prompt.

Agora não passamos `historico: []` manualmente: o gerenciador preenche o campo
com as mensagens da sessão identificada em `config`.

### 5. Acompanhar o fluxo

```text
Primeira chamada recebe:
  system + pergunta 1

Após a primeira resposta, o histórico guarda:
  pergunta 1 + resposta 1

Segunda chamada recebe:
  system + pergunta 1 + resposta 1 + pergunta 2

Após a segunda resposta, o histórico guarda:
  pergunta 1 + resposta 1 + pergunta 2 + resposta 2
```

A mensagem de sistema vem do template a cada chamada. Ela não faz parte das
quatro mensagens guardadas no histórico. O modelo recebe o contexto reenviado
pelo nosso programa; seus pesos não são alterados por essa conversa.

### Resultado observado e validação

A [execução real](../exemplos/etapa_3_com_memoria.txt) completou as duas chamadas à
Groq. A primeira resposta recomendou Python, e a segunda sugeriu um projeto de
detecção de eventos sísmicos em Python. O terminal mostrou 0 mensagens anteriores
na primeira chamada, 2 na segunda e 4 mensagens guardadas ao final.

Os [testes de histórico](../tests/test_memoria.py) usam respostas simuladas para
verificar as mensagens efetivamente entregues ao componente que representa o
modelo. Eles confirmam a reutilização do histórico, a inclusão do turno anterior
sem duplicar a pergunta atual e a separação entre sessões diferentes.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Duração e evolução dessa memória

O histórico existe somente enquanto este processo Python estiver rodando.
Executar o script novamente começa com um dicionário vazio, mesmo usando o
mesmo ID. Para manter conversas entre execuções, precisamos de armazenamento
persistente. Conforme a conversa cresce, mais mensagens são reenviadas ao
modelo, aumentando a quantidade de tokens de entrada.

Na versão instalada (`langchain-core==1.7.3`), as duas classes usadas nesta aula
emitem avisos de descontinuação. Continuam funcionando e foram mantidas para
acompanhar os requisitos do desafio. A documentação atual recomenda a abordagem
de persistência com LangGraph para novos desenvolvimentos. Não ocultamos esses
avisos durante a execução.

## Possíveis próximos exercícios

As três etapas do chatbot proposto no desafio estão implementadas. Podemos
praticar com uma conversa interativa no terminal, testar mais sessões e explorar
persistência com LangGraph.

A implementação atual usa uma cadeia LangChain com histórico; não cria um grafo.

## Referências

- [Integração ChatGroq no LangChain](https://docs.langchain.com/oss/python/integrations/chat/groq)
- [Modelo GPT OSS 120B na Groq](https://console.groq.com/docs/model/openai/gpt-oss-120b)
- [Parâmetros de raciocínio na Groq](https://console.groq.com/docs/reasoning)
- [ChatPromptTemplate](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate)
- [StrOutputParser](https://reference.langchain.com/python/langchain-core/output_parsers/string/StrOutputParser)
- [RunnableWithMessageHistory](https://reference.langchain.com/python/langchain-core/runnables/history/RunnableWithMessageHistory)
- [Memória de curto prazo e persistência recomendadas atualmente](https://docs.langchain.com/oss/python/langchain/short-term-memory)
