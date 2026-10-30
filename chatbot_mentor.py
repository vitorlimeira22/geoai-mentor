"""Etapa 3: GeoAI Mentor com histórico de conversa separado por sessão."""

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import APIConnectionError, APIStatusError
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq


# Cada chave identifica uma conversa; cada valor guarda suas mensagens.
memoria_sessoes = {}


def obter_historico_por_sessao(session_id: str):
    # Cria o histórico apenas no primeiro acesso a essa sessão.
    if session_id not in memoria_sessoes:
        memoria_sessoes[session_id] = InMemoryChatMessageHistory()

    # Chamadas com o mesmo ID recebem o mesmo objeto, já com as mensagens salvas.
    return memoria_sessoes[session_id]


def criar_prompt():
    # As tuplas informam o papel de cada mensagem e seu conteúdo.
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Você é o GeoAI Mentor, um mentor de carreira especializado em "
                "ajudar profissionais de Geociências, como Geofísica e Geologia, "
                "a migrar para Ciência de Dados e Inteligência Artificial. "
                "Seja amigável, didático e prático. Relacione suas orientações "
                "às habilidades de matemática, física e análise de dados desses "
                "profissionais. Ao sugerir projetos de portfólio, priorize "
                "aplicações em Geociências. Quando faltar uma informação "
                "necessária, faça uma pergunta curta de esclarecimento antes "
                "de recomendar uma solução. Responda em português.",
            ),
            # O gerenciador de histórico preenche esta posição com as mensagens.
            ("placeholder", "{historico}"),
            # A variável query será preenchida com a pergunta atual.
            ("human", "{query}"),
        ]
    )


def criar_cadeia_com_memoria(modelo):
    prompt = criar_prompt()
    # A cadeia da etapa 2 continua sendo o processamento de cada chamada.
    cadeia = prompt | modelo | StrOutputParser()

    # Envolvemos essa cadeia com leitura e atualização do histórico da sessão.
    return RunnableWithMessageHistory(
        runnable=cadeia,
        get_session_history=obter_historico_por_sessao,
        input_messages_key="query",
        history_messages_key="historico",
    )


def main():
    # O caminho parte deste arquivo, mesmo se o terminal estiver em outra pasta.
    load_dotenv(Path(__file__).with_name(".env"))
    chave_api = os.getenv("GROQ_API_KEY", "").strip()

    if not chave_api:
        raise SystemExit("Preencha GROQ_API_KEY no arquivo .env antes de executar.")

    # Criar o objeto configura a conexão; a chamada à API acontece no invoke().
    modelo = ChatGroq(
        api_key=chave_api,
        model="openai/gpt-oss-120b",
        temperature=0.7,
        max_tokens=2000,
        reasoning_effort="low",
        timeout=30,
        max_retries=1,
    )

    cadeia_com_memoria = criar_cadeia_com_memoria(modelo)
    session_id = "sessao_geofisico_01"
    config = {"configurable": {"session_id": session_id}}

    perguntas = [
        "Eu sou geofísico e quero migrar para a área de dados. "
        "Qual linguagem de programação devo aprender primeiro? "
        "Responda em até 150 palavras.",
        "E que tipo de projeto de portfólio eu poderia criar usando essa linguagem? "
        "Responda em até 150 palavras.",
    ]

    print("GeoAI Mentor — etapa 3: conversa com histórico por sessão", flush=True)
    print(f"Sessão: {session_id}", flush=True)

    for numero, pergunta in enumerate(perguntas, start=1):
        print(f"\nPergunta {numero}: {pergunta}", flush=True)

        historico = obter_historico_por_sessao(session_id)
        print(f"Mensagens anteriores nesta sessão: {len(historico.messages)}", flush=True)

        # O histórico é injetado automaticamente a partir do session_id.
        resposta = cadeia_com_memoria.invoke({"query": pergunta}, config=config)
        # StrOutputParser já transformou a saída do modelo em uma string.
        print(f"\nResposta {numero}:\n{resposta}", flush=True)

    historico = obter_historico_por_sessao(session_id)
    print(f"\nHistórico ao final: {len(historico.messages)} mensagens.", flush=True)


if __name__ == "__main__":
    try:
        main()
    except APIConnectionError:
        raise SystemExit("Não foi possível conectar à Groq. Confira sua conexão.") from None
    except APIStatusError as erro:
        # Não exibimos a requisição nem os detalhes que possam conter credenciais.
        if erro.status_code == 401:
            mensagem = "A Groq recusou a chave. Confira GROQ_API_KEY no arquivo .env."
        elif erro.status_code == 429:
            mensagem = "A Groq informou um limite de uso. Aguarde e tente novamente."
        else:
            mensagem = f"A Groq retornou um erro HTTP {erro.status_code}."
        raise SystemExit(mensagem) from None
