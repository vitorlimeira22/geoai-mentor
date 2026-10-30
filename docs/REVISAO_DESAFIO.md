# Conferência do desafio

Revisão baseada nos prints fornecidos: preparação, etapas 1 a 3, pontos de
revisão e encerramento. Não foi feito envio ao fórum ou a redes sociais.

## Implementação

| Requisito | Conferência |
| --- | --- |
| Ambiente e dependências | Ambiente virtual local e versões fixadas em `requirements.txt`. |
| Configuração por ambiente | `load_dotenv` e `GROQ_API_KEY`; adaptação autorizada da OpenAI para Groq. |
| Arquivo principal | `chatbot_mentor.py`, com versões 1 e 2 preservadas. |
| Etapa 1 | Duas perguntas, `temperature=0.7`, `invoke` e exibição de `.content`. |
| Etapa 2: template | Tuplas `system`, placeholder `{historico}` e `human` com `{query}`. |
| Etapa 2: LCEL | Template, modelo e `StrOutputParser`, nessa ordem. |
| Etapa 3: armazenamento | Dicionário `memoria_sessoes` e `InMemoryChatMessageHistory`. |
| Etapa 3: função de histórico | Cria no primeiro acesso e retorna o mesmo objeto por ID. |
| Etapa 3: gerenciador | `RunnableWithMessageHistory` envolve a cadeia. |
| Chaves consistentes | `query` e `historico` coincidem entre template e configuração. |
| Configuração da chamada | Pergunta no primeiro dicionário; `session_id` em `config.configurable`. |
| Continuidade e isolamento | Três testes verificam o histórico e a separação de sessões. |

Os imports foram adaptados para `langchain_core`. As classes de histórico
funcionam nessa versão, mas emitem avisos de descontinuação; a documentação
do projeto registra a evolução recomendada para LangGraph.

## Encerramento e apresentação

| Item do encerramento | Material preparado |
| --- | --- |
| README claro e com execução | README de apresentação, separado do guia didático. |
| Exemplos antes e depois | Registros reais das três etapas e comparação no README. |
| GIF ou prints | PNGs e GIF reproduzindo os registros reais, com origem identificada. |
| Explicação da arquitetura | Fluxo no README e explicação de cada componente no guia. |
| Relato de aprendizado | `RELATO_APRENDIZADO.md`, para revisão do aluno. |
| Repositório GitHub | Publicação pública autorizada pelo aluno; endereço informado no README. |

A postagem no fórum, comunidade ou LinkedIn fica a critério do aluno.
Persistência entre execuções e interface interativa são extensões, não requisitos
das três etapas mostradas.
