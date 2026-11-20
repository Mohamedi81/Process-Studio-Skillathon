# BPMN 2.0 Model Augmentation Guide

This reference explains how the `augment_bpmn.py` script augments a Signavio or baseline BPMN 2.0 XML model with findings mined from Celonis.

---

## 1. Augmentation Objectives

1. **Incorporate Discovered Reality**: Insert tasks and exception branches that occur in reality (e.g. Price Change, Payment Block & Release, Maverick Handling) using standard BPMN 2.0 syntax.
2. **Overlay Performance Metrics**: Attach text annotations and associations displaying actual execution frequency (% of cases) and average waiting/execution duration.
3. **Visual Heatmap Styling (BPMNDI)**: Apply standard BPMN Diagram Interchange (BPMNDI) styling attributes to distinguish compliant happy paths from bottlenecks and undocumented shadow activities.

---

## 2. BPMN 2.0 XML Structure & Namespaces

A valid augmented BPMN 2.0 document must include the standard namespaces:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions
    xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
    xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
    xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
    xmlns:bioc="http://bpmn.io/schema/bpmn/biocolor/1.0"
    xmlns:color="http://www.omg.org/spec/BPMN/non-normative/color/1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    id="Definitions_Augmented"
    targetNamespace="http://bpmn.io/schema/bpmn">
  
  <bpmn:process id="Process_Augmented" isExecutable="false">
    <!-- Tasks, Gateways, Sequence Flows, Annotations -->
  </bpmn:process>

  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_Augmented">
      <!-- BPMNShape and BPMNEdge elements with coordinate geometry -->
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</bpmn:definitions>
```

---

## 3. Visual Color Palette (BPMNDI & Biocolor)

| Conformance State | Stroke (`bioc:stroke`) | Fill (`bioc:fill`) | Meaning |
|---|---|---|---|
| **Compliant Happy Path** | `#10b981` (Green) | `#d1fae5` (Light Green) | Tasks & flows matching Signavio model with high conformance |
| **Bottleneck / Latency** | `#f59e0b` (Amber) | `#fef3c7` (Light Amber) | Modeled steps exhibiting severe execution delays or queue time |
| **Undocumented Shadow Step** | `#ef4444` (Red) | `#fee2e2` (Light Red) | Celonis-discovered activities not present in the original model |
| **Rework Loop** | `#dc2626` (Crimson) | `#fee2e2` (Light Red) | Repetitive / self-loop tasks (e.g. GR reversal, repeated edits) |
| **Skipped in Reality** | `#9ca3af` (Grey) | `#f3f4f6` (Light Grey) | Modelled tasks frequently bypassed in reality |

---

## 4. Text Annotations for Performance Overlays

For each activity with significant metrics, a linked Text Annotation is attached:

```xml
<bpmn:textAnnotation id="Annotation_act_change_price">
  <bpmn:text>Reality: 13.6% of cases (152,092 events)
Avg Delay: +8.8 days
Category: Rework Loop</bpmn:text>
</bpmn:textAnnotation>

<bpmn:association id="Assoc_act_change_price"
  sourceRef="act_change_price"
  targetRef="Annotation_act_change_price" />
```

---

## 5. Compatibility & Re-import

The augmented BPMN file output (`augmented-process.bpmn`) is strictly compliant with the OMG BPMN 2.0 XML standard and can be directly imported into:
- **SAP Signavio Process Manager** (via XML / BPMN 2.0 import)
- **Camunda Modeler / Camunda 8**
- **BPMN.io web modelers**
- **IBM Process Studio / Business Automation Studio**
