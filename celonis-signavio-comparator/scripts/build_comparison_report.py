#!/usr/bin/env python3
"""Build self-contained HTML comparison report: Theory (Signavio) vs Reality (Celonis).

Usage:
  python3 build_comparison_report.py --input comparison-spec.json --output celonis-signavio-comparison-report.html
"""
import argparse
import html
import json
import sys
from pathlib import Path

# Local import
try:
    from validate_spec import validate_spec
except ImportError:
    from .validate_spec import validate_spec

DEFAULT_OUTPUT_NAME = "celonis-signavio-comparison-report.html"


def generate_html_report(data: dict) -> str:
    """Generate self-contained HTML report from validated comparison spec."""
    meta = data.get("meta", {})
    exec_sum = data.get("executive_summary", {})
    activities = data.get("activities", [])
    transitions = data.get("transitions", [])
    deviations = data.get("deviations", [])
    bottlenecks = data.get("bottlenecks", [])
    recon_plan = data.get("reconciliation_plan", [])

    process_name = html.escape(str(meta.get("process_name", "Process Conformance Analysis")))
    signavio_model = html.escape(str(meta.get("signavio_model_name", "Signavio BPMN Model")))
    celonis_model = html.escape(str(meta.get("celonis_data_model", "Celonis Event Log")))
    analysis_date = html.escape(str(meta.get("analysis_date", "2026-11-20")))
    timeframe = html.escape(str(meta.get("timeframe", "Recent Period")))

    cases_count = meta.get("case_count", 0)
    events_count = meta.get("event_count", 0)
    conformance_pct = meta.get("conformance_rate_pct", 0.0)
    avg_tpt = meta.get("avg_throughput_days", 0.0)
    sla_days = meta.get("modeled_sla_days", 0.0)
    rework_pct = exec_sum.get("rework_rate_pct", 0.0)
    maverick_pct = exec_sum.get("maverick_rate_pct", 0.0)

    # Activity count stats
    total_acts = len(activities)
    matched_acts = sum(1 for a in activities if a.get("status") == "matched")
    shadow_acts = sum(1 for a in activities if a.get("status") == "undocumented_reality")
    skipped_acts = sum(1 for a in activities if a.get("status") == "skipped_in_reality")

    # Activities table rows
    act_rows = []
    for a in activities:
        name = html.escape(str(a.get("name", "")))
        orig_de = html.escape(str(a.get("original_name_de", "")))
        status = a.get("status", "unknown")
        sig_pres = a.get("signavio_presence", False)
        cel_pres = a.get("celonis_presence", False)
        cel_events = a.get("celonis_events", 0)
        cel_pct = a.get("celonis_case_pct", 0.0)
        avg_dur = a.get("avg_duration_days", 0.0)
        notes = html.escape(str(a.get("conformance_notes", "")))

        if status == "matched":
            badge = '<span class="badge badge-green">Matched (Theory & Reality)</span>'
        elif status == "undocumented_reality":
            badge = '<span class="badge badge-red">Shadow Activity (Undocumented)</span>'
        elif status == "skipped_in_reality":
            badge = '<span class="badge badge-grey">Bypassed / Skipped</span>'
        else:
            badge = f'<span class="badge badge-amber">{html.escape(status)}</span>'

        sig_icon = '<span class="icon-check">✓ Yes</span>' if sig_pres else '<span class="icon-cross">✗ No</span>'
        cel_icon = '<span class="icon-check">✓ Yes</span>' if cel_pres else '<span class="icon-cross">✗ No</span>'

        events_str = f"{cel_events:,}" if cel_pres and cel_events else "—"
        pct_str = f"{cel_pct:.1f}%" if cel_pres and cel_pct else "—"
        dur_str = f"{avg_dur:.1f} d" if avg_dur else "—"

        de_subtitle = f'<div class="text-xs text-muted">DE: {orig_de}</div>' if orig_de else ""

        act_rows.append(f"""
        <tr>
          <td><strong>{name}</strong>{de_subtitle}</td>
          <td>{badge}</td>
          <td class="text-center">{sig_icon}</td>
          <td class="text-center">{cel_icon}</td>
          <td class="text-right">{events_str}</td>
          <td class="text-right font-semibold">{pct_str}</td>
          <td class="text-right">{dur_str}</td>
          <td class="text-sm">{notes}</td>
        </tr>
        """)

    # Transitions table rows
    trans_rows = []
    for t in transitions:
        src = html.escape(str(t.get("source", "")))
        tgt = html.escape(str(t.get("target", "")))
        status = t.get("status", "matched")
        vol = t.get("volume", 0)
        wait_days = t.get("avg_wait_days", 0.0)
        mod_wait = t.get("modeled_wait_days")
        delta = t.get("delta_days")
        sev = t.get("severity", "medium")
        t_notes = html.escape(str(t.get("notes", "")))

        sev_class = "badge-red" if sev == "critical" else ("badge-amber" if sev == "high" else "badge-blue")
        mod_wait_str = f"{mod_wait:.1f} d" if mod_wait is not None else "—"
        delta_str = f"+{delta:.1f} d" if (delta is not None and delta > 0) else ("—" if delta is None else f"{delta:.1f} d")

        trans_rows.append(f"""
        <tr>
          <td><strong>{src}</strong> &rarr; <strong>{tgt}</strong></td>
          <td><span class="badge {sev_class}">{html.escape(status.replace('_', ' ').title())}</span></td>
          <td class="text-right">{vol:,}</td>
          <td class="text-right font-semibold">{wait_days:.1f} d</td>
          <td class="text-right text-muted">{mod_wait_str}</td>
          <td class="text-right text-danger font-semibold">{delta_str}</td>
          <td class="text-sm">{t_notes}</td>
        </tr>
        """)

    # Deviations cards
    dev_cards = []
    for d in deviations:
        dev_id = html.escape(str(d.get("id", "")))
        title = html.escape(str(d.get("title", "")))
        dtype = html.escape(str(d.get("type", "").replace('_', ' ').title()))
        desc = html.escape(str(d.get("description", "")))
        vol = d.get("affected_volume", 0)
        pct = d.get("pct_of_total", 0.0)
        penalty = d.get("time_penalty_days", 0.0)
        cost = html.escape(str(d.get("cost_impact_est", "N/A")))
        sev = d.get("severity", "medium")
        rec_type = html.escape(str(d.get("recommendation_type", "").replace('_', ' ').title()))
        rec = html.escape(str(d.get("recommendation", "")))

        sev_badge = "badge-red" if sev in ("critical", "high") else ("badge-amber" if sev == "medium" else "badge-blue")
        rec_badge = "badge-purple" if "bpmn" in rec_type.lower() or "model" in rec_type.lower() else "badge-teal"

        dev_cards.append(f"""
        <div class="card deviation-card">
          <div class="card-header">
            <div>
              <span class="badge badge-outline">{dev_id}</span>
              <span class="badge {sev_badge}">{sev.upper()}</span>
              <h3 class="card-title mt-1">{title}</h3>
              <div class="text-xs text-muted">{dtype}</div>
            </div>
            <div class="text-right">
              <div class="text-lg font-bold text-danger">{vol:,} cases ({pct:.1f}%)</div>
              <div class="text-xs text-muted">Delay Penalty: +{penalty:.1f} days</div>
            </div>
          </div>
          <div class="card-body">
            <p class="text-sm mb-3">{desc}</p>
            <div class="grid grid-2 gap-2 mb-3 bg-surface p-3 rounded">
              <div><strong class="text-xs text-muted uppercase">Cost / Efficiency Impact:</strong> <span class="text-sm font-semibold">{cost}</span></div>
              <div><strong class="text-xs text-muted uppercase">Reconciliation Strategy:</strong> <span class="badge {rec_badge}">{rec_type}</span></div>
            </div>
            <div class="recommendation-box">
              <strong class="text-xs text-brand uppercase">Recommended Fix:</strong>
              <p class="text-sm mt-1">{rec}</p>
            </div>
          </div>
        </div>
        """)

    # Key takeaways bullets
    takeaways_html = "".join([f"<li>{html.escape(t)}</li>" for t in exec_sum.get("key_takeaways", [])])

    # Reconciliation table
    recon_rows = []
    for r in recon_plan:
        act_id = html.escape(str(r.get("action_id", "")))
        ttype = html.escape(str(r.get("target_type", "").replace('_', ' ').title()))
        elem = html.escape(str(r.get("element_affected", "")))
        rdesc = html.escape(str(r.get("description", "")))
        owner = html.escape(str(r.get("owner", "")))
        prio = html.escape(str(r.get("priority", "Medium")))

        prio_badge = "badge-red" if prio.lower() in ("critical", "high") else "badge-amber"
        target_badge = "badge-purple" if "bpmn" in ttype.lower() or "augment" in ttype.lower() else "badge-teal"

        recon_rows.append(f"""
        <tr>
          <td><span class="badge badge-outline">{act_id}</span></td>
          <td><span class="badge {target_badge}">{ttype}</span></td>
          <td><strong>{elem}</strong></td>
          <td class="text-sm">{rdesc}</td>
          <td>{owner}</td>
          <td><span class="badge {prio_badge}">{prio}</span></td>
        </tr>
        """)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{process_name} — Theory (Signavio) vs Reality (Celonis) Comparison</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --surface: #ffffff;
      --surface-subtle: #f1f5f9;
      --border: #e2e8f0;
      --text: #0f172a;
      --text-muted: #64748b;
      --brand: #2563eb;
      --brand-dark: #1e40af;
      --green: #10b981;
      --green-bg: #d1fae5;
      --amber: #f59e0b;
      --amber-bg: #fef3c7;
      --red: #ef4444;
      --red-bg: #fee2e2;
      --purple: #8b5cf6;
      --purple-bg: #ede9fe;
      --teal: #0d9488;
      --teal-bg: #ccfbf1;
      --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
      --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      font-size: 14px;
    }}

    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px;
    }}

    /* Header */
    .report-header {{
      background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
      color: #ffffff;
      border-radius: 12px;
      padding: 32px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-md);
    }}
    .header-kicker {{
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.1em;
      color: #93c5fd;
      font-weight: 700;
      margin-bottom: 8px;
    }}
    .report-title {{
      font-size: 26px;
      font-weight: 800;
      line-height: 1.2;
      margin-bottom: 12px;
    }}
    .header-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      font-size: 13px;
      color: #bfdbfe;
    }}
    .header-meta-item strong {{ color: #ffffff; }}

    /* KPI Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .kpi-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px;
      box-shadow: var(--shadow);
    }}
    .kpi-label {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }}
    .kpi-value {{
      font-size: 28px;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 6px;
    }}
    .kpi-subtext {{
      font-size: 12px;
      color: var(--text-muted);
    }}
    .val-green {{ color: var(--green); }}
    .val-amber {{ color: var(--amber); }}
    .val-red {{ color: var(--red); }}
    .val-brand {{ color: var(--brand); }}

    /* Cards */
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      box-shadow: var(--shadow);
      margin-bottom: 24px;
      overflow: hidden;
    }}
    .card-header {{
      padding: 18px 24px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #fafafa;
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: var(--text);
    }}
    .card-body {{
      padding: 24px;
    }}

    /* Badges */
    .badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      line-height: 1.2;
    }}
    .badge-green {{ background: var(--green-bg); color: #065f46; }}
    .badge-amber {{ background: var(--amber-bg); color: #92400e; }}
    .badge-red {{ background: var(--red-bg); color: #991b1b; }}
    .badge-purple {{ background: var(--purple-bg); color: #5b21b6; }}
    .badge-teal {{ background: var(--teal-bg); color: #115e59; }}
    .badge-grey {{ background: #f1f5f9; color: #475569; }}
    .badge-outline {{ border: 1px solid var(--border); background: #ffffff; color: var(--text); }}

    /* Tables */
    .table-container {{
      overflow-x: auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }}
    th {{
      background: var(--surface-subtle);
      padding: 10px 14px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border);
    }}
    td {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover td {{ background: #f8fafc; }}

    /* Utilities */
    .text-center {{ text-align: center; }}
    .text-right {{ text-align: right; }}
    .font-semibold {{ font-weight: 600; }}
    .font-bold {{ font-weight: 700; }}
    .text-muted {{ color: var(--text-muted); }}
    .text-danger {{ color: var(--red); }}
    .text-brand {{ color: var(--brand); }}
    .text-xs {{ font-size: 11px; }}
    .text-sm {{ font-size: 13px; }}
    .text-lg {{ font-size: 16px; }}
    .mt-1 {{ margin-top: 4px; }}
    .mb-3 {{ margin-bottom: 12px; }}
    .p-3 {{ padding: 12px; }}
    .rounded {{ border-radius: 6px; }}
    .bg-surface {{ background: var(--surface-subtle); }}
    .uppercase {{ text-transform: uppercase; }}
    .grid {{ display: grid; }}
    .grid-2 {{ grid-template-columns: repeat(2, 1fr); }}
    .gap-2 {{ gap: 8px; }}

    .icon-check {{ color: var(--green); font-weight: bold; }}
    .icon-cross {{ color: var(--red); font-weight: bold; }}

    .executive-callout {{
      background: #eff6ff;
      border-left: 4px solid var(--brand);
      padding: 18px 20px;
      border-radius: 0 8px 8px 0;
      margin-bottom: 20px;
    }}
    .executive-callout h4 {{
      color: var(--brand-dark);
      font-size: 15px;
      margin-bottom: 8px;
    }}
    .executive-callout ul {{
      padding-left: 20px;
      color: #1e3a8a;
      font-size: 13px;
    }}
    .executive-callout li {{
      margin-bottom: 4px;
    }}

    .deviation-card {{
      margin-bottom: 16px;
    }}
    .recommendation-box {{
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      padding: 12px;
      border-radius: 6px;
    }}

    /* Visual Process Flow Diagram */
    .flow-diagram-container {{
      background: #ffffff;
      padding: 24px;
      border: 1px solid var(--border);
      border-radius: 8px;
      margin-bottom: 20px;
    }}

    .footer {{
      text-align: center;
      padding: 24px;
      font-size: 12px;
      color: var(--text-muted);
      border-top: 1px solid var(--border);
      margin-top: 40px;
    }}
  </style>
</head>
<body>

<div class="container">

  <!-- Header -->
  <header class="report-header">
    <div class="header-kicker">Process Conformance & Reconciliation Report</div>
    <h1 class="report-title">{process_name}: Theory vs. Reality Analysis</h1>
    <div class="header-meta">
      <div class="header-meta-item">Theory Model: <strong>{signavio_model}</strong></div>
      <div class="header-meta-item">Reality Source: <strong>{celonis_model}</strong></div>
      <div class="header-meta-item">Timeframe: <strong>{timeframe}</strong></div>
      <div class="header-meta-item">Date: <strong>{analysis_date}</strong></div>
    </div>
  </header>

  <!-- Executive Summary Callout -->
  <div class="executive-callout">
    <h4>Executive Finding</h4>
    <p class="font-semibold mb-3">{html.escape(str(exec_sum.get("headline", "")))}</p>
    <ul>
      {takeaways_html}
    </ul>
  </div>

  <!-- KPI Scorecard -->
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Conformance Rate (Happy Path)</div>
      <div class="kpi-value val-brand">{conformance_pct:.1f}%</div>
      <div class="kpi-subtext">{cases_count:,} total cases analyzed</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Rework & Exception Share</div>
      <div class="kpi-value val-red">{rework_pct:.1f}%</div>
      <div class="kpi-subtext">{(int(cases_count * rework_pct / 100)):,} cases with friction/rework</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Actual vs SLA Throughput</div>
      <div class="kpi-value val-amber">{avg_tpt:.1f} <span style="font-size: 16px; font-weight: normal;">days</span></div>
      <div class="kpi-subtext">Modeled SLA: {sla_days:.1f} days (+{avg_tpt - sla_days:.1f} d delta)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Maverick Buying Rate</div>
      <div class="kpi-value val-red">{maverick_pct:.1f}%</div>
      <div class="kpi-subtext">Invoices received prior to PO dispatch</div>
    </div>
  </div>

  <!-- Visual Process Comparison Flow Diagram -->
  <div class="card">
    <div class="card-header">
      <h2 class="card-title">Process Architecture: Prescribed Signavio Path vs Reality Findings</h2>
      <div class="text-xs text-muted">BPMN Happy Path with Empirical Reality Overlays</div>
    </div>
    <div class="card-body">
      <div class="flow-diagram-container">
        <svg viewBox="0 0 1060 280" style="width: 100%; height: auto; font-family: sans-serif;">
          <!-- Swimlane / Stage Backgrounds -->
          <rect x="10" y="20" width="1040" height="240" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-dasharray="4" />
          <text x="25" y="42" font-size="12" font-weight="bold" fill="#64748b">END-TO-END PROCESS CONFORMANCE MAP</text>

          <!-- Standard Flow Boxes (Signavio Happy Path) -->
          <!-- Step 1: Create PR -->
          <rect x="40" y="70" width="120" height="50" rx="6" fill="#d1fae5" stroke="#10b981" stroke-width="2" />
          <text x="100" y="95" font-size="11" font-weight="bold" fill="#065f46" text-anchor="middle">Create PR</text>
          <text x="100" y="110" font-size="9" fill="#047857" text-anchor="middle">78.9% cases</text>

          <!-- Arrow 1 -> 2 -->
          <path d="M 160 95 L 200 95" fill="none" stroke="#10b981" stroke-width="2" marker-end="url(#arrow-green)" />

          <!-- Step 2: Create PO -->
          <rect x="200" y="70" width="120" height="50" rx="6" fill="#d1fae5" stroke="#10b981" stroke-width="2" />
          <text x="260" y="95" font-size="11" font-weight="bold" fill="#065f46" text-anchor="middle">Create PO</text>
          <text x="260" y="110" font-size="9" fill="#047857" text-anchor="middle">100% (1.11M)</text>

          <!-- Arrow 2 -> 3 -->
          <path d="M 320 95 L 360 95" fill="none" stroke="#10b981" stroke-width="2" />

          <!-- Step 3: Send PO -->
          <rect x="360" y="70" width="120" height="50" rx="6" fill="#d1fae5" stroke="#10b981" stroke-width="2" />
          <text x="420" y="95" font-size="11" font-weight="bold" fill="#065f46" text-anchor="middle">Send PO</text>
          <text x="420" y="110" font-size="9" fill="#047857" text-anchor="middle">97.6% (1.09M)</text>

          <!-- Arrow 3 -> 4 -->
          <path d="M 480 95 L 530 95" fill="none" stroke="#10b981" stroke-width="2" />
          <text x="505" y="88" font-size="9" fill="#64748b" text-anchor="middle">8.1 days</text>

          <!-- Step 4: Goods Receipt -->
          <rect x="530" y="70" width="130" height="50" rx="6" fill="#d1fae5" stroke="#10b981" stroke-width="2" />
          <text x="595" y="95" font-size="11" font-weight="bold" fill="#065f46" text-anchor="middle">Goods Receipt</text>
          <text x="595" y="110" font-size="9" fill="#047857" text-anchor="middle">92.6% (1.03M)</text>

          <!-- Arrow 4 -> 5 -->
          <path d="M 660 95 L 710 95" fill="none" stroke="#10b981" stroke-width="2" />
          <text x="685" y="88" font-size="9" fill="#64748b" text-anchor="middle">5.8 days</text>

          <!-- Step 5: Record Invoice -->
          <rect x="710" y="70" width="130" height="50" rx="6" fill="#d1fae5" stroke="#10b981" stroke-width="2" />
          <text x="775" y="95" font-size="11" font-weight="bold" fill="#065f46" text-anchor="middle">Record Invoice</text>
          <text x="775" y="110" font-size="9" fill="#047857" text-anchor="middle">91.8% (1.02M)</text>

          <!-- Arrow 5 -> 6 (BOTTLENECK) -->
          <path d="M 840 95 L 890 95" fill="none" stroke="#f59e0b" stroke-width="3" />
          <text x="865" y="85" font-size="10" font-weight="bold" fill="#b45309" text-anchor="middle">11.7 days!</text>

          <!-- Step 6: Pay Invoice -->
          <rect x="890" y="70" width="130" height="50" rx="6" fill="#d1fae5" stroke="#10b981" stroke-width="2" />
          <text x="955" y="95" font-size="11" font-weight="bold" fill="#065f46" text-anchor="middle">Pay Invoice</text>
          <text x="955" y="110" font-size="9" fill="#047857" text-anchor="middle">90.8% (1.01M)</text>

          <!-- SHADOW PATH 1: Price Change Loop (Discovered in Celonis) -->
          <path d="M 420 120 L 420 170 L 470 170" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="3" />
          <rect x="470" y="145" width="130" height="50" rx="6" fill="#fee2e2" stroke="#ef4444" stroke-width="2" />
          <text x="535" y="168" font-size="11" font-weight="bold" fill="#991b1b" text-anchor="middle">Price Change</text>
          <text x="535" y="183" font-size="9" fill="#dc2626" text-anchor="middle">13.6% (+8.8 days delay)</text>
          <path d="M 600 170 L 630 170 L 630 120" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="3" />

          <!-- SHADOW PATH 2: Payment Block & Release Loop -->
          <path d="M 775 120 L 775 220 L 810 220" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="3" />
          <rect x="810" y="195" width="140" height="50" rx="6" fill="#fee2e2" stroke="#ef4444" stroke-width="2" />
          <text x="880" y="218" font-size="11" font-weight="bold" fill="#991b1b" text-anchor="middle">Payment Block/Release</text>
          <text x="880" y="233" font-size="9" fill="#dc2626" text-anchor="middle">2.3% (+11.4 days delay)</text>
          <path d="M 950 220 L 980 220 L 980 120" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="3" />

          <!-- SHADOW PATH 3: Maverick Buying (Invoice before PO) -->
          <path d="M 730 70 L 730 40 L 260 40 L 260 70" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="4" />
          <text x="495" y="34" font-size="10" font-weight="bold" fill="#dc2626" text-anchor="middle">Maverick Invoicing (7.0% of cases bypass PO initiation)</text>
        </svg>
      </div>
      <div class="grid grid-2 gap-2 text-xs text-muted">
        <div><span class="badge badge-green">Green Solid</span> = Signavio Prescribed Happy Path</div>
        <div><span class="badge badge-red">Red Dashed</span> = Celonis-Discovered Reality Deviations & Shadow Loops</div>
      </div>
    </div>
  </div>

  <!-- Activity Conformance Matrix -->
  <div class="card">
    <div class="card-header">
      <h2 class="card-title">Activity Conformance Matrix ({total_acts} Total Activities)</h2>
      <div>
        <span class="badge badge-green">{matched_acts} Matched</span>
        <span class="badge badge-red">{shadow_acts} Undocumented Shadow</span>
        <span class="badge badge-grey">{skipped_acts} Skipped</span>
      </div>
    </div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Activity Name</th>
            <th>Conformance Status</th>
            <th class="text-center">Signavio (Theory)</th>
            <th class="text-center">Celonis (Reality)</th>
            <th class="text-right">Event Count</th>
            <th class="text-right">Case Share %</th>
            <th class="text-right">Avg Wait / Loop</th>
            <th>Conformance Notes & Impact</th>
          </tr>
        </thead>
        <tbody>
          {"".join(act_rows)}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Transition & Bottleneck Latency -->
  <div class="card">
    <div class="card-header">
      <h2 class="card-title">Transition & Bottleneck Latency Analysis</h2>
      <div class="text-xs text-muted">Modeled Waiting Time SLA vs Actual Execution Delay</div>
    </div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Transition (Source &rarr; Target)</th>
            <th>Flow Category</th>
            <th class="text-right">Volume</th>
            <th class="text-right">Actual Wait</th>
            <th class="text-right">Signavio SLA</th>
            <th class="text-right">SLA Delta</th>
            <th>Operational Impact & Root Cause</th>
          </tr>
        </thead>
        <tbody>
          {"".join(trans_rows)}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Identified Deviations & Friction Points -->
  <div class="card">
    <div class="card-header">
      <h2 class="card-title">Detailed Deviation Register & Root Causes ({len(deviations)} Findings)</h2>
    </div>
    <div class="card-body">
      {"".join(dev_cards)}
    </div>
  </div>

  <!-- Model & Operational Reconciliation Plan -->
  <div class="card">
    <div class="card-header">
      <h2 class="card-title">Reconciliation Plan: Model Augmentation vs Operational Enforcement</h2>
      <div class="text-xs text-muted">Closing the Gap between Theory and Reality</div>
    </div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Action ID</th>
            <th>Reconciliation Type</th>
            <th>Target Element</th>
            <th>Action Description</th>
            <th>Accountable Owner</th>
            <th>Priority</th>
          </tr>
        </thead>
        <tbody>
          {"".join(recon_rows)}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Footer -->
  <footer class="footer">
    Generated by <strong>Celonis-Signavio-Comparator</strong> &bull; Process Studio BYOS Engine &bull; Conformance & BPMN Augmentation Suite
  </footer>

</div>

</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Generate HTML comparison report.")
    parser.add_argument("--input", required=True, help="Path to comparison-spec.json")
    parser.add_argument("--output", required=True, help="Path to output HTML report")
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

    html_content = generate_html_report(data)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_content, encoding="utf-8")
    print(f"PASS: wrote comparison report to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
