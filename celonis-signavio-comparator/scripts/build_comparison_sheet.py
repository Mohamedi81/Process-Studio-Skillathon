#!/usr/bin/env python3
"""Build formatted Excel comparison matrix: Theory (Signavio) vs Reality (Celonis).

Usage:
  python3 build_comparison_sheet.py --input comparison-spec.json --output comparison-matrix.xlsx
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    openpyxl = None

# Local import
try:
    from validate_spec import validate_spec
except ImportError:
    from .validate_spec import validate_spec

DEFAULT_OUTPUT_NAME = "comparison-matrix.xlsx"


def create_excel_matrix(data: dict, output_path: str):
    """Generate multi-tab Excel workbook with formatted comparison sheets."""
    if openpyxl is None:
        raise RuntimeError("openpyxl package is required to build Excel review matrix")

    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    meta = data.get("meta", {})
    exec_sum = data.get("executive_summary", {})
    activities = data.get("activities", [])
    transitions = data.get("transitions", [])
    deviations = data.get("deviations", [])
    recon_plan = data.get("reconciliation_plan", [])

    # Styles
    navy_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    blue_header_fill = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
    subtle_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    green_fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
    amber_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    red_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")

    white_bold = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=16, bold=True, color="1E3A8A")
    subtitle_font = Font(name="Calibri", size=11, italic=True, color="64748B")
    section_font = Font(name="Calibri", size=13, bold=True, color="1E3A8A")
    bold_font = Font(name="Calibri", size=11, bold=True)
    normal_font = Font(name="Calibri", size=11)

    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )

    # ==========================================
    # Sheet 1: Executive Summary
    # ==========================================
    ws_exec = wb.create_sheet(title="Executive Summary")
    ws_exec.views.sheetView[0].showGridLines = True

    ws_exec["A1"] = f"{meta.get('process_name', 'Process Conformance')} — Theory vs Reality Comparison"
    ws_exec["A1"].font = title_font
    ws_exec["A2"] = f"Signavio Model: {meta.get('signavio_model_name', 'N/A')}  |  Celonis Model: {meta.get('celonis_data_model', 'N/A')}  |  Date: {meta.get('analysis_date', '2026-11-20')}"
    ws_exec["A2"].font = subtitle_font

    ws_exec["A4"] = "Core Metric"
    ws_exec["B4"] = "Value"
    ws_exec["C4"] = "Reference / Description"
    for col in ("A", "B", "C"):
        ws_exec[f"{col}4"].fill = navy_fill
        ws_exec[f"{col}4"].font = white_bold

    metrics = [
        ("Total Case Volume", f"{meta.get('case_count', 0):,}", "Number of distinct cases analyzed in Celonis"),
        ("Total Event Log Volume", f"{meta.get('event_count', 0):,}", "Total transactional timestamped events"),
        ("Conformance Rate (Happy Path)", f"{meta.get('conformance_rate_pct', 0.0):.1f}%", "Cases strictly following the Signavio happy path"),
        ("Rework & Friction Share", f"{exec_sum.get('rework_rate_pct', 0.0):.1f}%", "Cases encountering rework, repetitions, or exception loops"),
        ("Maverick Buying Share", f"{exec_sum.get('maverick_rate_pct', 0.0):.1f}%", "Invoices recorded before PO item creation"),
        ("Actual Average Throughput", f"{meta.get('avg_throughput_days', 0.0):.1f} days", "Empirical end-to-end process lead time"),
        ("Signavio Modeled SLA", f"{meta.get('modeled_sla_days', 0.0):.1f} days", "Prescribed target throughput SLA"),
        ("Average SLA Variance / Delay", f"+{meta.get('avg_throughput_days', 0.0) - meta.get('modeled_sla_days', 0.0):.1f} days", "Unmodeled waiting time and execution latency")
    ]

    for idx, (m_name, m_val, m_desc) in enumerate(metrics, start=5):
        ws_exec[f"A{idx}"] = m_name
        ws_exec[f"B{idx}"] = m_val
        ws_exec[f"C{idx}"] = m_desc
        ws_exec[f"A{idx}"].font = bold_font
        ws_exec[f"B{idx}"].font = bold_font
        ws_exec[f"C{idx}"].font = normal_font
        for col in ("A", "B", "C"):
            ws_exec[f"{col}{idx}"].border = thin_border

    ws_exec["A15"] = "Executive Headline & Findings"
    ws_exec["A15"].font = section_font
    ws_exec["A16"] = exec_sum.get("headline", "")
    ws_exec["A16"].font = bold_font

    ws_exec["A18"] = "Key Takeaways:"
    ws_exec["A18"].font = bold_font
    for t_idx, takeaway in enumerate(exec_sum.get("key_takeaways", []), start=19):
        ws_exec[f"A{t_idx}"] = f"• {takeaway}"
        ws_exec[f"A{t_idx}"].font = normal_font

    # ==========================================
    # Sheet 2: Activity Comparison
    # ==========================================
    ws_act = wb.create_sheet(title="Activity Comparison")
    ws_act.views.sheetView[0].showGridLines = True

    act_headers = [
        "Activity ID", "Activity Name", "Original (DE)", "Conformance Status",
        "Signavio (Theory)", "Signavio Lane", "Celonis (Reality)",
        "Celonis Events", "Case Share %", "Avg Duration (d)", "Notes & Impact"
    ]
    for c_idx, h in enumerate(act_headers, start=1):
        cell = ws_act.cell(row=1, column=c_idx, value=h)
        cell.fill = blue_header_fill
        cell.font = white_bold
        cell.alignment = Alignment(horizontal="center" if "Status" in h or "Theory" in h or "Reality" in h else "left")

    for r_idx, a in enumerate(activities, start=2):
        status = a.get("status", "unknown")
        sig_pres = "Yes" if a.get("signavio_presence") else "No"
        cel_pres = "Yes" if a.get("celonis_presence") else "No"
        events = a.get("celonis_events", 0)
        pct = a.get("celonis_case_pct", 0.0)
        dur = a.get("avg_duration_days", 0.0)

        ws_act.cell(row=r_idx, column=1, value=a.get("id", f"ACT-{r_idx-1}"))
        ws_act.cell(row=r_idx, column=2, value=a.get("name", ""))
        ws_act.cell(row=r_idx, column=3, value=a.get("original_name_de", ""))
        
        status_cell = ws_act.cell(row=r_idx, column=4, value=status.replace('_', ' ').title())
        if status == "matched":
            status_cell.fill = green_fill
        elif "undocumented" in status or "shadow" in status:
            status_cell.fill = red_fill
        elif "skipped" in status:
            status_cell.fill = amber_fill

        ws_act.cell(row=r_idx, column=5, value=sig_pres)
        ws_act.cell(row=r_idx, column=6, value=a.get("signavio_lane") or "—")
        ws_act.cell(row=r_idx, column=7, value=cel_pres)
        ws_act.cell(row=r_idx, column=8, value=events if cel_pres == "Yes" else 0)
        ws_act.cell(row=r_idx, column=9, value=pct / 100.0 if cel_pres == "Yes" else 0.0)
        ws_act.cell(row=r_idx, column=10, value=dur if dur else 0.0)
        ws_act.cell(row=r_idx, column=11, value=a.get("conformance_notes", ""))

        # Number formatting
        ws_act.cell(row=r_idx, column=8).number_format = '#,##0'
        ws_act.cell(row=r_idx, column=9).number_format = '0.0%'
        ws_act.cell(row=r_idx, column=10).number_format = '0.0'

        for c_idx in range(1, 12):
            ws_act.cell(row=r_idx, column=c_idx).border = thin_border
            ws_act.cell(row=r_idx, column=c_idx).font = normal_font

    # ==========================================
    # Sheet 3: Transition & Latency
    # ==========================================
    ws_trans = wb.create_sheet(title="Transition & Latency")
    ws_trans.views.sheetView[0].showGridLines = True

    trans_headers = [
        "Source Activity", "Target Activity", "Flow Category", "Volume",
        "Actual Wait (d)", "Signavio SLA (d)", "SLA Delta (d)", "Severity", "Notes"
    ]
    for c_idx, h in enumerate(trans_headers, start=1):
        cell = ws_trans.cell(row=1, column=c_idx, value=h)
        cell.fill = blue_header_fill
        cell.font = white_bold

    for r_idx, t in enumerate(transitions, start=2):
        ws_trans.cell(row=r_idx, column=1, value=t.get("source", ""))
        ws_trans.cell(row=r_idx, column=2, value=t.get("target", ""))
        ws_trans.cell(row=r_idx, column=3, value=t.get("status", "").replace('_', ' ').title())
        ws_trans.cell(row=r_idx, column=4, value=t.get("volume", 0))
        ws_trans.cell(row=r_idx, column=5, value=t.get("avg_wait_days", 0.0))
        ws_trans.cell(row=r_idx, column=6, value=t.get("modeled_wait_days", 0.0) if t.get("modeled_wait_days") is not None else "—")
        ws_trans.cell(row=r_idx, column=7, value=t.get("delta_days", 0.0) if t.get("delta_days") is not None else "—")
        
        sev_cell = ws_trans.cell(row=r_idx, column=8, value=t.get("severity", "medium").upper())
        if t.get("severity") == "critical":
            sev_cell.fill = red_fill
        elif t.get("severity") == "high":
            sev_cell.fill = amber_fill

        ws_trans.cell(row=r_idx, column=9, value=t.get("notes", ""))

        ws_trans.cell(row=r_idx, column=4).number_format = '#,##0'
        if isinstance(ws_trans.cell(row=r_idx, column=5).value, (int, float)):
            ws_trans.cell(row=r_idx, column=5).number_format = '0.0'
        if isinstance(ws_trans.cell(row=r_idx, column=6).value, (int, float)):
            ws_trans.cell(row=r_idx, column=6).number_format = '0.0'
        if isinstance(ws_trans.cell(row=r_idx, column=7).value, (int, float)):
            ws_trans.cell(row=r_idx, column=7).number_format = '+0.0;-0.0;0.0'

        for c_idx in range(1, 10):
            ws_trans.cell(row=r_idx, column=c_idx).border = thin_border
            ws_trans.cell(row=r_idx, column=c_idx).font = normal_font

    # ==========================================
    # Sheet 4: Deviation Register
    # ==========================================
    ws_dev = wb.create_sheet(title="Deviation Register")
    ws_dev.views.sheetView[0].showGridLines = True

    dev_headers = [
        "ID", "Title", "Deviation Type", "Description", "Affected Volume",
        "Case Share %", "Delay Penalty (d)", "Cost Impact", "Severity",
        "Strategy", "Recommended Action"
    ]
    for c_idx, h in enumerate(dev_headers, start=1):
        cell = ws_dev.cell(row=1, column=c_idx, value=h)
        cell.fill = blue_header_fill
        cell.font = white_bold

    for r_idx, d in enumerate(deviations, start=2):
        ws_dev.cell(row=r_idx, column=1, value=d.get("id", f"DEV-{r_idx-1}"))
        ws_dev.cell(row=r_idx, column=2, value=d.get("title", ""))
        ws_dev.cell(row=r_idx, column=3, value=d.get("type", "").replace('_', ' ').title())
        ws_dev.cell(row=r_idx, column=4, value=d.get("description", ""))
        ws_dev.cell(row=r_idx, column=5, value=d.get("affected_volume", 0))
        ws_dev.cell(row=r_idx, column=6, value=d.get("pct_of_total", 0.0) / 100.0)
        ws_dev.cell(row=r_idx, column=7, value=d.get("time_penalty_days", 0.0))
        ws_dev.cell(row=r_idx, column=8, value=d.get("cost_impact_est", "N/A"))
        
        sev_cell = ws_dev.cell(row=r_idx, column=9, value=d.get("severity", "medium").upper())
        if d.get("severity") in ("critical", "high"):
            sev_cell.fill = red_fill
        elif d.get("severity") == "medium":
            sev_cell.fill = amber_fill

        ws_dev.cell(row=r_idx, column=10, value=d.get("recommendation_type", "").replace('_', ' ').title())
        ws_dev.cell(row=r_idx, column=11, value=d.get("recommendation", ""))

        ws_dev.cell(row=r_idx, column=5).number_format = '#,##0'
        ws_dev.cell(row=r_idx, column=6).number_format = '0.0%'
        ws_dev.cell(row=r_idx, column=7).number_format = '0.0'

        for c_idx in range(1, 12):
            ws_dev.cell(row=r_idx, column=c_idx).border = thin_border
            ws_dev.cell(row=r_idx, column=c_idx).font = normal_font

    # ==========================================
    # Sheet 5: Reconciliation Plan (with Decision Dropdown)
    # ==========================================
    ws_plan = wb.create_sheet(title="Reconciliation Plan")
    ws_plan.views.sheetView[0].showGridLines = True

    plan_headers = [
        "Action ID", "Target Type", "Element Affected", "Action Description",
        "Owner", "Priority", "Stakeholder Decision", "Review Comments"
    ]
    for c_idx, h in enumerate(plan_headers, start=1):
        cell = ws_plan.cell(row=1, column=c_idx, value=h)
        cell.fill = blue_header_fill
        cell.font = white_bold

    # Data validation dropdown for Decision column (Column G)
    dv = DataValidation(type="list", formula1='"Approved as-is,Approved with changes,Rejected,Under Review"', allow_blank=True)
    ws_plan.add_data_validation(dv)

    for r_idx, r in enumerate(recon_plan, start=2):
        ws_plan.cell(row=r_idx, column=1, value=r.get("action_id", f"REC-{r_idx-1}"))
        ws_plan.cell(row=r_idx, column=2, value=r.get("target_type", "").replace('_', ' ').title())
        ws_plan.cell(row=r_idx, column=3, value=r.get("element_affected", ""))
        ws_plan.cell(row=r_idx, column=4, value=r.get("description", ""))
        ws_plan.cell(row=r_idx, column=5, value=r.get("owner", ""))
        
        prio_cell = ws_plan.cell(row=r_idx, column=6, value=r.get("priority", "Medium"))
        if r.get("priority", "").lower() in ("critical", "high"):
            prio_cell.fill = red_fill
        elif r.get("priority", "").lower() == "medium":
            prio_cell.fill = amber_fill

        dec_cell = ws_plan.cell(row=r_idx, column=7, value="Under Review")
        dv.add(dec_cell)
        ws_plan.cell(row=r_idx, column=8, value="")

        for c_idx in range(1, 9):
            ws_plan.cell(row=r_idx, column=c_idx).border = thin_border
            ws_plan.cell(row=r_idx, column=c_idx).font = normal_font

    # Adjust column widths automatically across all sheets
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if cell.number_format == '0.0%':
                    val_str += ' %'
                max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 48)

    wb.save(output_path)


def main():
    parser = argparse.ArgumentParser(description="Generate formatted Excel comparison matrix.")
    parser.add_argument("--input", required=True, help="Path to comparison-spec.json")
    parser.add_argument("--output", required=True, help="Path to output Excel review matrix (.xlsx)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"FAIL: input file '{args.input}' does not exist", file=sys.stderr)
        return 1

    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: invalid JSON in input file: {exc}", file=sys.stderr)
        return 1

    errors = validate_spec(data)
    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        return 1

    try:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        create_excel_matrix(data, str(out_path))
        print(f"PASS: wrote comparison matrix to {args.output}")
        return 0
    except Exception as exc:
        print(f"FAIL: could not generate Excel workbook: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
