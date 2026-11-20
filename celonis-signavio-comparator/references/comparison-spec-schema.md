# Comparison Spec Schema (`comparison-spec.json`)

The `comparison-spec.json` file is the central data contract authored by the model and ingested by all bundled scripts (`build_comparison_report.py`, `augment_bpmn.py`, `build_comparison_sheet.py`).

## JSON Structure

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
      "Significant shadow activities (Price changes post-PO, payment blocks) are missing in the Signavio model.",
      "Invoice-to-payment wait (11.7 days) is the largest latency bottleneck, far exceeding the modeled 2-day SLA.",
      "Maverick buying (7.0% of cases receiving invoice before PO creation) violates core procurement compliance."
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
      "signavio_step_num": 1,
      "celonis_presence": true,
      "celonis_events": 1116080,
      "celonis_case_pct": 100.0,
      "avg_duration_days": 0.0,
      "category": "happy_path",
      "conformance_notes": "Core starting activity, 100% aligned with Signavio."
    },
    {
      "id": "act_change_price",
      "name": "Change price",
      "original_name_de": "Aendere Preis",
      "status": "undocumented_reality",
      "signavio_presence": false,
      "signavio_lane": null,
      "signavio_step_num": null,
      "celonis_presence": true,
      "celonis_events": 152092,
      "celonis_case_pct": 13.6,
      "avg_duration_days": 10.0,
      "category": "rework_shadow",
      "conformance_notes": "Undocumented in Signavio. Adds +8.8 days to case duration."
    }
  ],
  "transitions": [
    {
      "source": "Record invoice receipt",
      "target": "Pay invoice",
      "status": "matched_delayed",
      "signavio_presence": true,
      "celonis_presence": true,
      "volume": 905259,
      "avg_wait_days": 11.7,
      "modeled_wait_days": 2.0,
      "delta_days": 9.7,
      "severity": "critical",
      "notes": "Largest waiting bottleneck in execution."
    },
    {
      "source": "Record invoice receipt",
      "target": "Create PO item",
      "status": "out_of_sequence_maverick",
      "signavio_presence": false,
      "celonis_presence": true,
      "volume": 77964,
      "avg_wait_days": 2.0,
      "modeled_wait_days": null,
      "delta_days": null,
      "severity": "high",
      "notes": "Retroactive PO / Maverick buying violation."
    }
  ],
  "deviations": [
    {
      "id": "DEV-01",
      "type": "undocumented_activity",
      "title": "Post-PO Price Modification",
      "description": "152,092 PO items (13.6%) have prices modified ~7 days after PO dispatch.",
      "affected_volume": 152092,
      "pct_of_total": 13.6,
      "time_penalty_days": 8.8,
      "cost_impact_est": "$450,000",
      "severity": "high",
      "recommendation_type": "operational_fix",
      "recommendation": "Synchronize contract master data before PO dispatch; augment BPMN with optional price tolerance review gateway."
    }
  ],
  "bottlenecks": [
    {
      "id": "BOT-01",
      "stage": "Invoice Receipt -> Payment",
      "avg_wait_days": 11.7,
      "sla_target_days": 2.0,
      "volume": 905259,
      "total_waiting_days_millions": 10.6,
      "root_cause": "Batch payment run cycles and manual approval queues",
      "remedy": "Automate 3-way match and enable dynamic early payment discounts"
    }
  ],
  "reconciliation_plan": [
    {
      "action_id": "REC-01",
      "target_type": "augment_bpmn",
      "element_affected": "Change Price / Exception Gateway",
      "description": "Insert exclusive gateway after 'Send PO' to model legitimate supplier price confirmation loop with 4-eyes approval.",
      "owner": "BPM Center of Excellence",
      "priority": "High"
    },
    {
      "action_id": "REC-02",
      "target_type": "enforce_reality",
      "element_affected": "No-PO-No-Pay Enforcement",
      "description": "Block invoices in ERP without prior PO reference to eliminate 77.9k maverick buying cases.",
      "owner": "Finance Operations & Procurement",
      "priority": "Critical"
    }
  ]
}
```

## Required Fields
- `meta`: `process_name`, `case_count`, `conformance_rate_pct`, `avg_throughput_days`.
- `executive_summary`: `headline`, `key_takeaways`, `conformance_score`, `rework_rate_pct`.
- `activities`: array with `id`, `name`, `status`, `signavio_presence`, `celonis_presence`.
- `transitions`: array with `source`, `target`, `status`, `volume`, `avg_wait_days`.
- `deviations`: array with `id`, `type`, `title`, `description`, `severity`, `recommendation`.
- `reconciliation_plan`: array with `action_id`, `target_type`, `description`, `owner`, `priority`.
