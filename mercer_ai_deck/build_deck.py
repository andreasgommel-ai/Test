"""
Build: "The Impact of AI on Careers in Europe" — Mercer-branded executive deck.

Run:  python build_deck.py
Out:  Mercer_AI_Impact_Careers_Europe.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from mercer_brand import (
    C, FONT_HEAD, FONT_BODY, SLIDE_W, SLIDE_H,
    _blank, rect, textbox, bullets, logo, footer, section_header,
)

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H

TOTAL = 12


def source_note(slide, text):
    textbox(slide, Inches(0.85), Inches(6.62), Inches(11.9), Inches(0.32),
            [{"text": "Source: " + text, "size": 7.5, "color": C.SLATE,
              "italic": True, "font": FONT_BODY}])


def stat_card(slide, x, y, w, h, number, label, num_color=C.BLUE,
              bg=C.LIGHT_BG):
    rect(slide, x, y, w, h, bg, MSO_SHAPE.ROUNDED_RECTANGLE)
    # top accent strip
    rect(slide, x, y, w, Inches(0.09), C.TEAL, MSO_SHAPE.RECTANGLE)
    textbox(slide, x + Inches(0.18), y + Inches(0.28), w - Inches(0.36),
            Inches(0.95),
            [{"text": number, "size": 40, "color": num_color, "bold": True,
              "font": FONT_HEAD}])
    textbox(slide, x + Inches(0.18), y + Inches(1.25), w - Inches(0.36),
            h - Inches(1.35),
            [{"text": label, "size": 11.5, "color": C.INK, "font": FONT_BODY}])


# ===========================================================================
# SLIDE 1 — TITLE
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.NAVY)
# decorative accent band
rect(s, 0, Inches(5.55), SLIDE_W, Inches(0.10), C.TEAL)
rect(s, Inches(0.9), Inches(2.0), Inches(0.9), Inches(0.14), C.TEAL)
logo(s, color=C.WHITE)
textbox(s, Inches(0.9), Inches(2.35), Inches(11.5), Inches(2.2),
        [{"text": "The Impact of AI on", "size": 46, "color": C.WHITE,
          "font": FONT_HEAD, "space_after": 2},
         {"text": "Careers in Europe", "size": 46, "color": C.SKY,
          "font": FONT_HEAD}])
textbox(s, Inches(0.9), Inches(4.55), Inches(11.0), Inches(0.9),
        [{"text": "What generative and agentic AI mean for the European "
                  "workforce — and how Mercer is helping organisations "
                  "redesign work, reward and careers.", "size": 15,
          "color": C.SKY, "font": FONT_BODY}])
textbox(s, Inches(0.9), Inches(5.85), Inches(11.0), Inches(0.5),
        [{"text": "Executive briefing  ·  June 2026  ·  Mercer Career — Europe",
          "size": 12, "color": C.WHITE, "font": FONT_BODY, "bold": True}])

# ===========================================================================
# SLIDE 2 — EXECUTIVE SUMMARY
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.WHITE)
section_header(s, "Executive summary", "Five things European leaders need to know")
items = [
    "AI exposure is broad, not catastrophic. The IMF estimates ~60% of jobs in advanced economies are exposed to AI — about half complemented (productivity upside), half at risk of disruption.",
    "Net effect in Europe is job-positive but disruptive. The WEF projects AI creates ~11M and displaces ~9M European jobs to 2030, with ~12M occupational transitions and ~27% of work hours automatable.",
    "Skills are the bottleneck. ~39% of core skills will change by 2030 and 6 in 10 EU workers face task transformation — yet only 56% of EU adults have basic digital skills and 44% doubt their employer will train them.",
    "Europe regulates first. The EU AI Act makes most HR uses of AI (hiring, promotion, monitoring) 'high-risk', with worker-notification duties — reshaping how AI can be deployed in the workplace.",
    "Mercer's answer: redesign work, not just jobs. Backed by new AI tools (Workforce Insights, Aida) and skills-based services, Mercer helps clients turn disruption into productivity and engagement.",
]
bullets(s, Inches(0.85), Inches(1.75), Inches(11.9), Inches(4.9), items,
        size=13.5, gap=12)
footer(s, 2, TOTAL)

# ===========================================================================
# SLIDE 3 — SCALE OF EXPOSURE
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.WHITE)
section_header(s, "The scale", "AI touches most European jobs — but exposure is not destiny")
stat_card(s, Inches(0.85), Inches(1.85), Inches(3.7), Inches(2.5),
          "~60%", "of jobs in advanced economies (incl. Western Europe) are "
          "exposed to AI — roughly half complemented, half at risk  (IMF, 2024)")
stat_card(s, Inches(4.82), Inches(1.85), Inches(3.7), Inches(2.5),
          "~2 in 3", "jobs in the US and Europe are exposed to some degree of "
          "AI automation; clerical roles ~45% vs ~4% in trades  (Goldman Sachs)")
stat_card(s, Inches(8.79), Inches(1.85), Inches(3.7), Inches(2.5),
          "27–28%", "of jobs across OECD economies sit in occupations at the "
          "highest risk of automation  (OECD)")
textbox(s, Inches(0.85), Inches(4.75), Inches(11.9), Inches(1.6),
        [{"text": "Exposure ≠ displacement.", "size": 15, "color": C.BLUE,
          "bold": True, "font": FONT_HEAD, "space_after": 4},
         {"text": "Both the IMF and OECD stress that 'exposure' measures the "
          "tasks AI can touch — not jobs lost. For roughly half of exposed "
          "roles, AI augments people and lifts productivity. The decisive "
          "variable is how organisations choose to redesign the work.",
          "size": 13, "color": C.INK, "font": FONT_BODY}])
source_note(s, "IMF Gen-AI & the Future of Work (2024); Goldman Sachs (2023); OECD Employment Outlook / AI & Work.")
footer(s, 3, TOTAL)

# ===========================================================================
# SLIDE 4 — JOBS CREATED VS DISPLACED
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.WHITE)
section_header(s, "Jobs", "Europe: more jobs created than displaced — amid heavy churn")
stat_card(s, Inches(0.85), Inches(1.85), Inches(3.7), Inches(2.5),
          "+11M", "European jobs created by AI & information-processing tech "
          "by 2030 — the largest impact of any technology  (WEF, 2025)",
          num_color=C.TEAL)
stat_card(s, Inches(4.82), Inches(1.85), Inches(3.7), Inches(2.5),
          "−9M", "European jobs displaced over the same period — a net "
          "positive, but with significant transition  (WEF, 2025)",
          num_color=C.BLUE_MID)
stat_card(s, Inches(8.79), Inches(1.85), Inches(3.7), Inches(2.5),
          "~12M", "occupational transitions may be needed in Europe by 2030; "
          "~27% of current work hours are automatable  (McKinsey, 2024)")
textbox(s, Inches(0.85), Inches(4.75), Inches(11.9), Inches(1.6),
        [{"text": "Where demand shifts:", "size": 15, "color": C.BLUE,
          "bold": True, "font": FONT_HEAD, "space_after": 4},
         {"text": "Demand rises for STEM, healthcare and other high-skill "
          "roles, and falls for office/clerical, production and customer-"
          "service roles. Globally the WEF sees a net +78M jobs (+7%) by 2030 "
          "— but 22% structural churn of all roles studied.", "size": 13,
          "color": C.INK, "font": FONT_BODY}])
source_note(s, "WEF Future of Jobs Report 2025; McKinsey, 'A new future of work: …Europe and beyond' (2024).")
footer(s, 4, TOTAL)

# ===========================================================================
# SLIDE 5 — PRODUCTIVITY PRIZE
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.WHITE)
section_header(s, "The prize", "The upside is a productivity step-change — if adoption is paired with reskilling")
stat_card(s, Inches(0.85), Inches(1.85), Inches(3.7), Inches(2.5),
          "~3%", "potential annual productivity growth for Europe to 2030 with "
          "fast adoption + redeployment — vs ~0.3% if slow  (McKinsey)",
          num_color=C.TEAL)
stat_card(s, Inches(4.82), Inches(1.85), Inches(3.7), Inches(2.5),
          "~4x", "faster productivity growth in the most AI-exposed industries "
          "(7% → 27% revenue per employee)  (PwC, 2025)")
stat_card(s, Inches(8.79), Inches(1.85), Inches(3.7), Inches(2.5),
          "+56%", "wage premium for roles requiring AI skills — up from 25% a "
          "year earlier  (PwC Global AI Jobs Barometer, 2025)",
          num_color=C.BLUE_MID)
textbox(s, Inches(0.85), Inches(4.75), Inches(11.9), Inches(1.6),
        [{"text": "The value is conditional.", "size": 15, "color": C.BLUE,
          "bold": True, "font": FONT_HEAD, "space_after": 4},
         {"text": "McKinsey's high-growth scenario depends on rapid adoption "
          "AND proactive worker redeployment. Technology alone doesn't deliver "
          "the gain — the work, the skills and the operating model have to be "
          "redesigned around it.", "size": 13, "color": C.INK,
          "font": FONT_BODY}])
source_note(s, "McKinsey (2024); PwC 2025 Global AI Jobs Barometer.")
footer(s, 5, TOTAL)

# ===========================================================================
# SLIDE 6 — SKILLS SHIFT
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.WHITE)
section_header(s, "The bottleneck", "Skills are the real constraint on Europe's AI dividend")
stat_card(s, Inches(0.85), Inches(1.85), Inches(2.78), Inches(2.5),
          "39%", "of workers' core skills will be transformed or outdated by "
          "2030  (WEF, global)")
stat_card(s, Inches(3.77), Inches(1.85), Inches(2.78), Inches(2.5),
          "6 in 10", "EU workers are susceptible to AI-related task "
          "transformation  (Cedefop, 2024)", num_color=C.TEAL)
stat_card(s, Inches(6.69), Inches(1.85), Inches(2.78), Inches(2.5),
          "56%", "of EU adults have at least basic digital skills — vs an 80% "
          "target for 2030  (Eurostat)", num_color=C.BLUE_MID)
stat_card(s, Inches(9.61), Inches(1.85), Inches(2.78), Inches(2.5),
          "9.7M", "shortfall of ICT specialists against the EU's 2030 goal  "
          "(Eurostat)")
textbox(s, Inches(0.85), Inches(4.75), Inches(11.9), Inches(1.6),
        [{"text": "Willing workers, hesitant employers.", "size": 15,
          "color": C.BLUE, "bold": True, "font": FONT_HEAD, "space_after": 4},
         {"text": "61% of EU workers expect to need new skills, but 44% doubt "
          "their employer will provide adequate AI training. Analytical "
          "thinking and 'AI & big data' top the fastest-growing skills; "
          "EU professionals adding AI-literacy skills grew 80-fold in a year.",
          "size": 13, "color": C.INK, "font": FONT_BODY}])
source_note(s, "WEF Future of Jobs 2025; Cedefop AI Skills Survey (2024); Eurostat Digital Decade; LinkedIn Economic Graph.")
footer(s, 6, TOTAL)

# ===========================================================================
# SLIDE 7 — REGULATORY FRONTIER
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.WHITE)
section_header(s, "The European frontier", "Europe regulates AI at work first — and unevenly adopts it")
bullets(s, Inches(0.85), Inches(1.8), Inches(6.0), Inches(4.6), [
    "EU AI Act in force since Aug 2024; prohibited practices apply from Feb 2025, high-risk obligations from Aug 2026.",
    "Most HR uses of AI — recruitment, candidate filtering, promotion, termination, task allocation, performance monitoring — are classified 'high-risk' (Annex III).",
    "Employers must ensure human oversight, keep logs ≥6 months, and inform workers' representatives before deploying high-risk AI (Art. 26).",
    "Emotion-recognition AI in the workplace is banned; breaches of prohibited practices carry fines up to 7% of global turnover.",
], size=12.5, gap=11)
# right column adoption stats
rect(s, Inches(7.15), Inches(1.8), Inches(5.6), Inches(4.55), C.LIGHT_BG,
     MSO_SHAPE.ROUNDED_RECTANGLE)
rect(s, Inches(7.15), Inches(1.8), Inches(5.6), Inches(0.09), C.TEAL)
textbox(s, Inches(7.45), Inches(2.05), Inches(5.0), Inches(0.5),
        [{"text": "A two-speed Europe", "size": 16, "color": C.BLUE,
          "bold": True, "font": FONT_HEAD}])
bullets(s, Inches(7.45), Inches(2.65), Inches(5.0), Inches(3.5), [
    "20% of EU enterprises (10+ staff) used AI in 2025 — up from 13.5% in 2024.",
    "~55% of large firms use AI vs ~17% of small firms.",
    "Leaders: Denmark 42%, Finland 38%, Sweden 35%. Laggards: Romania 5%, Poland 8%.",
    "Positive attitudes to AI rose to 70% (EY, 2025) — but a 19pt management-vs-staff gap remains.",
], size=12, gap=9)
source_note(s, "European Commission EU AI Act; Eurostat (Dec 2025); EY European AI Barometer 2025.")
footer(s, 7, TOTAL)

# ===========================================================================
# SLIDE 8 — HUMAN DIMENSION (Mercer GTT)
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.WHITE)
section_header(s, "The human dimension", "Mercer's data: anxiety is up, thriving is down — trust is the gap")
stat_card(s, Inches(0.85), Inches(1.85), Inches(3.7), Inches(2.5),
          "66→44%", "share of employees 'thriving' fell from 2024 to 2026 — "
          "the lowest Mercer has recorded", num_color=C.BLUE_MID)
stat_card(s, Inches(4.82), Inches(1.85), Inches(3.7), Inches(2.5),
          "28→40%", "rise in employees concerned about losing their job to AI "
          "(2024 → 2026)", num_color=C.BLUE)
stat_card(s, Inches(8.79), Inches(1.85), Inches(3.7), Inches(2.5),
          "63%", "of employees would trade a 10% pay rise for AI & digital "
          "upskilling and career development", num_color=C.TEAL)
textbox(s, Inches(0.85), Inches(4.75), Inches(11.9), Inches(1.6),
        [{"text": "Readiness lags ambition.", "size": 15, "color": C.BLUE,
          "bold": True, "font": FONT_HEAD, "space_after": 4},
         {"text": "98% of executives plan organisational redesign and 65% "
          "expect 11–30% of staff reskilled or redeployed within two years — "
          "yet only ~1 in 3 firms use GenAI regularly, and 67% of HR leaders "
          "admit they deployed technology without redesigning the work.",
          "size": 13, "color": C.INK, "font": FONT_BODY}])
source_note(s, "Mercer Global Talent Trends 2024 & 2026.")
footer(s, 8, TOTAL)

# ===========================================================================
# SLIDE 9 — MERCER POINT OF VIEW (divider-style, navy)
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.NAVY)
rect(s, Inches(0.9), Inches(1.6), Inches(0.9), Inches(0.14), C.TEAL)
textbox(s, Inches(0.9), Inches(1.0), Inches(8), Inches(0.4),
        [{"text": "MERCER'S POINT OF VIEW", "size": 12, "color": C.TEAL,
          "bold": True, "font": FONT_BODY}])
textbox(s, Inches(0.9), Inches(1.95), Inches(11.5), Inches(1.2),
        [{"text": "Redesign work — not just jobs.", "size": 38,
          "color": C.WHITE, "font": FONT_HEAD}])
cols = [
    ("Decompose & redesign", "Break jobs into tasks to decide what AI automates, what it augments and what stays human — then rebuild roles around the new mix."),
    ("Go skills-based", "Shift from rigid job structures to a skills-powered model: a single skills taxonomy, skills-to-job mapping, and paying for skills."),
    ("Lead human-centric", "Pair AI adoption with trust, transparency and reskilling. 'Human-centric productivity' leaders see far higher efficiency and innovation gains."),
]
x = Inches(0.9)
for title, body in cols:
    rect(s, x, Inches(3.55), Inches(3.7), Inches(0.07), C.TEAL)
    textbox(s, x, Inches(3.75), Inches(3.7), Inches(0.6),
            [{"text": title, "size": 17, "color": C.SKY, "bold": True,
              "font": FONT_HEAD}])
    textbox(s, x, Inches(4.45), Inches(3.7), Inches(2.0),
            [{"text": body, "size": 12.5, "color": C.WHITE, "font": FONT_BODY}])
    x = x + Inches(3.97)
footer(s, 9, TOTAL, dark=True)

# ===========================================================================
# SLIDE 10 — HOW MERCER IS RESPONDING (services)
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.WHITE)
section_header(s, "Angle 2 — Mercer's own transformation",
               "AI is now embedded in Mercer's Career services")
cards = [
    ("Workforce Insights + Aida", "AI-powered benchmarking across 100+ countries & 20,000 organisations, with 'Aida' — a proprietary AI assistant for natural-language queries on pay, talent and compliance.  (Launched Oct 2025)"),
    ("Skills Edge & Skills Library", "Award-winning skills-based talent management; AI matches jobs to skills using partner databases that scan millions of job profiles.  (2024 HR Tech Award)"),
    ("AI Pathmaker", "Consulting service to adopt AI responsibly — work redesign, AI ROI and building a future-fit, reskilled workforce."),
    ("Data Connector & IPE", "AI-assisted job matching and grading tied to Mercer's compensation surveys and the International Position Evaluation framework."),
]
positions = [(Inches(0.85), Inches(1.8)), (Inches(6.85), Inches(1.8)),
             (Inches(0.85), Inches(4.15)), (Inches(6.85), Inches(4.15))]
for (title, body), (x, y) in zip(cards, positions):
    rect(s, x, y, Inches(5.9), Inches(2.15), C.LIGHT_BG,
         MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s, x, y, Inches(0.10), Inches(2.15), C.TEAL)
    textbox(s, x + Inches(0.3), y + Inches(0.22), Inches(5.4), Inches(0.5),
            [{"text": title, "size": 16, "color": C.BLUE, "bold": True,
              "font": FONT_HEAD}])
    textbox(s, x + Inches(0.3), y + Inches(0.78), Inches(5.4), Inches(1.25),
            [{"text": body, "size": 11.5, "color": C.INK, "font": FONT_BODY}])
source_note(s, "Mercer newsroom & solution pages (2024–2026). Some client outcomes are Mercer-reported.")
footer(s, 10, TOTAL)

# ===========================================================================
# SLIDE 11 — RECOMMENDATIONS
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.WHITE)
section_header(s, "What to do now", "A five-move agenda for HR, reward & talent leaders")
recs = [
    ("1.  Map exposure & redesign work", "Assess which roles and tasks AI can augment vs automate; redesign the highest-impact roles before scaling tools."),
    ("2.  Build a skills-based foundation", "Stand up a single skills taxonomy, map skills to jobs, and start paying for skills — the operating system for an AI-era workforce."),
    ("3.  Invest visibly in reskilling", "Close the trust gap: workers will trade pay for development, but 44% doubt training will come. Make commitments concrete and funded."),
    ("4.  Get AI-in-HR governance right", "Treat hiring, promotion and monitoring AI as 'high-risk' under the EU AI Act — human oversight, worker notification, logging and bias testing."),
    ("5.  Lead human-centric productivity", "Pair adoption with transparency, manager capability and pay equity to convert AI into both productivity and engagement."),
]
y = Inches(1.8)
for title, body in recs:
    rect(s, Inches(0.85), y + Inches(0.05), Inches(0.14), Inches(0.62), C.TEAL)
    textbox(s, Inches(1.15), y, Inches(4.3), Inches(0.9),
            [{"text": title, "size": 14, "color": C.BLUE, "bold": True,
              "font": FONT_HEAD}])
    textbox(s, Inches(5.6), y + Inches(0.02), Inches(7.1), Inches(0.9),
            [{"text": body, "size": 12.5, "color": C.INK, "font": FONT_BODY}])
    y = y + Inches(0.97)
footer(s, 11, TOTAL)

# ===========================================================================
# SLIDE 12 — CLOSING / SOURCES
# ===========================================================================
s = _blank(prs)
rect(s, 0, 0, SLIDE_W, SLIDE_H, C.NAVY)
rect(s, 0, Inches(5.55), SLIDE_W, Inches(0.10), C.TEAL)
logo(s, color=C.WHITE)
textbox(s, Inches(0.9), Inches(2.1), Inches(11.4), Inches(1.4),
        [{"text": "Turn AI disruption into", "size": 38, "color": C.WHITE,
          "font": FONT_HEAD, "space_after": 2},
         {"text": "a people advantage.", "size": 38, "color": C.SKY,
          "font": FONT_HEAD}])
textbox(s, Inches(0.9), Inches(3.95), Inches(11.0), Inches(0.8),
        [{"text": "Let's discuss how Mercer can help your organisation in "
                  "Europe redesign work, reward and careers for the AI era.",
          "size": 14, "color": C.SKY, "font": FONT_BODY}])
textbox(s, Inches(0.9), Inches(5.85), Inches(11.6), Inches(1.4),
        [{"text": "KEY SOURCES", "size": 9, "color": C.TEAL, "bold": True,
          "font": FONT_BODY, "space_after": 3},
         {"text": "IMF Gen-AI & the Future of Work (2024) · WEF Future of Jobs "
          "2025 · McKinsey 'A new future of work …Europe' (2024) · PwC Global "
          "AI Jobs Barometer 2025 · Cedefop AI Skills Survey 2024 · Eurostat "
          "Digital Decade · OECD · European Commission EU AI Act · EY European "
          "AI Barometer 2025 · Mercer Global Talent Trends 2024 & 2026.",
          "size": 9.5, "color": C.WHITE, "font": FONT_BODY}])

prs.save("Mercer_AI_Impact_Careers_Europe.pptx")
print("Saved Mercer_AI_Impact_Careers_Europe.pptx with", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
