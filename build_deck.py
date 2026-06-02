#!/usr/bin/env python3
"""
Build: "AI's Impact on Mercer's Career Business in Europe"
Internal leadership deck — Mercer-branded (16:9).

Generates: decks/Mercer_AI_Career_Europe.pptx
Run: python3 build_deck.py
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import os

# ---------------------------------------------------------------- brand palette
# Mercer-inspired corporate palette (approximate brand colors).
NAVY      = RGBColor(0x0A, 0x1A, 0x40)   # deep Mercer navy — titles / bars
BLUE      = RGBColor(0x00, 0x73, 0xCF)   # Mercer blue — primary accent
TEAL      = RGBColor(0x00, 0xA1, 0x9A)   # secondary accent
CORAL     = RGBColor(0xFF, 0x6A, 0x39)   # "spark" highlight for key stats
GRAY      = RGBColor(0x53, 0x56, 0x5A)   # body text
LIGHT     = RGBColor(0xF2, 0xF4, 0xF7)   # panel background
MIDGRAY   = RGBColor(0x8A, 0x8E, 0x96)   # captions / footer
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
INK       = RGBColor(0x1A, 0x1D, 0x29)   # near-black headings

FONT = "Calibri"
FONT_H = "Calibri"

EMU_W = Inches(13.333)
EMU_H = Inches(7.5)

prs = Presentation()
prs.slide_width = EMU_W
prs.slide_height = EMU_H
BLANK = prs.slide_layouts[6]


# ----------------------------------------------------------------- helpers
def _set_fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def rect(slide, x, y, w, h, color, line=None, shape=MSO_SHAPE.RECTANGLE):
    sp = slide.shapes.add_shape(shape, x, y, w, h)
    sp.fill.solid()
    sp.fill.fore_color.rgb = color
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(1)
    sp.shadow.inherit = False
    return sp


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    return tb, tf


def para(tf, text, size, color, bold=False, font=FONT, align=PP_ALIGN.LEFT,
         space_after=6, space_before=0, line=1.0, first=False, level=0):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    p.level = level
    try:
        p.line_spacing = line
    except Exception:
        pass
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = font
    r.font.color.rgb = color
    return p


def footer(slide, idx, total=None):
    bar = rect(slide, 0, Inches(7.18), EMU_W, Inches(0.32), NAVY)
    tb, tf = textbox(slide, Inches(0.5), Inches(7.2), Inches(8), Inches(0.28),
                     anchor=MSO_ANCHOR.MIDDLE)
    para(tf, "Mercer  |  Internal — AI & the Future of Careers in Europe",
         9, WHITE, bold=False, first=True)
    tb2, tf2 = textbox(slide, Inches(11.8), Inches(7.2), Inches(1.0), Inches(0.28),
                       anchor=MSO_ANCHOR.MIDDLE)
    para(tf2, str(idx), 9, WHITE, align=PP_ALIGN.RIGHT, first=True)


def content_header(slide, kicker, title):
    """Standard content-slide header with accent bar."""
    rect(slide, 0, 0, EMU_W, Inches(1.32), WHITE)
    rect(slide, Inches(0.5), Inches(0.42), Inches(0.09), Inches(0.62), CORAL)
    tb, tf = textbox(slide, Inches(0.75), Inches(0.32), Inches(11.8), Inches(0.95))
    para(tf, kicker.upper(), 11, BLUE, bold=True, first=True, space_after=2)
    para(tf, title, 25, NAVY, bold=True, space_after=0, line=1.0)
    rect(slide, Inches(0.5), Inches(1.28), Inches(12.33), Pt(1.4), LIGHT)


def stat_card(slide, x, y, w, h, number, label, accent=BLUE):
    card = rect(slide, x, y, w, h, LIGHT)
    rect(slide, x, y, Inches(0.08), h, accent)
    tb, tf = textbox(slide, x + Inches(0.22), y + Inches(0.14),
                     w - Inches(0.34), h - Inches(0.24), anchor=MSO_ANCHOR.MIDDLE)
    para(tf, number, 30, accent, bold=True, first=True, space_after=2, line=0.95)
    para(tf, label, 11, GRAY, space_after=0, line=1.02)


def bullet(tf, text, size=14, color=GRAY, bold_lead=None, first=False,
           space_after=10, marker="—", marker_color=None):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.space_after = Pt(space_after)
    p.line_spacing = 1.05
    rm = p.add_run()
    rm.text = marker + "  "
    rm.font.size = Pt(size)
    rm.font.bold = True
    rm.font.name = FONT
    rm.font.color.rgb = marker_color or CORAL
    if bold_lead:
        rb = p.add_run()
        rb.text = bold_lead
        rb.font.size = Pt(size)
        rb.font.bold = True
        rb.font.name = FONT
        rb.font.color.rgb = INK
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.name = FONT
    r.font.color.rgb = color
    return p


# ================================================================ 1. TITLE
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, EMU_W, EMU_H, NAVY)
# diagonal accent block
band = rect(s, 0, Inches(5.55), EMU_W, Inches(0.16), CORAL)
rect(s, 0, Inches(5.71), EMU_W, Inches(0.06), TEAL)
# Mercer wordmark
tb, tf = textbox(s, Inches(0.7), Inches(0.6), Inches(6), Inches(0.7))
para(tf, "MERCER", 26, WHITE, bold=True, first=True, space_after=0)
tb, tf = textbox(s, Inches(0.7), Inches(2.05), Inches(11.9), Inches(3.2))
para(tf, "AI's Impact on the Future of Careers in Europe", 40, WHITE,
     bold=True, first=True, space_after=10, line=1.02)
para(tf, "Market outlook and strategic implications for Mercer's Career business",
     19, RGBColor(0xC7, 0xD4, 0xEA), space_after=0, line=1.1)
tb, tf = textbox(s, Inches(0.7), Inches(6.0), Inches(11.9), Inches(0.9))
para(tf, "Internal leadership briefing", 13, TEAL, bold=True, first=True, space_after=2)
para(tf, "June 2026  ·  Prepared for Mercer Career — Europe leadership",
     12, RGBColor(0x9F, 0xB0, 0xCC))

# ================================================================ 2. AGENDA
s = prs.slides.add_slide(BLANK)
content_header(s, "Briefing overview", "What this deck covers")
items = [
    ("01", "The AI inflection point", "Why AI is a structural shift for European labour markets"),
    ("02", "The talent paradox", "Mercer Global Talent Trends 2026 — the leadership signal"),
    ("03", "Automation vs. augmentation", "What AI actually does to European work today"),
    ("04", "The widening skills gap", "Where demand is shifting fastest across Europe"),
    ("05", "Workforce sentiment & trust", "Wellbeing, fear and the readiness gap"),
    ("06", "Implications for Mercer Career", "Threats, and where Mercer wins"),
    ("07", "Strategic recommendations", "A horizon-based action agenda"),
]
y = Inches(1.65)
for num, t, d in items:
    rect(s, Inches(0.75), y, Inches(0.62), Inches(0.62), NAVY)
    tb, tf = textbox(s, Inches(0.75), y, Inches(0.62), Inches(0.62), anchor=MSO_ANCHOR.MIDDLE)
    para(tf, num, 16, WHITE, bold=True, first=True, align=PP_ALIGN.CENTER)
    tb, tf = textbox(s, Inches(1.6), y - Inches(0.02), Inches(11), Inches(0.66),
                     anchor=MSO_ANCHOR.MIDDLE)
    p = tf.paragraphs[0]
    p.line_spacing = 1.0
    r = p.add_run(); r.text = t + "   "
    r.font.size = Pt(15); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = NAVY
    r2 = p.add_run(); r2.text = d
    r2.font.size = Pt(12); r2.font.name = FONT; r2.font.color.rgb = GRAY
    y += Inches(0.74)
footer(s, 2)

# ================================================================ 3. EXEC SUMMARY
s = prs.slides.add_slide(BLANK)
content_header(s, "Executive summary", "The bottom line for Mercer Career leadership")
tb, tf = textbox(s, Inches(0.75), Inches(1.55), Inches(7.1), Inches(5.3))
bullet(tf, "AI is reshaping European work faster than organisations can adapt — "
           "the gap between skills held and skills needed is widening, not closing.",
       bold_lead="A structural shift, not a cycle. ", first=True, space_after=13, size=14)
bullet(tf, "The dominant pattern in Europe today is augmentation, but leaders are "
           "already redesigning org structures and roles for an AI operating model.",
       bold_lead="Augmentation now, redesign next. ", space_after=13, size=14)
bullet(tf, "Demand for skills-based organisation design, reskilling, AI-ready career "
           "frameworks, work redesign and reward recalibration is accelerating.",
       bold_lead="Demand pull for Mercer is real. ", space_after=13, size=14)
bullet(tf, "Employee trust and wellbeing are falling while AI-related fear rises — "
           "the human side of transformation is Mercer's natural right to win.",
       bold_lead="The human edge matters. ", space_after=13, size=14)
bullet(tf, "Mercer must also apply AI inside its own Career delivery to protect "
           "margin and stay credible as an adviser on AI-enabled work.",
       bold_lead="Practise what we advise. ", space_after=0, size=14)
# right rail headline stat
rect(s, Inches(8.25), Inches(1.55), Inches(4.55), Inches(5.25), NAVY)
tb, tf = textbox(s, Inches(8.6), Inches(1.85), Inches(3.9), Inches(4.7))
para(tf, "THE SIGNAL", 11, TEAL, bold=True, first=True, space_after=10)
para(tf, "98%", 46, CORAL, bold=True, space_after=0, line=0.9)
para(tf, "of executives plan organisational design changes within two years",
     13, WHITE, space_after=16, line=1.05)
para(tf, "65%", 46, CORAL, bold=True, space_after=0, line=0.9)
para(tf, "expect 11–30% of their workforce to be reskilled or redeployed due to AI",
     13, WHITE, space_after=14, line=1.05)
para(tf, "Source: Mercer Global Talent Trends 2026", 9, MIDGRAY, space_after=0)
footer(s, 3)

# ================================================================ 4. AI INFLECTION
s = prs.slides.add_slide(BLANK)
content_header(s, "01  ·  The AI inflection point", "AI is a structural shift for European labour markets")
cards = [
    ("~1 in 3", "EU adults already use generative AI tools in 2025", BLUE),
    ("58%", "of current work hours across 10 European countries are technically automatable", TEAL),
    ("+4%", "average lift in EU labour productivity from AI adoption — with no short-run job loss", CORAL),
    ("$1.9T", "potential economic value in Europe by 2030, gated by pace of adoption", NAVY),
]
x = Inches(0.75)
for n, l, c in cards:
    stat_card(s, x, Inches(1.6), Inches(2.92), Inches(2.0), n, l, c)
    x += Inches(3.04)
tb, tf = textbox(s, Inches(0.75), Inches(3.95), Inches(12.05), Inches(2.9))
para(tf, "Why this is different from past automation waves", 15, NAVY, bold=True,
     first=True, space_after=8)
bullet(tf, "Generative AI reaches cognitive, non-routine tasks — knowledge and "
           "professional roles, not just routine manual work.", size=13.5, space_after=8)
bullet(tf, "Adoption is bottom-up and fast: employees bring AI to work before "
           "organisations have redesigned the work around it.", size=13.5, space_after=8)
bullet(tf, "The constraint is no longer technology — it is organisation design, "
           "skills, governance and trust. That is HR and Career terrain.", size=13.5,
       space_after=0, marker_color=CORAL)
tb, tf = textbox(s, Inches(0.75), Inches(6.78), Inches(12), Inches(0.3))
para(tf, "Sources: ILO / EPC (2025); McKinsey Global Institute, ‘Agents, robots and us — Europe’ (2026); CEPR (2025).",
     9, MIDGRAY, first=True)
footer(s, 4)

# ================================================================ 5. TALENT PARADOX
s = prs.slides.add_slide(BLANK)
content_header(s, "02  ·  The talent paradox", "Mercer Global Talent Trends 2026 — the leadership signal")
tb, tf = textbox(s, Inches(0.75), Inches(1.5), Inches(5.7), Inches(1.4))
para(tf, "The C-suite is caught between two truths: AI means fewer people may be "
         "needed for today's work — yet there is not enough talent with the skills "
         "tomorrow's AI-enabled work demands.", 15, GRAY, first=True, line=1.12)
para(tf, "Resolving this paradox is the core people-strategy challenge of 2026 — "
         "and Mercer's central advisory opportunity.", 13, NAVY, bold=True, space_before=8, line=1.12)
# stat grid 2x3 on the right
data = [
    ("98%", "execs planning org-design change in 2 yrs", BLUE),
    ("63%", "say redesigning work for AI drives the greatest ROI", TEAL),
    ("65%", "expect 11–30% of staff reskilled / redeployed", CORAL),
    ("59%", "of HR leaders: attracting digital talent is the #1 challenge", NAVY),
    ("51%", "of C-suite feel ready for the human-machine era (was 65% in 2024)", BLUE),
    ("40%", "of employees fear AI job loss (was 28% in 2024)", CORAL),
]
gx, gy = Inches(6.7), Inches(1.5)
cw, ch = Inches(2.92), Inches(1.62)
for i, (n, l, c) in enumerate(data):
    col = i % 2
    row = i // 2
    stat_card(s, gx + col * Inches(3.05), gy + row * Inches(1.74), cw, ch, n, l, c)
tb, tf = textbox(s, Inches(0.75), Inches(6.78), Inches(12), Inches(0.3))
para(tf, "Source: Mercer Global Talent Trends 2026 (≈12,000 executives, HR leaders, employees & investors; 16 geographies; Sep–Oct 2025).",
     9, MIDGRAY, first=True)
footer(s, 5)

# ================================================================ 6. AUTOMATION VS AUGMENTATION
s = prs.slides.add_slide(BLANK)
content_header(s, "03  ·  Automation vs. augmentation", "What AI actually does to European work today")
# left panel augmentation, right automation
rect(s, Inches(0.75), Inches(1.6), Inches(5.9), Inches(4.0), LIGHT)
rect(s, Inches(0.75), Inches(1.6), Inches(5.9), Inches(0.55), TEAL)
tb, tf = textbox(s, Inches(1.0), Inches(1.66), Inches(5.4), Inches(0.45), anchor=MSO_ANCHOR.MIDDLE)
para(tf, "TODAY: AUGMENTATION DOMINATES", 13, WHITE, bold=True, first=True)
tb, tf = textbox(s, Inches(1.0), Inches(2.35), Inches(5.4), Inches(3.1))
bullet(tf, "AI helps people work faster and decide better — without displacing labour.", first=True, size=13, space_after=9)
bullet(tf, "Three-quarters of skills European employers seek are used in BOTH automatable and non-automatable work.", size=13, space_after=9)
bullet(tf, "Demand for AI-skilled roles grew +7.5% even as total job postings fell 11.3%.", size=13, space_after=9)
bullet(tf, "AI-skilled roles command a 56% wage premium.", size=13, space_after=0)

rect(s, Inches(6.95), Inches(1.6), Inches(5.9), Inches(4.0), LIGHT)
rect(s, Inches(6.95), Inches(1.6), Inches(5.9), Inches(0.55), NAVY)
tb, tf = textbox(s, Inches(7.2), Inches(1.66), Inches(5.4), Inches(0.45), anchor=MSO_ANCHOR.MIDDLE)
para(tf, "NEXT: SELECTIVE AUTOMATION", 13, WHITE, bold=True, first=True)
tb, tf = textbox(s, Inches(7.2), Inches(2.35), Inches(5.4), Inches(3.1))
bullet(tf, "15–25% of work hours expected to be automated by 2030 (midpoint scenarios).", first=True, size=13, space_after=9, marker_color=NAVY)
bullet(tf, "Sector range: ~18% in healthcare to ~30% in manufacturing.", size=13, space_after=9, marker_color=NAVY)
bullet(tf, "Work shifts to collaboration among people, AI agents and robots.", size=13, space_after=9, marker_color=NAVY)
bullet(tf, "Outcome is transformation of jobs — not a ‘job apocalypse’.", size=13, space_after=0, marker_color=NAVY)
tb, tf = textbox(s, Inches(0.75), Inches(5.85), Inches(12), Inches(0.85))
para(tf, "Implication for Mercer:  the value is in redesigning roles and tasks — "
         "deciding what humans keep, what AI takes, and how the two combine. "
         "That is job architecture and work-redesign advisory.",
     13.5, NAVY, bold=True, first=True, line=1.1)
tb, tf = textbox(s, Inches(0.75), Inches(6.82), Inches(12), Inches(0.3))
para(tf, "Sources: McKinsey Global Institute (2026); PwC 2025 Global AI Jobs Barometer.", 9, MIDGRAY, first=True)
footer(s, 6)

# ================================================================ 7. SKILLS GAP + CHART
s = prs.slides.add_slide(BLANK)
content_header(s, "04  ·  The widening skills gap", "Demand is shifting fastest where AI exposure is highest")
tb, tf = textbox(s, Inches(0.75), Inches(1.5), Inches(5.3), Inches(4.5))
bullet(tf, "Nearly 1 in 5 European occupations now require AI-related skills — "
           "more than tripled since 2023.", first=True, size=14, space_after=11)
bullet(tf, "Skills sought change 66% faster in roles most exposed to AI.", size=14, space_after=11)
bullet(tf, "Demand for AI fluency rose ~5× between Q4-2023 and Q4-2025.", size=14, space_after=11)
bullet(tf, "Sweden leads — over 1 in 4 occupations require AI skills; Poland and "
           "the UK show the fastest demand growth.", size=14, space_after=11)
bullet(tf, "Yet ~17% of European organisations invest in AI tools without "
           "building the capability to use them.", size=14, space_after=0, marker_color=CORAL)
# bar chart: GenAI job-ad growth by country (yr to Mar 2025)
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
chart_data = CategoryChartData()
chart_data.categories = ["Ireland", "UK", "Germany", "France"]
chart_data.add_series("Growth", (204, 120, 109, 91))
gframe = s.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(6.4), Inches(1.7),
    Inches(6.35), Inches(4.05), chart_data)
chart = gframe.chart
chart.has_legend = False
chart.has_title = True
chart.chart_title.text_frame.text = "Growth in job ads mentioning generative AI (% YoY, to Mar 2025)"
ct = chart.chart_title.text_frame.paragraphs[0].runs[0].font
ct.size = Pt(11); ct.bold = True; ct.color.rgb = NAVY; ct.name = FONT
plot = chart.plots[0]
plot.has_data_labels = True
plot.data_labels.number_format = '0"%"'
plot.data_labels.number_format_is_linked = False
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
plot.data_labels.font.size = Pt(11)
plot.data_labels.font.bold = True
plot.data_labels.font.color.rgb = NAVY
plot.gap_width = 80
ser = plot.series[0]
ser.format.fill.solid()
ser.format.fill.fore_color.rgb = BLUE
cax = chart.category_axis
cax.tick_labels.font.size = Pt(11)
cax.tick_labels.font.color.rgb = GRAY
vax = chart.value_axis
vax.visible = False
vax.has_major_gridlines = False
tb, tf = textbox(s, Inches(0.75), Inches(6.82), Inches(12), Inches(0.3))
para(tf, "Sources: PwC 2025 Global AI Jobs Barometer; McKinsey Global Institute (2026); EPC / ILO (2025).", 9, MIDGRAY, first=True)
footer(s, 7)

# ================================================================ 8. SENTIMENT
s = prs.slides.add_slide(BLANK)
content_header(s, "05  ·  Workforce sentiment & trust", "The human side is eroding — and that is Mercer's right to win")
cards = [
    ("44%", "of employees are ‘thriving’ at work — down sharply from 66% in 2024", CORAL),
    ("40%", "fear losing their job to AI — up from 28% in 2024", NAVY),
    ("63%", "would trade a 10% pay rise for AI & digital upskilling", TEAL),
    ("51%", "of C-suite feel prepared for the human-machine era (was 65%)", BLUE),
]
x = Inches(0.75)
for n, l, c in cards:
    stat_card(s, x, Inches(1.6), Inches(2.92), Inches(2.05), n, l, c)
    x += Inches(3.04)
tb, tf = textbox(s, Inches(0.75), Inches(4.0), Inches(12.05), Inches(2.7))
para(tf, "The readiness gap is a trust gap", 15, NAVY, bold=True, first=True, space_after=8)
bullet(tf, "Falling wellbeing and rising AI anxiety undermine the very adoption "
           "leaders are chasing — disengaged people don't transform.", size=13.5, space_after=8)
bullet(tf, "Employees are hungry to reskill — appetite is not the barrier; "
           "clear pathways, fair reward and trusted change are.", size=13.5, space_after=8)
bullet(tf, "Mercer's heritage in reward, wellbeing, communication and change makes "
           "the human transition our most defensible territory in AI transformation.",
       size=13.5, space_after=0, marker_color=CORAL)
tb, tf = textbox(s, Inches(0.75), Inches(6.82), Inches(12), Inches(0.3))
para(tf, "Source: Mercer Global Talent Trends 2026.", 9, MIDGRAY, first=True)
footer(s, 8)

# ================================================================ 9. IMPLICATIONS FOR MERCER CAREER
s = prs.slides.add_slide(BLANK)
content_header(s, "06  ·  Implications for Mercer Career", "Where demand pulls — and where we must defend")
# Two columns: Demand pull (opportunity) / Pressure (threat)
rect(s, Inches(0.75), Inches(1.55), Inches(5.95), Inches(5.05), WHITE, line=LIGHT)
rect(s, Inches(0.75), Inches(1.55), Inches(5.95), Inches(0.5), TEAL)
tb, tf = textbox(s, Inches(1.0), Inches(1.6), Inches(5.5), Inches(0.42), anchor=MSO_ANCHOR.MIDDLE)
para(tf, "DEMAND PULL — WHERE MERCER WINS", 12.5, WHITE, bold=True, first=True)
tb, tf = textbox(s, Inches(1.0), Inches(2.2), Inches(5.5), Inches(4.3))
for t in [
    ("Skills-based organisation:", " job architecture and skills taxonomies as roles dissolve into tasks."),
    ("AI-ready career frameworks:", " new ladders, internal mobility and talent marketplaces."),
    ("Work & role redesign:", " deciding human vs. AI task allocation, sized for value."),
    ("Reskilling at scale:", " capability strategy, learning pathways, workforce planning."),
    ("Reward recalibration:", " pricing AI-skill premiums and new job values."),
    ("Change, trust & wellbeing:", " the human transition leaders cannot self-serve."),
]:
    bullet(tf, t[1], bold_lead=t[0], size=12.5, space_after=8, marker="✓", marker_color=TEAL)

rect(s, Inches(6.9), Inches(1.55), Inches(5.95), Inches(5.05), WHITE, line=LIGHT)
rect(s, Inches(6.9), Inches(1.55), Inches(5.95), Inches(0.5), CORAL)
tb, tf = textbox(s, Inches(7.15), Inches(1.6), Inches(5.5), Inches(0.42), anchor=MSO_ANCHOR.MIDDLE)
para(tf, "PRESSURE — WHAT WE MUST DEFEND", 12.5, WHITE, bold=True, first=True)
tb, tf = textbox(s, Inches(7.15), Inches(2.2), Inches(5.5), Inches(4.3))
for t in [
    ("Commoditisation:", " AI tools let clients self-serve benchmarking, surveys and job levelling."),
    ("New competitors:", " AI-native HR-tech and platforms entering Mercer's core."),
    ("Speed expectations:", " clients want real-time insight, not annual studies."),
    ("Credibility risk:", " advising on AI work while delivering it manually erodes trust."),
    ("Talent & margin:", " consultants themselves must be AI-fluent to stay productive."),
    ("Data advantage at risk:", " proprietary data must become AI-activated, not static."),
]:
    bullet(tf, t[1], bold_lead=t[0], size=12.5, space_after=8, marker="!", marker_color=CORAL)
footer(s, 9)

# ================================================================ 10. WHERE MERCER IS POSITIONED
s = prs.slides.add_slide(BLANK)
content_header(s, "06  ·  Mercer's starting position", "We are not starting from zero in Europe")
tb, tf = textbox(s, Inches(0.75), Inches(1.55), Inches(12), Inches(0.6))
para(tf, "Existing assets to build on as we scale an AI-and-careers proposition:",
     14, GRAY, first=True)
assets = [
    ("AI advisory solutions", "‘AI Pathmaker’ and Talent & Workforce Strategy offerings help clients chart and govern AI-enabled work."),
    ("European depth", "Acquisition of hkp///group (Germany) and a dedicated UK & Europe Organizational Transformation practice (based in Paris)."),
    ("People-analytics engine", "Partnership with Crunchr (Netherlands) and ‘Mercer Digital’ embed analytics and AI across practices in 40+ countries."),
    ("Skills & reward data", "Deep pay, skills and job-architecture datasets — the raw material for AI-driven career and reward tools."),
    ("Trusted human-capital brand", "Heritage in reward, wellbeing and change gives Mercer permission to own the human side of AI transformation."),
    ("Global Talent Trends platform", "Annual evidence base (≈12,000 voices) positions Mercer as the authority on the future of work."),
]
gx, gy = Inches(0.75), Inches(2.25)
cw, ch = Inches(3.92), Inches(1.95)
for i, (t, d) in enumerate(assets):
    col = i % 3; row = i // 3
    x = gx + col * Inches(4.04); y = gy + row * Inches(2.07)
    rect(s, x, y, cw, ch, LIGHT)
    rect(s, x, y, cw, Inches(0.07), BLUE)
    tbx, tfx = textbox(s, x + Inches(0.22), y + Inches(0.18), cw - Inches(0.44), ch - Inches(0.3))
    para(tfx, t, 13.5, NAVY, bold=True, first=True, space_after=5, line=1.0)
    para(tfx, d, 11.5, GRAY, line=1.06)
tb, tf = textbox(s, Inches(0.75), Inches(6.82), Inches(12), Inches(0.3))
para(tf, "Sources: Mercer.com solutions; Consultancy.eu (2024–25).", 9, MIDGRAY, first=True)
footer(s, 10)

# ================================================================ 11. RECOMMENDATIONS / ROADMAP
s = prs.slides.add_slide(BLANK)
content_header(s, "07  ·  Strategic recommendations", "A horizon-based action agenda for Mercer Career Europe")
horizons = [
    ("NOW  (0–6 months)", BLUE, [
        "Package an ‘AI & the Future of Careers’ POV per major European market.",
        "Launch work-redesign / job-architecture diagnostics as a lead offer.",
        "Equip every Career consultant with AI fluency and AI-assisted delivery.",
    ]),
    ("NEXT  (6–18 months)", TEAL, [
        "Productise skills-based org design and AI-ready career frameworks.",
        "Activate Mercer pay & skills data into AI-driven client tools.",
        "Scale reskilling & internal-mobility programmes with partners.",
    ]),
    ("LATER  (18 months +)", NAVY, [
        "Build a recurring, data-led ‘future-of-work’ subscription model.",
        "Lead on AI workforce governance, ethics and trust advisory.",
        "Embed wellbeing & change as the signature human layer of AI transformation.",
    ]),
]
x = Inches(0.75)
for title, color, pts in horizons:
    rect(s, x, Inches(1.6), Inches(3.94), Inches(5.0), WHITE, line=LIGHT)
    rect(s, x, Inches(1.6), Inches(3.94), Inches(0.62), color)
    tbx, tfx = textbox(s, x + Inches(0.2), Inches(1.64), Inches(3.5), Inches(0.55), anchor=MSO_ANCHOR.MIDDLE)
    para(tfx, title, 13.5, WHITE, bold=True, first=True)
    tbx, tfx = textbox(s, x + Inches(0.25), Inches(2.45), Inches(3.45), Inches(4.0))
    for p in pts:
        bullet(tfx, p, size=12.5, space_after=12, marker="—", marker_color=color, first=(p == pts[0]))
    x += Inches(4.04)
footer(s, 11)

# ================================================================ 12. CLOSING / CALL TO ACTION
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, EMU_W, EMU_H, NAVY)
rect(s, 0, Inches(5.55), EMU_W, Inches(0.12), CORAL)
rect(s, 0, Inches(5.67), EMU_W, Inches(0.05), TEAL)
tb, tf = textbox(s, Inches(0.8), Inches(0.6), Inches(6), Inches(0.7))
para(tf, "MERCER", 22, WHITE, bold=True, first=True)
tb, tf = textbox(s, Inches(0.8), Inches(1.9), Inches(11.7), Inches(3.4))
para(tf, "The opportunity", 15, TEAL, bold=True, first=True, space_after=10)
para(tf, "AI is redrawing European careers — and clients need a trusted guide for "
         "the human side of that change.", 30, WHITE, bold=True, space_after=16, line=1.05)
para(tf, "Mercer's data, European footprint and human-capital heritage make Career "
         "the natural owner of AI-and-work advisory. The window is now.",
     17, RGBColor(0xC7, 0xD4, 0xEA), line=1.12)
tb, tf = textbox(s, Inches(0.8), Inches(5.9), Inches(11.7), Inches(0.9))
para(tf, "Recommended next step:  endorse the NOW agenda and stand up a Europe "
         "‘AI & Careers’ working group.", 14, WHITE, bold=True, first=True)

# ================================================================ 13. APPENDIX — SOURCES
s = prs.slides.add_slide(BLANK)
content_header(s, "Appendix", "Sources & methodology")
tb, tf = textbox(s, Inches(0.75), Inches(1.6), Inches(12), Inches(5.2))
para(tf, "Primary evidence base", 14, NAVY, bold=True, first=True, space_after=8)
srcs = [
    "Mercer, Global Talent Trends 2026 — survey of ≈12,000 executives, HR leaders, employees & investors across 16 geographies and 16 industries (Sep–Oct 2025).",
    "McKinsey Global Institute, ‘Agents, robots, and us: How AI reshapes work and skills in Europe’ (2026) — automation potential, 2030 scenarios, skills overlap.",
    "PwC, 2025 Global AI Jobs Barometer — AI-skill demand, wage premium, occupational exposure.",
    "European Policy Centre (EPC) & International Labour Organization (ILO), generative AI and the EU labour market (2025).",
    "CEPR, ‘How AI is affecting productivity and jobs in Europe’ (2025).",
    "Mercer.com — AI Pathmaker, Talent & Workforce Strategy solutions; Consultancy.eu — hkp///group acquisition, Crunchr partnership, leadership appointments (2024–25).",
]
for sline in srcs:
    bullet(tf, sline, size=12, space_after=9, marker="•", marker_color=BLUE)
para(tf, "Note on branding & figures", 13, NAVY, bold=True, space_before=8, space_after=6)
para(tf, "Colours approximate Mercer's corporate identity for internal use; replace "
         "with the official Mercer template and logo before external distribution. "
         "Statistics are drawn from the published sources above as of June 2026 and "
         "should be re-verified before client use.", 11, GRAY, line=1.1)
footer(s, 13)

# ---------------------------------------------------------------- save
os.makedirs("decks", exist_ok=True)
out = "decks/Mercer_AI_Career_Europe.pptx"
prs.save(out)
print("Saved", out, "with", len(prs.slides._sldIdLst), "slides")
