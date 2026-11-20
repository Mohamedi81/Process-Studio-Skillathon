#!/usr/bin/env python3
"""Validation helper for comparison-spec.json used by Celonis-Signavio-Comparator."""
from typing import List, Dict, Any


def validate_spec(data: Dict[str, Any]) -> List[str]:
    """Validate comparison spec dictionary and return list of error messages."""
    errors = []
    if not isinstance(data, dict):
        return ["Root JSON must be an object"]

    # Meta validation
    meta = data.get("meta")
    if not meta or not isinstance(meta, dict):
        errors.append("Missing or invalid 'meta' object")
    else:
        for req_key in ("process_name", "conformance_rate_pct", "avg_throughput_days"):
            if req_key not in meta or meta[req_key] is None:
                errors.append(f"meta: missing required key '{req_key}'")

    # Executive Summary validation
    exec_sum = data.get("executive_summary")
    if not exec_sum or not isinstance(exec_sum, dict):
        errors.append("Missing or invalid 'executive_summary' object")
    else:
        for req_key in ("headline", "key_takeaways", "conformance_score"):
            if req_key not in exec_sum or exec_sum[req_key] is None:
                errors.append(f"executive_summary: missing required key '{req_key}'")

    # Activities validation
    activities = data.get("activities")
    if not isinstance(activities, list) or len(activities) == 0:
        errors.append("Missing or empty 'activities' list")
    else:
        for idx, act in enumerate(activities):
            if not isinstance(act, dict):
                errors.append(f"activities[{idx}]: must be an object")
                continue
            for req in ("name", "status"):
                if req not in act:
                    errors.append(f"activities[{idx}]: missing required key '{req}'")

    # Transitions validation (optional but if present must be list of objects)
    transitions = data.get("transitions")
    if transitions is not None and not isinstance(transitions, list):
        errors.append("'transitions' must be a list if provided")

    # Deviations validation (optional but if present must be list of objects)
    deviations = data.get("deviations")
    if deviations is not None and not isinstance(deviations, list):
        errors.append("'deviations' must be a list if provided")

    # Reconciliation plan validation (optional but if present must be list of objects)
    recon = data.get("reconciliation_plan")
    if recon is not None and not isinstance(recon, list):
        errors.append("'reconciliation_plan' must be a list if provided")

    return errors
