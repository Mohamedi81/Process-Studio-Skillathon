#!/usr/bin/env python3
"""Build Celonis-Signavio-Comparator presentation matching the exact look-and-feel of BusinessUserJourneyWorkshopPack_oneSlide.pptx."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def build_slide(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # IBM Carbon Brand Colors
    C_BLUE = RGBColor(15, 98, 254)       # #0F62FE (IBM Blue 60)
    C_PURPLE = RGBColor(138, 63, 252)    # #8A3FFC (IBM Purple 60)
    C_DARK = RGBColor(22, 22, 22)        # #161616 (IBM Gray 100)
    C_GRAY = RGBColor(82, 82, 82)        # #525252 (IBM Gray 70)
    C_LIGHT_BG = RGBColor(244, 244, 244) # #F4F4F4 (IBM Gray 10)
    C_BORDER = RGBColor(224, 224, 224)   # #E0E0E0 (IBM Gray 20)
    C_WHITE = RGBColor(255, 255, 255)
    C_ARROW = RGBColor(82, 82, 82)       # #525252

    # 1. Main Header Title
    title_box = slide.shapes.add_textbox(Inches(0.60), Inches(0.35), Inches(12.13), Inches(0.52))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = "Process Conformance & Augmentation: Where Theory Meets Reality"
    p_title.font.name = "Calibri"
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = C_DARK

    # 2. Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.60), Inches(1.00), Inches(12.13), Inches(0.40))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "A Process Studio BYOS skill that reconciles designed Signavio BPMN models with Celonis execution event logs"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = C_GRAY

    # 3. Accent Line under Title
    accent_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.60), Inches(1.48), Inches(1.20), Inches(0.04))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = C_BLUE
    accent_bar.line.fill.background()

    # -------------------------------------------------------------
    # 4. Top Left Card: WHY IT'S THERE (x=0.60, y=1.75, w=3.91, h=2.55)
    # -------------------------------------------------------------
    c1_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.60), Inches(1.75), Inches(3.91), Inches(2.55))
    c1_bg.fill.solid()
    c1_bg.fill.fore_color.rgb = C_LIGHT_BG
    c1_bg.line.fill.background()

    c1_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.60), Inches(1.75), Inches(3.91), Inches(0.05))
    c1_top.fill.solid()
    c1_top.fill.fore_color.rgb = C_BLUE
    c1_top.line.fill.background()

    tb1 = slide.shapes.add_textbox(Inches(0.70), Inches(1.87), Inches(3.71), Inches(2.34))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p_h1 = tf1.paragraphs[0]
    p_h1.text = "WHY IT'S THERE"
    p_h1.font.name = "Calibri"
    p_h1.font.size = Pt(12)
    p_h1.font.bold = True
    p_h1.font.color.rgb = C_BLUE

    bullets_why = [
        "Signavio BPMN models represent idealized SOPs, but actual transactional execution across ERP/CRM systems deviates significantly.",
        "Celonis uncovers friction, shadow rework (13.6% price changes), and maverick buying (7.0%), but findings remain trapped in analytics dashboards.",
        "Updating enterprise BPMN models to reflect operational reality is currently a manual, disconnected, and error-prone process."
    ]
    for b_text in bullets_why:
        p = tf1.add_paragraph()
        p.text = f"•  {b_text}"
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_DARK
        p.space_before = Pt(5)

    # -------------------------------------------------------------
    # 5. Top Middle Card: WHAT IT DOES (x=4.71, y=1.75, w=3.91, h=2.55)
    # -------------------------------------------------------------
    c2_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.71), Inches(1.75), Inches(3.91), Inches(2.55))
    c2_bg.fill.solid()
    c2_bg.fill.fore_color.rgb = C_LIGHT_BG
    c2_bg.line.fill.background()

    c2_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.71), Inches(1.75), Inches(3.91), Inches(0.05))
    c2_top.fill.solid()
    c2_top.fill.fore_color.rgb = C_BLUE
    c2_top.line.fill.background()

    tb2 = slide.shapes.add_textbox(Inches(4.81), Inches(1.87), Inches(3.71), Inches(2.40))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    p_h2 = tf2.paragraphs[0]
    p_h2.text = "WHAT IT DOES"
    p_h2.font.name = "Calibri"
    p_h2.font.size = Pt(12)
    p_h2.font.bold = True
    p_h2.font.color.rgb = C_BLUE

    bullets_what = [
        "Compares Signavio BPMN 2.0 models (or Signavio context) against Celonis event logs and PQL metrics.",
        "Quantifies happy-path fitness (68.2%), undocumented shadow activities, bypassed controls, and latency bottlenecks (11.7d wait).",
        "Generates a color-coded BPMN Conformance Heatmap (Green/Amber/Red) with performance annotations.",
        "Produces a clean, swimlane-structured To-Be BPMN for Signavio re-import, an executive HTML report, and an Excel review matrix."
    ]
    for b_text in bullets_what:
        p = tf2.add_paragraph()
        p.text = f"•  {b_text}"
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_DARK
        p.space_before = Pt(4)

    # -------------------------------------------------------------
    # 6. Top Right: Sample Output Showcase (x=8.89, y=1.35, w=4.02, h=2.95)
    # -------------------------------------------------------------
    sample_lbl = slide.shapes.add_textbox(Inches(8.89), Inches(0.95), Inches(3.8), Inches(0.35))
    tf_s = sample_lbl.text_frame
    tf_s.word_wrap = False
    p_s = tf_s.paragraphs[0]
    p_s.text = "Sample output & deliverables"
    p_s.font.name = "Calibri"
    p_s.font.size = Pt(13)
    p_s.font.bold = True
    p_s.font.color.rgb = C_DARK

    # Showcase Container
    showcase_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.89), Inches(1.35), Inches(3.85), Inches(2.95))
    showcase_bg.fill.solid()
    showcase_bg.fill.fore_color.rgb = C_LIGHT_BG
    showcase_bg.line.color.rgb = C_BORDER

    # 4 Output Mini Tiles inside Showcase
    out_cards = [
        ("1. Executive HTML Report", "Interactive KPI cards, deviation catalog, bottlenecks & roadmap", C_BLUE),
        ("2. BPMN Conformance Heatmap", "Color-coded BPMN XML (Green/Amber/Red) + metric text overlays", C_DARK),
        ("3. Clean Signavio To-Be Model", "Standardized BPMN with swimlanes (Purchasing, Logistics, AP)", C_BLUE),
        ("4. Review Matrix in Excel", "Tabular sign-off sheet with Decision dropdowns for workshops", C_PURPLE),
    ]

    for idx, (o_title, o_desc, tag_col) in enumerate(out_cards):
        oy = Inches(1.45 + (idx * 0.68))
        ob = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.00), oy, Inches(3.63), Inches(0.60))
        ob.fill.solid()
        ob.fill.fore_color.rgb = C_WHITE
        ob.line.color.rgb = C_BORDER

        # Left tag indicator
        otag = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.00), oy, Inches(0.06), Inches(0.60))
        otag.fill.solid()
        otag.fill.fore_color.rgb = tag_col
        otag.line.fill.background()

        otext = slide.shapes.add_textbox(Inches(9.15), oy + Inches(0.04), Inches(3.40), Inches(0.52))
        tf_o = otext.text_frame
        tf_o.word_wrap = True
        tf_o.margin_left = tf_o.margin_top = tf_o.margin_right = tf_o.margin_bottom = 0
        p_ot = tf_o.paragraphs[0]
        p_ot.text = o_title
        p_ot.font.name = "Calibri"
        p_ot.font.size = Pt(10)
        p_ot.font.bold = True
        p_ot.font.color.rgb = C_DARK

        p_od = tf_o.add_paragraph()
        p_od.text = o_desc
        p_od.font.name = "Calibri"
        p_od.font.size = Pt(8.5)
        p_od.font.color.rgb = C_GRAY

    # -------------------------------------------------------------
    # 7. Bottom Section: HOW IT WORKS (x=0.60, y=4.45)
    # -------------------------------------------------------------
    hiw_lbl = slide.shapes.add_textbox(Inches(0.60), Inches(4.45), Inches(12.13), Inches(0.35))
    tf_h = hiw_lbl.text_frame
    tf_h.word_wrap = False
    tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
    p_hiw = tf_h.paragraphs[0]
    p_hiw.text = "HOW IT WORKS"
    p_hiw.font.name = "Calibri"
    p_hiw.font.size = Pt(12)
    p_hiw.font.bold = True
    p_hiw.font.color.rgb = C_BLUE

    # 5 Step Pipeline
    steps_data = [
        ("1  Source", "A Signavio BPMN file (uploaded or from context) + Celonis event log / PQL analysis.", C_WHITE, C_DARK, C_BORDER, C_GRAY),
        ("2  celonis-signavio-comparator", "Analyzes conformance, detects shadow steps, and authors comparison-spec.json.", C_BLUE, C_WHITE, None, C_WHITE),
        ("3  Multi-Format Output", "Generates executive HTML report, color-coded Heatmap, and clean Signavio BPMN.", C_WHITE, C_DARK, C_BORDER, C_GRAY),
        ("4  Workshop Sign-Off", "Stakeholders review findings and record decisions (Approved/Rejected) in Excel matrix.", C_PURPLE, C_WHITE, None, C_WHITE),
        ("5  Signavio Production", "Re-imports the validated To-Be BPMN 2.0 XML directly into SAP Signavio Process Manager.", C_WHITE, C_DARK, C_BORDER, C_GRAY),
    ]

    step_w = Inches(1.69)
    step_h = Inches(1.65)
    step_y = Inches(4.85)
    arrow_w = Inches(0.22)
    arrow_h = Inches(0.26)
    arrow_y = Inches(5.54)

    for idx, (s_title, s_desc, bg_color, text_color, border_color, sub_color) in enumerate(steps_data):
        sx = Inches(0.60 + (idx * 2.02))

        # Step Box
        s_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, sx, step_y, step_w, step_h)
        s_box.fill.solid()
        s_box.fill.fore_color.rgb = bg_color
        if border_color:
            s_box.line.color.rgb = border_color
            s_box.line.width = Pt(1)
        else:
            s_box.line.fill.background()

        s_tf = s_box.text_frame
        s_tf.word_wrap = True
        s_tf.margin_left = s_tf.margin_right = Inches(0.10)
        s_tf.margin_top = Inches(0.12)

        p1 = s_tf.paragraphs[0]
        p1.text = s_title
        p1.font.name = "Calibri"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = text_color

        p2 = s_tf.add_paragraph()
        p2.text = s_desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(11)
        p2.font.color.rgb = sub_color
        p2.space_before = Pt(6)

        # Right Arrow after steps 1, 2, 3, 4
        if idx < 4:
            ax = sx + step_w + Inches(0.06)
            arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, ax, arrow_y, arrow_w, arrow_h)
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_ARROW
            arr.line.fill.background()

    # Right side feedback annotation under step 4/5
    fb_lbl = slide.shapes.add_textbox(Inches(10.65), Inches(4.47), Inches(2.35), Inches(0.35))
    tf_fb = fb_lbl.text_frame
    tf_fb.word_wrap = True
    p_fb = tf_fb.paragraphs[0]
    p_fb.text = "Feedback in Excel review matrix"
    p_fb.font.name = "Calibri"
    p_fb.font.size = Pt(11.5)
    p_fb.font.color.rgb = C_GRAY

    # -------------------------------------------------------------
    # 8. Footer (y = 6.95)
    # -------------------------------------------------------------
    foot_box = slide.shapes.add_textbox(Inches(0.60), Inches(6.95), Inches(12.13), Inches(0.30))
    tf_foot = foot_box.text_frame
    tf_foot.word_wrap = True
    tf_foot.margin_left = tf_foot.margin_top = tf_foot.margin_right = tf_foot.margin_bottom = 0
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = "Runs in Process Studio as Bring Your Own Skill. Closes the review & augmentation loop between Process Mining and Signavio Process Modeling."
    p_foot.font.name = "Calibri"
    p_foot.font.size = Pt(10.5)
    p_foot.font.color.rgb = C_GRAY

    prs.save(output_path)
    print(f"PASS: saved PowerPoint presentation to {output_path}")


if __name__ == "__main__":
    out_file = "/Users/mohamedi/Documents/Repos/Skillathon/process-studio-skills/celonis-signavio-comparator/BusinessUserJourneyWorkshopPack_oneSlide_Comparator.pptx"
    build_slide(out_file)
