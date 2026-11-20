---
name: celonis-signavio-comparator
description: Compares a target/prescribed BPMN process model (loaded from connected Signavio context, imported from workspace BPMN files, or uploaded directly) against actual execution reality mined from Celonis event logs. Identifies conformance deviations (undocumented shadow steps, skipped activities, out-of-sequence/maverick transitions, rework loops, SLA latency bottlenecks). Produces an executive HTML comparison report, an Excel comparison matrix, a visual BPMN conformance heatmap, and a clean standardized To-Be BPMN 2.0 model with swimlanes ready for SAP Signavio import. Use when the user wants to compare theory with reality, perform conformance checking, or augment BPMN models with process mining findings.
allowed-tools: run_skill_script read_wiki_page write_temp_file read_temp_file save_output_text save_output_file
---

# Celonis-Signavio-Comparator

Compares prescriptive BPMN process models (Theory / Signavio / uploaded BPMN 2.0) against actual empirical process execution data mined from Celonis (Reality / Event Logs).

Inputs:
- **Theory Process Model (any ONE of the following options)**:
  - **Option 1: Direct File Attachment**: An uploaded `.bpmn` or `.xml` BPMN 2.0 file attached directly to the prompt.
  - **Option 2: Signavio Context / Workspace Repository (when BPMN is not attached)**: If no BPMN file is attached in chat, look for and load the process model from the **connected Signavio context**, project wiki pages (using `read_wiki_page`), or workspace repository containing exported Signavio BPMN files.
  - **Option 3: Prescribed SOP / Text Description**: A written standard operating procedure (SOP) or process blueprint defining the prescribed happy path, decision gates, and swimlane roles.
- **Reality Process Data**: Celonis process mining analysis, event log summary, PQL query findings, or bottleneck report.

Outputs (generated every run):
1. `celonis-signavio-comparison-report.html`: Interactive, self-contained executive comparison report with visual flow maps, KPI scorecards, activity conformance matrix, bottleneck breakdown, and reconciliation roadmap.
2. `augmented-conformance-heatmap.bpmn`: Visual BPMN 2.0 Conformance Heatmap with color-coded tasks (Green = Happy Path, Amber = Latency Bottleneck, Red = Shadow Exception), metric text annotations, and clean XOR gateways for visual review in Process Studio, Camunda, or BPMN.io.
3. `signavio-target-process.bpmn`: Clean, production-ready To-Be BPMN 2.0 model with organizational swimlanes (Purchasing, Logistics, Accounts Payable), formal exception gateways, and neutral styling ready for direct import into SAP Signavio Process Manager.
4. `comparison-matrix.xlsx`: Structured multi-tab Excel workbook with Conformance Review sheets and editable Stakeholder Decision dropdowns for model reconciliation workshops.

Never write code at runtime. You author one structured `comparison-spec.json` file, and bundled scripts render the deliverables.

## Do Not Ask Questions
Work directly from the provided documents. If a BPMN file is not attached, automatically check the Signavio context or wiki pages. Use these standard defaults and report them in your delivery summary:
- Report Title: The process name from the source plus " — Theory vs. Reality Conformance Report".
- SLA Default: If the BPMN model lacks explicit duration SLAs, use 15.0 days as the default baseline SLA for end-to-end throughput.
- Conformance Score: Derived directly from the Celonis happy-path case share percentage.
- Target Actions: Grouped into "Augment BPMN Model" (for legitimate real-world variations) vs "Operational Enforcement" (for wasteful deviations and compliance violations).

## Steps

1. **Read & Extract**:
   - **Ingest Theory (Signavio / BPMN)**:
     - Check for directly attached BPMN XML files.
     - If no BPMN file is attached, inspect the **Signavio context** or use `read_wiki_page` to retrieve the Signavio process model from the project repository.
     - Extract prescribed activities, sequence flows, decision gateway logic, and swimlane roles.
   - **Ingest Reality (Celonis)**:
     - Ingest case volume, event counts, activity frequency, transition waiting times, rework loops, and maverick buying / retro-PO rates.
2. **Analyze Differences (Theory vs Reality)**:
   - Identify **Matched Activities**: Tasks existing in both Signavio design and Celonis execution.
   - Identify **Undocumented Shadow Steps**: Activities occurring in Celonis that are missing in Signavio (e.g., Price Changes, Payment Block/Unblock, Reversals, Dunning).
   - Identify **Skipped / Bypassed Activities**: Tasks designed in Signavio that cases frequently skip in reality.
   - Identify **Sequence & Maverick Violations**: Out-of-order execution (e.g., Invoice Receipt before PO Item Creation).
   - Quantify **Latency & Throughput Deltas**: Modeled SLA vs actual empirical throughput and waiting bottlenecks.
3. **Write the Comparison Spec**:
   - Construct `comparison-spec.json` adhering to the schema in `references/comparison-spec-schema.md`.
   - Save it using `write_temp_file(file_path="comparison-spec.json", content=...)`.
4. **Build Comparison Report**:
   - Call `run_skill_script` with script `build_comparison_report.py`, `--input comparison-spec.json`, `--output celonis-signavio-comparison-report.html`.
   - If validation errors are reported, fix `comparison-spec.json` and re-run.
5. **Generate BPMN Models (Heatmap & Clean Signavio)**:
   - Call `run_skill_script` with script `augment_bpmn.py`, `--input comparison-spec.json`, `--output augmented-conformance-heatmap.bpmn`. (This generates both `augmented-conformance-heatmap.bpmn` and `signavio-target-process.bpmn`).
6. **Build Excel Review Matrix**:
   - Call `run_skill_script` with script `build_comparison_sheet.py`, `--input comparison-spec.json`, `--output comparison-matrix.xlsx`.
7. **Deliver**:
   - Save the deliverables using `save_output_file` for `celonis-signavio-comparison-report.html`, `augmented-conformance-heatmap.bpmn`, `signavio-target-process.bpmn`, and `comparison-matrix.xlsx`.
   - Reply with an executive summary covering the overall Conformance Score (%), top shadow deviations, largest latency bottlenecks, and key reconciliation recommendations.
