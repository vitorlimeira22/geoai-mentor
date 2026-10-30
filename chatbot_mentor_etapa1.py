"""Etapa 1: duas perguntas à Groq, sem prompt de persona nem histórico."""

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import APIConnectionError, APIStatusError
from langchain_groq import ChatGroq


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

    perguntas = [
        "Eu sou geofísico e quero migrar para a área de dados. "
        "Qual linguagem de programação devo aprender primeiro? "
        "Responda em até 150 palavras.",
        "E que tipo de projeto de portfólio eu poderia criar usando essa linguagem? "
        "Responda em até 150 palavras.",
    ]

    print("GeoAI Mentor — etapa 1: perguntas sem histórico", flush=True)

    for numero, pergunta in enumerate(perguntas, start=1):
        print(f"\nPergunta {numero}: {pergunta}", flush=True)

        # Enviamos só a pergunta atual. A resposta anterior não é reenviada.
        resposta = modelo.invoke(pergunta)
        print(f"\nResposta {numero}:\n{resposta.content}", flush=True)

        if resposta.response_metadata.get("finish_reason") == "length":
            print("\nAviso: a geração atingiu o limite de tokens.", flush=True)


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
