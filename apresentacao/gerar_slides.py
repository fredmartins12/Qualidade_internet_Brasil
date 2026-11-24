"""Gera o deck da prévia (5 min) em docs/apresentacao_previa.pptx.

Uso:
    python gerar_slides.py
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

DARK = RGBColor(0x0B, 0x3D, 0x5C)
TEAL = RGBColor(0x0B, 0x9B, 0x9B)
BG = RGBColor(0xF4, 0xF8, 0xF9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x55, 0x55, 0x55)
GREEN = RGBColor(0x13, 0x73, 0x33)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

EQUIPE = [
    "Antônio Victor Travassos Brasil",
    "Istênio Gomes",
    "Felipe Emidio de Medeiros Neto",
    "Frederico Botelho Martins",
]


def new_slide(prs, bg_color=WHITE):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    rect.fill.solid()
    rect.fill.fore_color.rgb = bg_color
    rect.line.fill.background()
    rect.shadow.inherit = False
    return slide


def add_text(slide, left, top, width, height, text, size, color, bold=False,
             align=PP_ALIGN.LEFT, italic=False, font="Segoe UI"):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font
    return box


def add_bullets(slide, left, top, width, height, items, size=18, color=DARK, spacing=8):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(spacing)
        run = p.add_run()
        run.text = f"•  {item}"
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.name = "Segoe UI"
    return box


def add_header(slide, kicker, title):
    add_text(slide, Inches(0.6), Inches(0.35), Inches(12), Inches(0.4),
              kicker.upper(), 13, TEAL, bold=True)
    add_text(slide, Inches(0.6), Inches(0.7), Inches(12), Inches(0.8),
              title, 30, DARK, bold=True)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.5),
                                   Inches(2.2), Pt(3))
    line.fill.solid()
    line.fill.fore_color.rgb = TEAL
    line.line.fill.background()


def slide_capa(prs):
    s = new_slide(prs, DARK)
    add_text(s, Inches(0.8), Inches(1.8), Inches(11.7), Inches(0.5),
              "TRABALHO DE REDES DE COMPUTADORES — PRÉVIA", 16, TEAL, bold=True)
    add_text(s, Inches(0.8), Inches(2.3), Inches(11.7), Inches(2.0),
              "Qualidade de Internet no Brasil\ncom Dados Abertos (Anatel)", 40, WHITE, bold=True)
    add_text(s, Inches(0.8), Inches(4.4), Inches(11.7), Inches(0.4),
              "Professor: Iguatemi", 16, RGBColor(0xCC, 0xDD, 0xE5))
    add_bullets(s, Inches(0.8), Inches(4.9), Inches(11.7), Inches(2.0),
                EQUIPE, size=16, color=WHITE, spacing=4)


def slide_motivacao(prs):
    s = new_slide(prs)
    add_header(s, "Motivação", "Internet chegou, mas a qualidade é desigual")
    add_bullets(s, Inches(0.6), Inches(1.9), Inches(7.2), Inches(4.5), [
        "95% dos domicílios brasileiros têm internet em 2025 (IBGE/PNAD Contínua TIC)",
        "Mas a qualidade do acesso ainda é desigual entre classes sociais e regiões (CGI.br/TIC Domicílios 2025)",
        "Ter acesso ≠ ter uma conexão de boa qualidade",
    ], size=18)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.6), Inches(12.1), Inches(1.3))
    box.fill.solid()
    box.fill.fore_color.rgb = BG
    box.line.color.rgb = TEAL
    box.line.width = Pt(1.5)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_right = Inches(0.3)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = ("Pergunta: é possível, com medições próprias e dados públicos, identificar padrões "
                "de qualidade da conexão e prever momentos de degradação?")
    run.font.size = Pt(16)
    run.font.italic = True
    run.font.color.rgb = DARK


def slide_objetivo(prs):
    s = new_slide(prs)
    add_header(s, "Objetivo", "O que o projeto propõe fazer")
    add_text(s, Inches(0.6), Inches(1.9), Inches(12), Inches(0.5), "Objetivo geral", 18, TEAL, bold=True)
    add_text(s, Inches(0.6), Inches(2.3), Inches(12), Inches(1.0),
              "Medir a qualidade da conexão de internet via sondagem ativa, identificar padrões de "
              "degradação e comparar com dados públicos de qualidade (Anatel/SIMET).", 16, DARK)
    add_text(s, Inches(0.6), Inches(3.4), Inches(12), Inches(0.5), "Objetivos específicos", 18, TEAL, bold=True)
    add_bullets(s, Inches(0.6), Inches(3.8), Inches(12), Inches(3.0), [
        "Coletar RTT, jitter, desvio-padrão e perda de pacotes (ICMP/Scapy)",
        "Organizar os dados em janelas horárias",
        "Visualizar a variação da qualidade ao longo do dia/semana",
        "Detectar padrões de degradação da conexão",
        "Comparar com indicadores públicos (Anatel / SIMET)",
    ], size=16)


def slide_arquitetura(prs):
    s = new_slide(prs)
    add_header(s, "Metodologia", "Como o projeto funciona, em 5 etapas")
    etapas = [
        ("1", "Coleta", "ICMP via Scapy"),
        ("2", "Agregação", "janelas por hora"),
        ("3", "Visualização", "padrões no tempo"),
        ("4", "Detecção", "limiar estatístico"),
        ("5", "Comparação", "Anatel / SIMET"),
    ]
    n = len(etapas)
    box_w = Inches(2.2)
    gap = Inches(0.25)
    total_w = box_w * n + gap * (n - 1)
    start_x = Emu(int((SLIDE_W - total_w) / 2))
    y = Inches(3.0)
    for i, (num, titulo, sub) in enumerate(etapas):
        x = Emu(int(start_x + i * (box_w + gap)))
        circle = s.shapes.add_shape(MSO_SHAPE.OVAL, Emu(int(x + box_w / 2 - Inches(0.35))), Inches(2.0), Inches(0.7), Inches(0.7))
        circle.fill.solid()
        circle.fill.fore_color.rgb = TEAL
        circle.line.fill.background()
        tf = circle.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = num
        run.font.size = Pt(22)
        run.font.bold = True
        run.font.color.rgb = WHITE

        card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, box_w, Inches(1.6))
        card.fill.solid()
        card.fill.fore_color.rgb = BG
        card.line.color.rgb = TEAL
        card.line.width = Pt(1)
        tf2 = card.text_frame
        tf2.word_wrap = True
        tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = tf2.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        r1 = p1.add_run()
        r1.text = titulo
        r1.font.bold = True
        r1.font.size = Pt(16)
        r1.font.color.rgb = DARK
        p2 = tf2.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = sub
        r2.font.size = Pt(12)
        r2.font.color.rgb = GRAY

        if i < n - 1:
            arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                        Emu(int(x + box_w + gap / 4)), Inches(2.65),
                                        Emu(int(gap / 2)), Inches(0.3))
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = TEAL
            arrow.line.fill.background()

    add_text(s, Inches(0.6), Inches(5.0), Inches(12.1), Inches(1.5),
              "Base teórica: extensão do ICMP Pinger Lab, trabalho de programação oficial do livro-texto "
              "Kurose & Ross (capítulo de ICMP) — usamos Scapy para escalar a coleta "
              "(múltiplos alvos, agendamento, milhares de amostras).",
              15, GRAY, italic=True)


def slide_status(prs):
    s = new_slide(prs)
    add_header(s, "Onde estamos", "O que já foi implementado")
    feitos = [
        "Script de coleta (RTT, stdev, jitter, perda) rodando via ICMP/Scapy + Npcap",
        "Coleta em loop contínuo (15 em 15 min), sem precisar de admin — já em execução",
        "Script de agregação horária implementado e testado",
        "Repositório no GitHub organizado e documentado",
    ]
    y = Inches(1.9)
    for item in feitos:
        check = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.6), y, Inches(0.35), Inches(0.35))
        check.fill.solid()
        check.fill.fore_color.rgb = GREEN
        check.line.fill.background()
        ctf = check.text_frame
        cp = ctf.paragraphs[0]
        cp.alignment = PP_ALIGN.CENTER
        cr = cp.add_run()
        cr.text = "✓"
        cr.font.size = Pt(16)
        cr.font.bold = True
        cr.font.color.rgb = WHITE
        add_text(s, Inches(1.15), Emu(int(y) - Emu(int(Inches(0.03)))), Inches(11.4), Inches(0.6), item, 17, DARK)
        y = Emu(int(y) + int(Inches(0.85)))

    add_text(s, Inches(0.6), Inches(5.9), Inches(12.1), Inches(1.0),
              "Pendente: visualização dos dados, detector de degradação e comparação com "
              "Anatel/SIMET — previsto até a apresentação final (07/Dez).", 15, GRAY, italic=True)


def slide_demo(prs):
    s = new_slide(prs, DARK)
    add_text(s, Inches(0.6), Inches(0.5), Inches(12), Inches(0.5), "DEMONSTRAÇÃO AO VIVO", 16, TEAL, bold=True)
    add_text(s, Inches(0.6), Inches(1.0), Inches(12), Inches(1.0),
              "Coleta rodando em tempo real", 32, WHITE, bold=True)
    add_bullets(s, Inches(0.6), Inches(2.3), Inches(12), Inches(3.5), [
        "Terminal executando python coleta/probe.py",
        "Métricas de RTT, stdev, jitter e perda impressas em tempo real",
        "dados/probes.csv sendo gerado a cada execução",
    ], size=18, color=WHITE)


def slide_proximos(prs):
    s = new_slide(prs)
    add_header(s, "Próximos passos", "Cronograma até a apresentação final")
    add_bullets(s, Inches(0.6), Inches(1.9), Inches(12), Inches(2.8), [
        "Visualização dos dados coletados (séries temporais por alvo)",
        "Detector simples de degradação (limiar estatístico sobre média móvel)",
        "Comparação com dados abertos da Anatel (plano principal) e SIMET (complementar)",
        "Roteiro e ensaio da apresentação final",
    ], size=18)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.2), Inches(12.1), Inches(1.6))
    box.fill.solid()
    box.fill.fore_color.rgb = DARK
    box.line.fill.background()
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.3)
    tf.margin_right = Inches(0.3)
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Apresentação final: 07/Dezembro/2026 — 12 minutos, com demonstração prática obrigatória"
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = WHITE


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slide_capa(prs)
    slide_motivacao(prs)
    slide_objetivo(prs)
    slide_arquitetura(prs)
    slide_status(prs)
    slide_demo(prs)
    slide_proximos(prs)

    out = "../docs/apresentacao_previa.pptx"
    prs.save(out)
    print(f"Gerado: {out}")


if __name__ == "__main__":
    main()
