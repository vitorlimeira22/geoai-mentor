"""Etapa 2: persona e cadeia LCEL, com o espaço do histórico ainda vazio."""

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import APIConnectionError, APIStatusError
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


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
            # Aqui entrarão as mensagens anteriores na etapa 3.
            ("placeholder", "{historico}"),
            # A variável query será preenchida com a pergunta atual.
            ("human", "{query}"),
        ]
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

    prompt = criar_prompt()
    # A saída de cada componente se torna a entrada do próximo.
    cadeia = prompt | modelo | StrOutputParser()

    perguntas = [
        "Eu sou geofísico e quero migrar para a área de dados. "
        "Qual linguagem de programação devo aprender primeiro? "
        "Responda em até 150 palavras.",
        "E que tipo de projeto de portfólio eu poderia criar usando essa linguagem? "
        "Responda em até 150 palavras.",
    ]

    print("GeoAI Mentor — etapa 2: persona e cadeia, sem histórico", flush=True)

    for numero, pergunta in enumerate(perguntas, start=1):
        print(f"\nPergunta {numero}: {pergunta}", flush=True)

        # O template recebe a pergunta e uma lista de histórico vazia.
        # Nenhuma mensagem anterior é armazenada ou reenviada nesta etapa.
        resposta = cadeia.invoke({"query": pergunta, "historico": []})
        # StrOutputParser já transformou a saída do modelo em uma string.
        print(f"\nResposta {numero}:\n{resposta}", flush=True)


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
