---
name: celonis-signavio-comparator
description: Compares a target/prescribed BPMN process model (imported from Signavio or uploaded BPMN 2.0 XML) against actual execution reality mined from Celonis event logs. Identifies conformance deviations (undocumented shadow steps, skipped activities, out-of-sequence/maverick transitions, rework loops, SLA latency bottlenecks). Produces an executive HTML comparison report, an Excel comparison matrix, and generates an augmented BPMN 2.0 XML model enriched with Celonis exception flows, metrics, and visual heatmap styling. Use when the user wants to compare theory with reality, perform conformance checking, or augment BPMN models with process mining findings.
allowed-tools: run_skill_script read_wiki_page write_temp_file read_temp_file save_output_text save_output_file
---

# Celonis-Signavio-Comparator

Compares prescriptive BPMN process models (Theory / Signavio / uploaded BPMN 2.0) against actual empirical process execution data mined from Celonis (Reality / Event Logs).

Inputs:
- **Theory Process Model**: A Signavio BPMN export, uploaded BPMN 2.0 XML file, or text description of the prescribed standard operating procedure (SOP).
- **Reality Process Data**: Celonis process mining analysis, event log summary, PQL query findings, or bottleneck report.

Outputs (generated every run):
1. `celonis-signavio-comparison-report.html`: Interactive, self-contained executive comparison report with visual flow maps, KPI scorecards, activity conformance matrix, bottleneck breakdown, and reconciliation roadmap.
2. `augmented-process.bpmn`: Valid BPMN 2.0 XML model enriching the original Signavio model with Celonis exception flows, shadow activities, performance metrics annotations, and color-coded BPMNDI visual styling (Green = Happy Path, Amber = Bottleneck, Red = Shadow Deviation).
3. `comparison-matrix.xlsx`: Structured multi-tab Excel workbook with Conformance Review sheets and editable Stakeholder Decision dropdowns for model reconciliation workshops.

Never write code at runtime. You author one structured `comparison-spec.json` file, and bundled scripts render the deliverables.

## Do Not Ask Questions
Work directly from the provided documents. Use these standard defaults and report them in your delivery summary:
- Report Title: The process name from the source plus " — Theory vs. Reality Conformance Report".
- SLA Default: If the BPMN model lacks explicit duration SLAs, use 15.0 days as the default baseline SLA for end-to-end throughput.
- Conformance Score: Derived directly from the Celonis happy-path case share percentage.
- Target Actions: Grouped into "Augment BPMN Model" (for legitimate real-world variations) vs "Operational Enforcement" (for wasteful deviations and compliance violations).

## Steps

1. **Read & Extract**:
   - Ingest the Signavio / BPMN source (prescribed tasks, sequence flows, gateway logic, swimlane roles).
   - Ingest the Celonis source (case volume, event counts, activity frequency, transition waiting times, rework loops, maverick buying / retro-PO rates).
2. **Analyze Differences (Theory vs Reality)**:
   - Identify **Matched Activities**: Tasks existing in both Signavio design and Celonis execution.
   - Identify **Undocumented Shadow Steps**: Activities occurring in Celonis that are missing in Signavio (e.g., Price Changes, Payment Block/Unblock, Reversals, Dunning).
   - Identify **Skipped / Bypassed Activities**: Tasks designed in Signavio that cases frequently skip in reality.
   - Identify **Sequence & Maverick Violations**: Out-of-order execution (e.g., Invoice Receipt before PO Item Creation).
   - Quantify **Latency & Throughput Deltas**: Modeled SLA vs actual empirical throughput and waiting bottlenecks.
3. **Write the Comparison Spec**:
   - Construct `comparison-spec.json` adhering to the schema below.
   - Save it using `write_temp_file(file_path="comparison-spec.json", content=...)`.
4. **Build Comparison Report**:
   - Call `run_skill_script` with script `build_comparison_report.py`, `--input comparison-spec.json`, `--output celonis-signavio-comparison-report.html`.
   - If validation errors are reported, fix `comparison-spec.json` and re-run.
5. **Generate Augmented BPMN 2.0 XML**:
   - Call `run_skill_script` with script `augment_bpmn.py`, `--input comparison-spec.json`, `--output augmented-process.bpmn`.
6. **Build Excel Review Matrix**:
   - Call `run_skill_script` with script `build_comparison_sheet.py`, `--input comparison-spec.json`, `--output comparison-matrix.xlsx`.
7. **Deliver**:
   - Save the deliverables using `save_output_file` for `celonis-signavio-comparison-report.html`, `augmented-process.bpmn`, and `comparison-matrix.xlsx`.
   - Reply with an executive summary covering the overall Conformance Score (%), top shadow deviations, largest latency bottlenecks, and key reconciliation recommendations.

---

## `comparison-spec.json` Format

```json
{
  "meta": {
    "process_name": "Purchase-to-Pay (P2P)",
    "signavio_model_name": "Standard P2P Process v2.4",
    "signavio_model_id": "SIG-P2P-2026-001",
    "celonis_data_model": "P2P Model (SAP ECC/S4)",
    "celonis_model_id": "6a5f1b3d-3434-4c41-8c0e-15d4530e04f6",
    "analysis_date": "2026-11-20",
    "timeframe": "2016-01-01 to 2017-01-06",
    "case_count": 1116080,
    "event_count": 6733164,
    "conformance_rate_pct": 68.2,
    "avg_throughput_days": 31.1,
    "modeled_sla_days": 15.0
  },
  "executive_summary": {
    "headline": "Only 68.2% of cases follow the Signavio happy path; 31.8% incur rework or exception loops adding +8.6 days of delay.",
    "key_takeaways": [
      "Post-PO price modifications occur in 13.6% of cases (+8.8 days delay) and are unrepresented in Signavio.",
      "Invoice-to-payment wait (11.7 days) is the largest latency bottleneck across the entire lifecycle.",
      "Maverick buying (7.0% invoice before PO) creates substantial compliance exposure."
    ],
    "conformance_score": 68.2,
    "rework_rate_pct": 31.8,
    "maverick_rate_pct": 7.0,
    "avg_delay_days": 16.1
  },
  "activities": [
    {
      "id": "act_create_po",
      "name": "Create PO item",
      "original_name_de": "Lege Bestellposition an",
      "status": "matched",
      "signavio_presence": true,
      "signavio_lane": "Purchaser",
      "celonis_presence": true,
      "celonis_events": 1116080,
      "celonis_case_pct": 100.0,
      "avg_duration_days": 0.0,
      "conformance_notes": "Prescribed initial step; 100% case coverage."
    },
    {
      "id": "act_change_price",
      "name": "Change price",
      "original_name_de": "Aendere Preis",
      "status": "undocumented_reality",
      "signavio_presence": false,
      "signavio_lane": null,
      "celonis_presence": true,
      "celonis_events": 152092,
      "celonis_case_pct": 13.6,
      "avg_duration_days": 10.0,
      "conformance_notes": "Undocumented rework step in Signavio. Adds +8.8 days delay."
    }
  ],
  "transitions": [
    {
      "source": "Record invoice receipt",
      "target": "Pay invoice",
      "status": "matched_delayed",
      "volume": 905259,
      "avg_wait_days": 11.7,
      "modeled_wait_days": 2.0,
      "delta_days": 9.7,
      "severity": "critical",
      "notes": "Major queuing bottleneck due to batch payment schedules."
    }
  ],
  "deviations": [
    {
      "id": "DEV-01",
      "type": "undocumented_activity",
      "title": "Post-PO Price Modification",
      "description": "152,092 items (13.6%) modified after PO dispatch.",
      "affected_volume": 152092,
      "pct_of_total": 13.6,
      "time_penalty_days": 8.8,
      "cost_impact_est": "$450,000",
      "severity": "high",
      "recommendation_type": "operational_fix",
      "recommendation": "Synchronize contract master data before PO dispatch; augment BPMN with optional price tolerance review gateway."
    }
  ],
  "reconciliation_plan": [
    {
      "action_id": "REC-01",
      "target_type": "augment_bpmn",
      "element_affected": "Change Price / Exception Gateway",
      "description": "Insert exclusive gateway after 'Send PO' to model legitimate supplier price confirmation loop.",
      "owner": "BPM Center of Excellence",
      "priority": "High"
    }
  ]
}
```

---

## Rules
- **Conformance Classifications**:
  - `matched`: Activity present in both Signavio model and Celonis event log.
  - `undocumented_reality`: Shadow activity discovered in Celonis, omitted from Signavio.
  - `skipped_in_reality`: Prescribed Signavio activity omitted/bypassed in actual execution.
- **Augmented BPMN Output**: The generated `augmented-process.bpmn` must always be strictly valid OMG BPMN 2.0 XML with full BPMNDI geometry, text annotations, and bioc color highlights.
- **Empirical Rigor**: All case counts, percentages, and days must derive directly from the source data or explicitly be labeled as illustrative estimates.
