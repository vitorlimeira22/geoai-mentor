"""Renderiza registros reais como PNGs e um replay de terminal em GIF; sem API."""

from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont


RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "docs" / "images"
LARGURA = 1280
FUNDO = "#0d1520"
TEXTO = "#dce6f2"


def carregar_fonte():
    for caminho in (
        "C:/Windows/Fonts/consola.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ):
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, 21)
    return ImageFont.load_default(size=21)


def linhas_do_terminal(texto):
    # Normaliza variantes de espaço e hífen não cobertas por algumas fontes.
    texto = texto.replace("\u2011", "-").replace("\u202f", " ").replace("\u2009", " ")
    linhas = []
    for linha in texto.splitlines():
        linhas.extend(textwrap.wrap(linha, width=94, replace_whitespace=False) or [""])
    return linhas


def desenhar(linhas, titulo, fonte, altura=None):
    altura = altura or max(320, 140 + 29 * len(linhas))
    imagem = Image.new("RGB", (LARGURA, altura), FUNDO)
    desenho = ImageDraw.Draw(imagem)
    desenho.rectangle((0, 0, LARGURA, 52), fill="#1c2939")
    for x, cor in ((26, "#ff6b6b"), (49, "#ffd166"), (72, "#62d6a7")):
        desenho.ellipse((x, 20, x + 11, 31), fill=cor)
    desenho.text((108, 14), titulo, font=fonte, fill=TEXTO)
    desenho.text((28, 68), "Reprodução de saída real | Python + LangChain + Groq", font=fonte, fill="#93a9c3")
    for indice, linha in enumerate(linhas):
        cor = TEXTO
        if linha.startswith(("Pergunta", "## Pergunta")):
            cor = "#76c8ff"
        elif linha.startswith(("Mensagens anteriores", "Histórico ao final", "Sessão:")):
            cor = "#62d6a7"
        desenho.text((28, 110 + indice * 29), linha, font=fonte, fill=cor)
    return imagem


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    fonte = carregar_fonte()
    etapa1 = (RAIZ / "exemplos" / "etapa_1_sem_memoria.md").read_text(encoding="utf-8")
    etapa1 = "## Pergunta 1" + etapa1.split("## Pergunta 1", 1)[1].split("## O que observar", 1)[0]
    etapa3 = (RAIZ / "exemplos" / "etapa_3_com_memoria.txt").read_text(encoding="utf-8-sig")
    linhas1 = linhas_do_terminal(etapa1)
    linhas3 = linhas_do_terminal(etapa3)
    desenhar(linhas1, "GeoAI Mentor | etapa 1: sem histórico", fonte).save(SAIDA / "etapa_1_sem_memoria.png")
    desenhar(linhas3, "GeoAI Mentor | etapa 3: com histórico", fonte).save(SAIDA / "etapa_3_com_memoria.png")
    frames = []
    duracoes = []
    for fim in range(4, len(linhas3) + 4, 4):
        fim = min(fim, len(linhas3))
        imagem = desenhar(linhas3[max(0, fim - 21):fim], "GeoAI Mentor | replay da etapa 3", fonte, altura=780)
        frames.append(imagem.quantize(colors=96))
        duracoes.append(1100)
    duracoes[0] = 2200
    duracoes[-1] = 4500
    frames[0].save(
        SAIDA / "conversa_com_memoria.gif",
        save_all=True,
        append_images=frames[1:],
        duration=duracoes,
        loop=0,
        disposal=2,
    )
    print("Demonstração gerada em docs/images, a partir dos registros existentes.")


if __name__ == "__main__":
    main()
