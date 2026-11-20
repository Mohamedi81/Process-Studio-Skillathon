# Theory vs. Reality: Comparing Signavio BPMN Models with Celonis Process Mining

When prescriptive process models designed in SAP Signavio (Theory / As-Planned) meet actual transactional execution data mined by Celonis (Reality / As-Is), organizations uncover a profound gap between how they *believe* their business operates and how it *actually* runs.

This guide details the core comparison dimensions, common deviation patterns, analytical metrics, and reconciliation strategies.

---

## 1. The Core Dichotomy: De Jure vs. De Facto

| Dimension | Signavio (Theory / Prescriptive) | Celonis (Reality / Descriptive) |
|---|---|---|
| **Nature** | Standard Operating Procedure (SOP), Idealized Target | Digital Footprint, Timestamped Transaction Log |
| **Perspective** | How the process *should* run | How the process *does* run |
| **Coverage** | Happy path, standard decision gates, modeled exceptions | 100% of case variants, edge cases, friction points |
| **Durations** | Theoretical SLAs (e.g., "1 day approval") | Empirical cycle & waiting times (e.g., "8.1 days average") |
| **Control** | Formal governance, assigned swimlanes | Observed user IDs, bot/system executions, bypasses |

---

## 2. The Five Conformance & Delta Dimensions

### A. Structural Conformance & Flow Alignment
- **Happy Path Fitness Rate**: The percentage of total cases that follow the modeled Signavio flow from start to end without deviations.
- **Process Variant Proliferation**: Signavio models typically depict 1–3 clean paths; Celonis routinely discovers 50–500+ execution variants across thousands of cases.

### B. Undocumented Activities (Shadow Steps)
- Activities recorded in the event log that **do not exist** in the Signavio model.
- *Examples in P2P / O2C*:
  - "Change Price" (post-PO dispatch rework)
  - "Set Payment Block" / "Remove Payment Block"
  - "Reverse Goods Receipt"
  - "Remind for Order Confirmation"
  - "Dunning Notice Sent"
- *Root causes*: Master data gaps, manual workarounds, supplier discrepancies, missing system integration.

### C. Skipped / Bypassed Activities
- Mandatory or governance activities defined in Signavio that **never occurred** in Celonis for specific cases.
- *Examples*:
  - Skipping "Create Purchase Requisition" (direct PO creation)
  - Skipping "Quality Inspection" on goods receipt
  - Skipping "Manager Approval" for certain threshold tiers
- *Impact*: Audit vulnerability, internal control failures, regulatory non-compliance.

### D. Sequence Violations & Out-of-Order Execution (Maverick Paths)
- Activities that occur in a sequence contrary to the designed BPMN flow.
- *Classic Maverick Buying*:
  - `Record Invoice Receipt` -> `Create PO Item` (Retroactive POs / Maverick Buying). Invoices arrive before authorization exists.
  - `Goods Receipt` -> `Pay Invoice` without recorded Invoice Receipt event (EDI or automated bypass).
  - `Pay Invoice` occurring before `Record Invoice Receipt`.

### E. Rework Loops & Multi-Touch Latency
- Single tasks in BPMN that cycle repeatedly in reality.
- *Self-Loops & Ping-Pong Loops*:
  - Repeated price changes, quantity modifications, or multiple goods-receipt reversal cycles.
  - Approval ping-pong between department and finance.
- *Latency Penalty*: Quantifies the extra cycle time and cost introduced by rework loops compared to the single-pass happy path.

---

## 3. Performance & Bottleneck Analysis

| Comparison Point | Theoretical Model (Signavio) | Empirical Reality (Celonis) | Delta / Finding |
|---|---|---|---|
| **Total Throughput Time** | Modeled SLA (e.g. 15 days) | Actual average & median (e.g. 31.1 days) | **+16.1 days delta** |
| **Handoff Waiting Times** | Zero or minimal queue time assumed | Major queuing between stages (e.g. Invoice -> Pay = 11.7 days) | **Identified bottleneck** |
| **Rework Throughput Impact** | 0 days (not modeled) | +8.8 days for price change; +11.4 days for payment block | **Friction penalty** |
| **Automation Rate** | Modeled as Automated / Manual | Empirical breakdown by User Type / System Actor | **Automation gap** |

---

## 4. Reconciliation Strategy: Model Update vs. Operational Enforcement

When differences are identified, organizations have two reconciliation levers:

```
                      +---------------------------------------+
                      | Celonis Reality vs. Signavio Theory   |
                      +---------------------------------------+
                                          |
                   +----------------------+----------------------+
                   |                                             |
                   v                                             v
     [ Legitimate Real-World Need ]               [ Wasteful / Non-Compliant ]
  (e.g., standard price renegotiation,          (e.g., maverick buying, avoidable
   supplier confirmation sub-process)            price errors, manual block releases)
                   |                                             |
                   v                                             v
      AUGMENT SIGNAVIO BPMN MODEL                   OPERATIONAL ENFORCEMENT & FIXES
   - Add XOR exception gateways                  - Enforce No-PO-No-Pay system gates
   - Model discovered sub-processes              - Implement automated 3-way matching
   - Calibrate realistic SLAs                    - Master data contract synchronization
   - Enforce updated swimlane roles              - Automated guided user workflows
```

---

## 5. Augmenting BPMN 2.0 Models with Process Mining Insights

The **Augmented BPMN 2.0** file combines the clean architecture of the original design with the empirical reality discovered by process mining:

1. **Discovered Exception Branches**: Inserts exclusive gateways (`bpmn:exclusiveGateway`) and new tasks (`bpmn:task` / `bpmn:userTask` / `bpmn:serviceTask`) for valid real-world variations.
2. **Performance Annotations**: Attaches text annotations (`bpmn:textAnnotation`) and associations (`bpmn:association`) displaying case frequency (%) and average duration on activities and sequence flows.
3. **Visual Heatmap Styling (BPMN DI)**:
   - `bioc:stroke="#10b981"` / `bioc:fill="#d1fae5"`: **Green** = Compliant Happy Path
   - `bioc:stroke="#f59e0b"` / `bioc:fill="#fef3c7"`: **Amber** = Modeled path with severe latency/bottlenecks
   - `bioc:stroke="#ef4444"` / `bioc:fill="#fee2e2"`: **Red** = Undocumented shadow activity or high-rework loop
   - Dotted / Dashed sequence flows for reality-discovered transitions.
