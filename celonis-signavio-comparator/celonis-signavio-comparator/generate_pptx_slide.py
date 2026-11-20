#!/usr/bin/env python3
"""Generate executive 16:9 PowerPoint slide for Celonis-Signavio-Comparator."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path: str):
    prs = Presentation()
    # 16:9 Widescreen dimensions: 13.333 x 7.5 inches
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # Palette
    C_NAVY = RGBColor(33, 64, 107)       # #21406B
    C_INK = RGBColor(15, 30, 61)         # #0F1E3D
    C_MUTED = RGBColor(87, 87, 87)       # #575757
    C_LIGHT_BG = RGBColor(244, 247, 251) # #F4F7FB
    C_CARD_BG = RGBColor(255, 255, 255)  # #FFFFFF
    C_BORDER = RGBColor(220, 226, 235)   # #DCE2EB
    C_GREEN = RGBColor(25, 128, 56)      # #198038
    C_GREEN_BG = RGBColor(209, 250, 229) # #D1FAE5
    C_RED = RGBColor(218, 30, 40)        # #DA1E28
    C_RED_BG = RGBColor(254, 226, 226)   # #FEE2E2
    C_AMBER = RGBColor(217, 119, 6)      # #D97706
    C_AMBER_BG = RGBColor(254, 243, 199) # #FEF3C7
    C_BLUE_BG = RGBColor(239, 246, 255)  # #EFF6FF

    # 1. Slide Background Canvas
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(235, 241, 247)
    bg_shape.line.fill.background()

    # Main Card Surface
    main_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(0.35), Inches(12.533), Inches(6.8))
    main_card.fill.solid()
    main_card.fill.fore_color.rgb = C_CARD_BG
    main_card.line.color.rgb = C_BORDER
    main_card.line.width = Pt(1)

    # 2. Header Area
    # Header background tint
    hdr_tint = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.35), Inches(12.533), Inches(1.15))
    hdr_tint.fill.solid()
    hdr_tint.fill.fore_color.rgb = C_LIGHT_BG
    hdr_tint.line.fill.background()

    # Kicker + Title + Subtitle Text Box
    hdr_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.42), Inches(8.5), Inches(1.0))
    tf = hdr_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_kicker = tf.paragraphs[0]
    p_kicker.text = "PROCESS STUDIO SKILLATHON • BRING YOUR OWN SKILL (BYOS)"
    p_kicker.font.size = Pt(9.5)
    p_kicker.font.bold = True
    p_kicker.font.color.rgb = C_NAVY

    p_title = tf.add_paragraph()
    p_title.text = "Celonis-Signavio-Comparator"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = C_INK
    p_title.space_before = Pt(2)

    p_sub = tf.add_paragraph()
    p_sub.text = "Where Theory (Signavio BPMN) Meets Reality (Celonis Process Mining)"
    p_sub.font.size = Pt(11.5)
    p_sub.font.color.rgb = C_MUTED
    p_sub.space_before = Pt(2)

    # Header Chips (Right)
    chip1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.5), Inches(0.55), Inches(3.1), Inches(0.36))
    chip1.fill.solid()
    chip1.fill.fore_color.rgb = RGBColor(228, 238, 248)
    chip1.line.color.rgb = RGBColor(180, 205, 230)
    chip1.line.width = Pt(1)
    tf_c1 = chip1.text_frame
    tf_c1.word_wrap = False
    p_c1 = tf_c1.paragraphs[0]
    p_c1.text = "Automated Conformance Checking"
    p_c1.font.size = Pt(9)
    p_c1.font.bold = True
    p_c1.font.color.rgb = C_NAVY
    p_c1.alignment = PP_ALIGN.CENTER

    chip2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.5), Inches(0.98), Inches(3.1), Inches(0.36))
    chip2.fill.solid()
    chip2.fill.fore_color.rgb = RGBColor(228, 238, 248)
    chip2.line.color.rgb = RGBColor(180, 205, 230)
    chip2.line.width = Pt(1)
    tf_c2 = chip2.text_frame
    tf_c2.word_wrap = False
    p_c2 = tf_c2.paragraphs[0]
    p_c2.text = "BPMN 2.0 XML Augmentation"
    p_c2.font.size = Pt(9)
    p_c2.font.bold = True
    p_c2.font.color.rgb = C_NAVY
    p_c2.alignment = PP_ALIGN.CENTER

    # 3. Main Body - 3 Columns
    col_y = Inches(1.65)
    col_h = Inches(4.55)

    # -------------------------------------------------------------
    # Column 1: 01 • DUAL-SOURCE INGESTION (x = 0.65, w = 3.65)
    # -------------------------------------------------------------
    c1_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), col_y, Inches(3.65), col_h)
    c1_bg.fill.solid()
    c1_bg.fill.fore_color.rgb = RGBColor(248, 250, 252)
    c1_bg.line.color.rgb = C_BORDER

    # Col 1 Header Text
    c1_hdr = slide.shapes.add_textbox(Inches(0.8), Inches(1.75), Inches(3.35), Inches(0.6))
    tf1 = c1_hdr.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "01 • DUAL-SOURCE INGESTION"
    p1.font.size = Pt(9)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Theory & Reality Inputs"
    p1_sub.font.size = Pt(13)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = C_INK

    # Box 1.1: Signavio / BPMN
    b1_1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.4), Inches(3.35), Inches(1.15))
    b1_1.fill.solid()
    b1_1.fill.fore_color.rgb = C_CARD_BG
    b1_1.line.color.rgb = C_BORDER
    tf_b1 = b1_1.text_frame
    tf_b1.margin_left = tf_b1.margin_right = Inches(0.12)
    tf_b1.margin_top = Inches(0.08)
    p = tf_b1.paragraphs[0]
    p.text = "1. Signavio Context / BPMN"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p_desc = tf_b1.add_paragraph()
    p_desc.text = "Uploaded BPMN 2.0 XML file, direct prompt attachment, or auto-retrieved from connected Signavio context / workspace repository."
    p_desc.font.size = Pt(8.5)
    p_desc.font.color.rgb = C_MUTED
    p_desc.space_before = Pt(2)

    # Box 1.2: Celonis Execution Reality
    b1_2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.65), Inches(3.35), Inches(1.15))
    b1_2.fill.solid()
    b1_2.fill.fore_color.rgb = C_CARD_BG
    b1_2.line.color.rgb = C_BORDER
    tf_b2 = b1_2.text_frame
    tf_b2.margin_left = tf_b2.margin_right = Inches(0.12)
    tf_b2.margin_top = Inches(0.08)
    p = tf_b2.paragraphs[0]
    p.text = "2. Celonis Execution Reality"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p_desc = tf_b2.add_paragraph()
    p_desc.text = "Transactional event logs (_CEL_P2P_ACTIVITIES), PQL query analytics, activity frequencies, waiting times, and bottleneck data."
    p_desc.font.size = Pt(8.5)
    p_desc.font.color.rgb = C_MUTED
    p_desc.space_before = Pt(2)

    # Box 1.3: Zero-Code Spec
    b1_3 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.9), Inches(3.35), Inches(1.15))
    b1_3.fill.solid()
    b1_3.fill.fore_color.rgb = C_CARD_BG
    b1_3.line.color.rgb = C_BORDER
    tf_b3 = b1_3.text_frame
    tf_b3.margin_left = tf_b3.margin_right = Inches(0.12)
    tf_b3.margin_top = Inches(0.08)
    p = tf_b3.paragraphs[0]
    p.text = "3. Zero-Code Data Contract"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p_desc = tf_b3.add_paragraph()
    p_desc.text = "Agent authors comparison-spec.json containing verified metrics, flow transitions, root causes, and reconciliation actions."
    p_desc.font.size = Pt(8.5)
    p_desc.font.color.rgb = C_MUTED
    p_desc.space_before = Pt(2)

    # -------------------------------------------------------------
    # Column 2: 02 • COMPARISON ENGINE (x = 4.45, w = 4.45) - HERO
    # -------------------------------------------------------------
    c2_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.45), col_y, Inches(4.45), col_h)
    c2_bg.fill.solid()
    c2_bg.fill.fore_color.rgb = RGBColor(244, 247, 251)
    c2_bg.line.color.rgb = C_NAVY
    c2_bg.line.width = Pt(1.5)

    c2_hdr = slide.shapes.add_textbox(Inches(4.6), Inches(1.75), Inches(4.15), Inches(0.6))
    tf2 = c2_hdr.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "02 • COMPARISON ENGINE"
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = C_NAVY
    p2_sub = tf2.add_paragraph()
    p2_sub.text = "Theory vs. Reality Analysis"
    p2_sub.font.size = Pt(13)
    p2_sub.font.bold = True
    p2_sub.font.color.rgb = C_INK

    # 4 Delta KPI Tiles (2x2 Grid)
    # Top Left: Happy Path
    tile1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.6), Inches(2.4), Inches(2.0), Inches(1.1))
    tile1.fill.solid()
    tile1.fill.fore_color.rgb = C_CARD_BG
    tile1.line.color.rgb = C_GREEN
    tile1.line.width = Pt(1.5)
    tf_t1 = tile1.text_frame
    tf_t1.margin_left = tf_t1.margin_right = Inches(0.08)
    tf_t1.margin_top = Inches(0.08)
    p = tf_t1.paragraphs[0]
    p.text = "68.2%"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p_t1_l = tf_t1.add_paragraph()
    p_t1_l.text = "Happy Path Fitness"
    p_t1_l.font.size = Pt(8.5)
    p_t1_l.font.bold = True
    p_t1_l.font.color.rgb = C_INK
    p_t1_s = tf_t1.add_paragraph()
    p_t1_s.text = "Strict Signavio conformance"
    p_t1_s.font.size = Pt(7.5)
    p_t1_s.font.color.rgb = C_MUTED

    # Top Right: Rework & Friction
    tile2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(2.4), Inches(2.0), Inches(1.1))
    tile2.fill.solid()
    tile2.fill.fore_color.rgb = C_CARD_BG
    tile2.line.color.rgb = C_RED
    tile2.line.width = Pt(1.5)
    tf_t2 = tile2.text_frame
    tf_t2.margin_left = tf_t2.margin_right = Inches(0.08)
    tf_t2.margin_top = Inches(0.08)
    p = tf_t2.paragraphs[0]
    p.text = "31.8%"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p_t2_l = tf_t2.add_paragraph()
    p_t2_l.text = "Rework & Exceptions"
    p_t2_l.font.size = Pt(8.5)
    p_t2_l.font.bold = True
    p_t2_l.font.color.rgb = C_INK
    p_t2_s = tf_t2.add_paragraph()
    p_t2_s.text = "+8.6 days execution delay"
    p_t2_s.font.size = Pt(7.5)
    p_t2_s.font.color.rgb = C_MUTED

    # Bottom Left: Maverick Invoicing
    tile3 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.6), Inches(3.6), Inches(2.0), Inches(1.1))
    tile3.fill.solid()
    tile3.fill.fore_color.rgb = C_CARD_BG
    tile3.line.color.rgb = C_RED
    tile3.line.width = Pt(1.5)
    tf_t3 = tile3.text_frame
    tf_t3.margin_left = tf_t3.margin_right = Inches(0.08)
    tf_t3.margin_top = Inches(0.08)
    p = tf_t3.paragraphs[0]
    p.text = "7.0%"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p_t3_l = tf_t3.add_paragraph()
    p_t3_l.text = "Maverick Buying"
    p_t3_l.font.size = Pt(8.5)
    p_t3_l.font.bold = True
    p_t3_l.font.color.rgb = C_INK
    p_t3_s = tf_t3.add_paragraph()
    p_t3_s.text = "77.9k PO-less invoices"
    p_t3_s.font.size = Pt(7.5)
    p_t3_s.font.color.rgb = C_MUTED

    # Bottom Right: Invoice-to-Pay Lag
    tile4 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(3.6), Inches(2.0), Inches(1.1))
    tile4.fill.solid()
    tile4.fill.fore_color.rgb = C_CARD_BG
    tile4.line.color.rgb = C_AMBER
    tile4.line.width = Pt(1.5)
    tf_t4 = tile4.text_frame
    tf_t4.margin_left = tf_t4.margin_right = Inches(0.08)
    tf_t4.margin_top = Inches(0.08)
    p = tf_t4.paragraphs[0]
    p.text = "11.7 d"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p_t4_l = tf_t4.add_paragraph()
    p_t4_l.text = "Invoice -> Pay Lag"
    p_t4_l.font.size = Pt(8.5)
    p_t4_l.font.bold = True
    p_t4_l.font.color.rgb = C_INK
    p_t4_s = tf_t4.add_paragraph()
    p_t4_s.text = "10.6M case-days latency"
    p_t4_s.font.size = Pt(7.5)
    p_t4_s.font.color.rgb = C_MUTED

    # Flow Map Representation Box (Bottom of Col 2)
    flow_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.6), Inches(4.8), Inches(4.15), Inches(1.25))
    flow_box.fill.solid()
    flow_box.fill.fore_color.rgb = C_CARD_BG
    flow_box.line.color.rgb = C_BORDER
    tf_flow = flow_box.text_frame
    tf_flow.margin_left = tf_flow.margin_right = Inches(0.1)
    tf_flow.margin_top = Inches(0.06)
    p = tf_flow.paragraphs[0]
    p.text = "Process Conformance & Shadow Flow Detection"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    p_f1 = tf_flow.add_paragraph()
    p_f1.text = "• Happy Path: Create PR → Create PO → Send PO → Goods Receipt → Invoice → Pay"
    p_f1.font.size = Pt(8)
    p_f1.font.color.rgb = C_GREEN
    p_f1.space_before = Pt(3)

    p_f2 = tf_flow.add_paragraph()
    p_f2.text = "• Discovered Shadow Branch: Post-PO Price Change (13.6% cases, +8.8d delay)"
    p_f2.font.size = Pt(8)
    p_f2.font.color.rgb = C_RED
    p_f2.space_before = Pt(2)

    p_f3 = tf_flow.add_paragraph()
    p_f3.text = "• Discovered Exception Loop: Payment Block & Release (2.3% cases, +11.4d delay)"
    p_f3.font.size = Pt(8)
    p_f3.font.color.rgb = C_RED
    p_f3.space_before = Pt(2)

    # -------------------------------------------------------------
    # Column 3: 03 • 4 ACTIONABLE DELIVERABLES (x = 9.05, w = 3.5)
    # -------------------------------------------------------------
    c3_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.05), col_y, Inches(3.5), col_h)
    c3_bg.fill.solid()
    c3_bg.fill.fore_color.rgb = RGBColor(248, 250, 252)
    c3_bg.line.color.rgb = C_BORDER

    c3_hdr = slide.shapes.add_textbox(Inches(9.2), Inches(1.75), Inches(3.2), Inches(0.6))
    tf3 = c3_hdr.text_frame
    tf3.word_wrap = True
    p3 = tf3.paragraphs[0]
    p3.text = "03 • DELIVERABLES"
    p3.font.size = Pt(9)
    p3.font.bold = True
    p3.font.color.rgb = C_NAVY
    p3_sub = tf3.add_paragraph()
    p3_sub.text = "4 Actionable Deliverables"
    p3_sub.font.size = Pt(13)
    p3_sub.font.bold = True
    p3_sub.font.color.rgb = C_INK

    deliverables = [
        ("1. Executive HTML Report", "Interactive HTML with KPI scorecards, deviation register, bottleneck charts & roadmap.", "HTML Report", C_BLUE_BG, C_NAVY),
        ("2. BPMN Conformance Heatmap", "Color-coded BPMN 2.0 diagram (Green/Amber/Red) with performance text annotations.", "BPMN 2.0 XML", C_GREEN_BG, C_GREEN),
        ("3. Clean Signavio To-Be Model", "Standardized BPMN with swimlanes (Purchasing, Logistics, AP) for direct Signavio import.", "Signavio XML", C_BLUE_BG, C_NAVY),
        ("4. Review Matrix & Action Plan", "Multi-sheet Excel review workbook with editable Decision dropdowns for workshops.", "Excel (.XLSX)", C_AMBER_BG, C_AMBER)
    ]

    for idx, (title, desc, tag, bg_c, fg_c) in enumerate(deliverables):
        d_y = Inches(2.4 + (idx * 0.95))
        d_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), d_y, Inches(3.2), Inches(0.88))
        d_box.fill.solid()
        d_box.fill.fore_color.rgb = C_CARD_BG
        d_box.line.color.rgb = C_BORDER
        tf_d = d_box.text_frame
        tf_d.margin_left = tf_d.margin_right = Inches(0.1)
        tf_d.margin_top = Inches(0.06)

        p_dt = tf_d.paragraphs[0]
        p_dt.text = title
        p_dt.font.size = Pt(9.5)
        p_dt.font.bold = True
        p_dt.font.color.rgb = C_INK

        p_dd = tf_d.add_paragraph()
        p_dd.text = desc
        p_dd.font.size = Pt(7.5)
        p_dd.font.color.rgb = C_MUTED
        p_dd.space_before = Pt(1)

    # 4. Bottom Value Strip (y = 6.35, h = 0.7)
    foot_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(6.35), Inches(12.533), Inches(0.8))
    foot_bg.fill.solid()
    foot_bg.fill.fore_color.rgb = C_LIGHT_BG
    foot_bg.line.fill.background()

    foot_pillars = [
        ("✓ Reconciles Theory & Reality", "Bridges designed SOPs with event reality"),
        ("⚡ Uncovers Shadow Work", "Reveals hidden rework & maverick buying"),
        ("↻ Signavio Round-Trip Ready", "Direct production re-import to Signavio"),
        ("⚖ Governed Decision Making", "Structured workshop sign-off sheet")
    ]

    for idx, (p_title, p_desc) in enumerate(foot_pillars):
        p_x = Inches(0.65 + (idx * 3.1))
        p_box = slide.shapes.add_textbox(p_x, Inches(6.38), Inches(3.0), Inches(0.7))
        tf_p = p_box.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0

        p1 = tf_p.paragraphs[0]
        p1.text = p_title
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY

        p2 = tf_p.add_paragraph()
        p2.text = p_desc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_MUTED

    prs.save(output_path)
    print(f"PASS: saved PowerPoint presentation to {output_path}")

if __name__ == "__main__":
    out_file = "/Users/mohamedi/Documents/Repos/Skillathon/process-studio-skills/celonis-signavio-comparator/celonis-signavio-comparator-slide.pptx"
    create_deck(out_file)
