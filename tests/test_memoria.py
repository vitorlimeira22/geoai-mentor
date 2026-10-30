"""Verifica o fluxo de mensagens sem chave de API nem conexão à Groq."""

import unittest

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from chatbot_mentor import (
    criar_cadeia_com_memoria,
    memoria_sessoes,
    obter_historico_por_sessao,
)


class TestMemoriaPorSessao(unittest.TestCase):
    def setUp(self):
        memoria_sessoes.clear()
        self.chamadas = []

        def responder(prompt):
            self.chamadas.append(prompt.to_messages())
            return AIMessage(content=f"Resposta de teste {len(self.chamadas)}.")

        self.cadeia = criar_cadeia_com_memoria(RunnableLambda(responder))

    def tearDown(self):
        memoria_sessoes.clear()

    def test_reutiliza_o_mesmo_objeto_por_sessao(self):
        primeiro_acesso = obter_historico_por_sessao("sessao_a")
        segundo_acesso = obter_historico_por_sessao("sessao_a")

        self.assertIs(primeiro_acesso, segundo_acesso)
        self.assertEqual(primeiro_acesso.messages, [])

    def test_reenvia_o_turno_anterior_sem_duplicar_a_pergunta_atual(self):
        config = {"configurable": {"session_id": "sessao_a"}}
        primeira_resposta = self.cadeia.invoke({"query": "Quero aprender Julia."}, config=config)
        segunda_resposta = self.cadeia.invoke({"query": "Qual projeto posso criar?"}, config=config)

        self.assertEqual([m.type for m in self.chamadas[0]], ["system", "human"])
        self.assertEqual(
            [m.type for m in self.chamadas[1]],
            ["system", "human", "ai", "human"],
        )
        self.assertEqual(
            [m.content for m in self.chamadas[1][1:]],
            ["Quero aprender Julia.", primeira_resposta, "Qual projeto posso criar?"],
        )
        mensagens_salvas = obter_historico_por_sessao("sessao_a").messages
        self.assertEqual([m.type for m in mensagens_salvas], ["human", "ai", "human", "ai"])
        self.assertEqual(mensagens_salvas[-1].content, segunda_resposta)
        self.assertIsInstance(segunda_resposta, str)

    def test_sessoes_diferentes_nao_compartilham_mensagens(self):
        self.cadeia.invoke(
            {"query": "Minha linguagem é Julia."},
            config={"configurable": {"session_id": "sessao_a"}},
        )
        self.cadeia.invoke(
            {"query": "Quero começar outra conversa."},
            config={"configurable": {"session_id": "sessao_b"}},
        )

        self.assertEqual([m.type for m in self.chamadas[1]], ["system", "human"])
        self.assertEqual(self.chamadas[1][-1].content, "Quero começar outra conversa.")
        historico_a = obter_historico_por_sessao("sessao_a")
        historico_b = obter_historico_por_sessao("sessao_b")
        self.assertIsNot(historico_a, historico_b)
        self.assertEqual(len(historico_a.messages), 2)
        self.assertEqual(len(historico_b.messages), 2)


if __name__ == "__main__":
    unittest.main()
