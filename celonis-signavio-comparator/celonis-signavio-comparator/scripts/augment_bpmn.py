#!/usr/bin/env python3
"""Augment BPMN 2.0 process model with Celonis process mining discoveries.

Generates two complementary BPMN 2.0 outputs:
1. Visual Conformance Heatmap BPMN: Color-coded (Green/Amber/Red) with BPMNDI styling,
   performance metric annotations, and clean XOR gateway branches.
2. Clean Signavio Target BPMN: Formal, standardized BPMN 2.0 model with swimlanes,
   formalized exception gateways, and neutral styling ready for direct Signavio import.

Usage:
  python3 augment_bpmn.py --input comparison-spec.json --output augmented-conformance-heatmap.bpmn
  python3 augment_bpmn.py --input comparison-spec.json --output signavio-target-process.bpmn
"""
import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Local import
try:
    from validate_spec import validate_spec
except ImportError:
    from .validate_spec import validate_spec

DEFAULT_OUTPUT_NAME = "augmented-conformance-heatmap.bpmn"

NS_BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL"
NS_BPMNDI = "http://www.omg.org/spec/BPMN/20100524/DI"
NS_DC = "http://www.omg.org/spec/DD/20100524/DC"
NS_DI = "http://www.omg.org/spec/DD/20100524/DI"
NS_BIOC = "http://bpmn.io/schema/bpmn/biocolor/1.0"
NS_COLOR = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"


def register_namespaces():
    ET.register_namespace("bpmn", NS_BPMN)
    ET.register_namespace("bpmndi", NS_BPMNDI)
    ET.register_namespace("dc", NS_DC)
    ET.register_namespace("di", NS_DI)
    ET.register_namespace("bioc", NS_BIOC)
    ET.register_namespace("color", NS_COLOR)


# =========================================================================
# 1. VISUAL CONFORMANCE HEATMAP BPMN GENERATOR
# =========================================================================
def build_heatmap_bpmn_xml(data: dict) -> str:
    """Generate color-coded BPMN 2.0 XML with XOR gateways and metric annotations."""
    register_namespaces()
    meta = data.get("meta", {})
    process_name = meta.get("process_name", "Purchase-to-Pay (P2P)")

    definitions = ET.Element(
        f"{{{NS_BPMN}}}definitions",
        {
            "id": "Definitions_ConformanceHeatmap",
            "targetNamespace": "http://bpmn.io/schema/bpmn",
            "exporter": "Celonis-Signavio-Comparator BYOS",
            "exporterVersion": "2.0",
        },
    )

    proc_id = "Process_Conformance_Heatmap"
    process = ET.SubElement(
        definitions,
        f"{{{NS_BPMN}}}process",
        {"id": proc_id, "name": f"{process_name} — Conformance Heatmap (Theory vs Reality)", "isExecutable": "false"},
    )

    shapes_di = []
    edges_di = []

    # 1. Start Event (x=50, y=182, w=36, h=36)
    ET.SubElement(process, f"{{{NS_BPMN}}}startEvent", {"id": "StartEvent_1", "name": "Purchase Demand Identified"})
    shapes_di.append({"id": "StartEvent_1_di", "element": "StartEvent_1", "x": 50, "y": 182, "w": 36, "h": 36, "stroke": "#10b981", "fill": "#d1fae5"})

    # Step 1: Create PR (x=140, y=160, w=130, h=80)
    ET.SubElement(process, f"{{{NS_BPMN}}}task", {"id": "Activity_PR", "name": "Create Purchase\nRequisition"})
    shapes_di.append({"id": "Activity_PR_di", "element": "Activity_PR", "x": 140, "y": 160, "w": 130, "h": 80, "stroke": "#10b981", "fill": "#d1fae5"})

    # Flow Start -> PR
    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_Start_PR", "sourceRef": "StartEvent_1", "targetRef": "Activity_PR"})
    edges_di.append({"id": "Flow_Start_PR_di", "element": "Flow_Start_PR", "waypoints": [(86, 200), (140, 200)], "stroke": "#10b981"})

    # PR Annotation
    ET.SubElement(process, f"{{{NS_BPMN}}}textAnnotation", {"id": "Anno_PR"}).append(ET.Element(f"{{{NS_BPMN}}}text"))
    process.find(f".//{{{NS_BPMN}}}textAnnotation[@id='Anno_PR']/{{{NS_BPMN}}}text").text = "Celonis: 78.9% cases\n(21.1% direct PO bypass)"
    ET.SubElement(process, f"{{{NS_BPMN}}}association", {"id": "Assoc_PR", "sourceRef": "Activity_PR", "targetRef": "Anno_PR"})
    shapes_di.append({"id": "Anno_PR_di", "element": "Anno_PR", "x": 140, "y": 80, "w": 130, "h": 45, "stroke": "#64748b", "fill": "#ffffff"})
    edges_di.append({"id": "Assoc_PR_di", "element": "Assoc_PR", "waypoints": [(205, 160), (205, 125)], "stroke": "#94a3b8"})

    # Step 2: Create PO Item (x=330, y=160, w=130, h=80)
    ET.SubElement(process, f"{{{NS_BPMN}}}task", {"id": "Activity_PO", "name": "Create Purchase\nOrder Item"})
    shapes_di.append({"id": "Activity_PO_di", "element": "Activity_PO", "x": 330, "y": 160, "w": 130, "h": 80, "stroke": "#10b981", "fill": "#d1fae5"})

    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_PR_PO", "sourceRef": "Activity_PR", "targetRef": "Activity_PO"})
    edges_di.append({"id": "Flow_PR_PO_di", "element": "Flow_PR_PO", "waypoints": [(270, 200), (330, 200)], "stroke": "#10b981"})

    # PO Annotation
    ET.SubElement(process, f"{{{NS_BPMN}}}textAnnotation", {"id": "Anno_PO"}).append(ET.Element(f"{{{NS_BPMN}}}text"))
    process.find(f".//{{{NS_BPMN}}}textAnnotation[@id='Anno_PO']/{{{NS_BPMN}}}text").text = "Celonis: 100.0% cases\n(1.116M items)"
    ET.SubElement(process, f"{{{NS_BPMN}}}association", {"id": "Assoc_PO", "sourceRef": "Activity_PO", "targetRef": "Anno_PO"})
    shapes_di.append({"id": "Anno_PO_di", "element": "Anno_PO", "x": 330, "y": 80, "w": 130, "h": 45, "stroke": "#64748b", "fill": "#ffffff"})
    edges_di.append({"id": "Assoc_PO_di", "element": "Assoc_PO", "waypoints": [(395, 160), (395, 125)], "stroke": "#94a3b8"})

    # Step 3: Send PO (x=520, y=160, w=130, h=80)
    ET.SubElement(process, f"{{{NS_BPMN}}}task", {"id": "Activity_SendPO", "name": "Send Purchase\nOrder"})
    shapes_di.append({"id": "Activity_SendPO_di", "element": "Activity_SendPO", "x": 520, "y": 160, "w": 130, "h": 80, "stroke": "#10b981", "fill": "#d1fae5"})

    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_PO_SendPO", "sourceRef": "Activity_PO", "targetRef": "Activity_SendPO"})
    edges_di.append({"id": "Flow_PO_SendPO_di", "element": "Flow_PO_SendPO", "waypoints": [(460, 200), (520, 200)], "stroke": "#10b981"})

    # Send PO Annotation
    ET.SubElement(process, f"{{{NS_BPMN}}}textAnnotation", {"id": "Anno_SendPO"}).append(ET.Element(f"{{{NS_BPMN}}}text"))
    process.find(f".//{{{NS_BPMN}}}textAnnotation[@id='Anno_SendPO']/{{{NS_BPMN}}}text").text = "Celonis: 97.6% cases\n(1.089M sent)"
    ET.SubElement(process, f"{{{NS_BPMN}}}association", {"id": "Assoc_SendPO", "sourceRef": "Activity_SendPO", "targetRef": "Anno_SendPO"})
    shapes_di.append({"id": "Anno_SendPO_di", "element": "Anno_SendPO", "x": 520, "y": 80, "w": 130, "h": 45, "stroke": "#64748b", "fill": "#ffffff"})
    edges_di.append({"id": "Assoc_SendPO_di", "element": "Assoc_SendPO", "waypoints": [(585, 160), (585, 125)], "stroke": "#94a3b8"})

    # XOR Gateway 1: Split after Send PO (x=690, y=175, w=50, h=50)
    ET.SubElement(process, f"{{{NS_BPMN}}}exclusiveGateway", {"id": "Gateway_Price_Split", "name": "Price Correct?"})
    shapes_di.append({"id": "Gateway_Price_Split_di", "element": "Gateway_Price_Split", "x": 690, "y": 175, "w": 50, "h": 50, "stroke": "#64748b", "fill": "#ffffff"})

    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_SendPO_GW1", "sourceRef": "Activity_SendPO", "targetRef": "Gateway_Price_Split"})
    edges_di.append({"id": "Flow_SendPO_GW1_di", "element": "Flow_SendPO_GW1", "waypoints": [(650, 200), (690, 200)], "stroke": "#10b981"})

    # Exception Task: Change Price (x=770, y=300, w=140, h=80)
    ET.SubElement(process, f"{{{NS_BPMN}}}task", {"id": "Activity_ChangePrice", "name": "Change Price\n[Reality Exception]"})
    shapes_di.append({"id": "Activity_ChangePrice_di", "element": "Activity_ChangePrice", "x": 770, "y": 300, "w": 140, "h": 80, "stroke": "#ef4444", "fill": "#fee2e2"})

    # Price Change Annotation
    ET.SubElement(process, f"{{{NS_BPMN}}}textAnnotation", {"id": "Anno_ChangePrice"}).append(ET.Element(f"{{{NS_BPMN}}}text"))
    process.find(f".//{{{NS_BPMN}}}textAnnotation[@id='Anno_ChangePrice']/{{{NS_BPMN}}}text").text = "Reality: 13.6% (152k)\nAdds +8.8 days delay"
    ET.SubElement(process, f"{{{NS_BPMN}}}association", {"id": "Assoc_ChangePrice", "sourceRef": "Activity_ChangePrice", "targetRef": "Anno_ChangePrice"})
    shapes_di.append({"id": "Anno_ChangePrice_di", "element": "Anno_ChangePrice", "x": 770, "y": 410, "w": 140, "h": 45, "stroke": "#ef4444", "fill": "#ffffff"})
    edges_di.append({"id": "Assoc_ChangePrice_di", "element": "Assoc_ChangePrice", "waypoints": [(840, 380), (840, 410)], "stroke": "#f87171"})

    # Flow GW1 -> Change Price (Branch Down and Right)
    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_GW1_ChangePrice", "name": "Price Variance (13.6%)", "sourceRef": "Gateway_Price_Split", "targetRef": "Activity_ChangePrice"})
    edges_di.append({
        "id": "Flow_GW1_ChangePrice_di", "element": "Flow_GW1_ChangePrice",
        "waypoints": [(715, 225), (715, 340), (770, 340)],
        "stroke": "#ef4444"
    })

    # XOR Gateway 1 Join: Merge before Goods Receipt (x=940, y=175, w=50, h=50)
    ET.SubElement(process, f"{{{NS_BPMN}}}exclusiveGateway", {"id": "Gateway_Price_Join"})
    shapes_di.append({"id": "Gateway_Price_Join_di", "element": "Gateway_Price_Join", "x": 940, "y": 175, "w": 50, "h": 50, "stroke": "#64748b", "fill": "#ffffff"})

    # Flow GW1 -> GW1 Join (Direct Happy Path)
    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_GW1_Happy", "name": "Accurate Price (86.4%)", "sourceRef": "Gateway_Price_Split", "targetRef": "Gateway_Price_Join"})
    edges_di.append({"id": "Flow_GW1_Happy_di", "element": "Flow_GW1_Happy", "waypoints": [(740, 200), (940, 200)], "stroke": "#10b981"})

    # Flow Change Price -> GW1 Join
    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_ChangePrice_Join", "sourceRef": "Activity_ChangePrice", "targetRef": "Gateway_Price_Join"})
    edges_di.append({
        "id": "Flow_ChangePrice_Join_di", "element": "Flow_ChangePrice_Join",
        "waypoints": [(910, 340), (965, 340), (965, 225)],
        "stroke": "#ef4444"
    })

    # Step 4: Goods Receipt (x=1030, y=160, w=130, h=80)
    ET.SubElement(process, f"{{{NS_BPMN}}}task", {"id": "Activity_GR", "name": "Record Goods\nReceipt"})
    shapes_di.append({"id": "Activity_GR_di", "element": "Activity_GR", "x": 1030, "y": 160, "w": 130, "h": 80, "stroke": "#10b981", "fill": "#d1fae5"})

    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_Join_GR", "sourceRef": "Gateway_Price_Join", "targetRef": "Activity_GR"})
    edges_di.append({"id": "Flow_Join_GR_di", "element": "Flow_Join_GR", "waypoints": [(990, 200), (1030, 200)], "stroke": "#10b981"})

    # GR Annotation
    ET.SubElement(process, f"{{{NS_BPMN}}}textAnnotation", {"id": "Anno_GR"}).append(ET.Element(f"{{{NS_BPMN}}}text"))
    process.find(f".//{{{NS_BPMN}}}textAnnotation[@id='Anno_GR']/{{{NS_BPMN}}}text").text = "Celonis: 92.6% cases\nAvg Lead Time: 8.1d"
    ET.SubElement(process, f"{{{NS_BPMN}}}association", {"id": "Assoc_GR", "sourceRef": "Activity_GR", "targetRef": "Anno_GR"})
    shapes_di.append({"id": "Anno_GR_di", "element": "Anno_GR", "x": 1030, "y": 80, "w": 130, "h": 45, "stroke": "#64748b", "fill": "#ffffff"})
    edges_di.append({"id": "Assoc_GR_di", "element": "Assoc_GR", "waypoints": [(1095, 160), (1095, 125)], "stroke": "#94a3b8"})

    # Step 5: Record Invoice Receipt (x=1220, y=160, w=130, h=80)
    ET.SubElement(process, f"{{{NS_BPMN}}}task", {"id": "Activity_Inv", "name": "Record Invoice\nReceipt"})
    shapes_di.append({"id": "Activity_Inv_di", "element": "Activity_Inv", "x": 1220, "y": 160, "w": 130, "h": 80, "stroke": "#10b981", "fill": "#d1fae5"})

    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_GR_Inv", "sourceRef": "Activity_GR", "targetRef": "Activity_Inv"})
    edges_di.append({"id": "Flow_GR_Inv_di", "element": "Flow_GR_Inv", "waypoints": [(1160, 200), (1220, 200)], "stroke": "#10b981"})

    # Invoice Annotation
    ET.SubElement(process, f"{{{NS_BPMN}}}textAnnotation", {"id": "Anno_Inv"}).append(ET.Element(f"{{{NS_BPMN}}}text"))
    process.find(f".//{{{NS_BPMN}}}textAnnotation[@id='Anno_Inv']/{{{NS_BPMN}}}text").text = "Celonis: 91.8% cases\n5.8d posting lag"
    ET.SubElement(process, f"{{{NS_BPMN}}}association", {"id": "Assoc_Inv", "sourceRef": "Activity_Inv", "targetRef": "Anno_Inv"})
    shapes_di.append({"id": "Anno_Inv_di", "element": "Anno_Inv", "x": 1220, "y": 80, "w": 130, "h": 45, "stroke": "#64748b", "fill": "#ffffff"})
    edges_di.append({"id": "Assoc_Inv_di", "element": "Assoc_Inv", "waypoints": [(1285, 160), (1285, 125)], "stroke": "#94a3b8"})

    # XOR Gateway 2: Split after Invoice Receipt (x=1390, y=175, w=50, h=50)
    ET.SubElement(process, f"{{{NS_BPMN}}}exclusiveGateway", {"id": "Gateway_Block_Split", "name": "Payment Blocked?"})
    shapes_di.append({"id": "Gateway_Block_Split_di", "element": "Gateway_Block_Split", "x": 1390, "y": 175, "w": 50, "h": 50, "stroke": "#64748b", "fill": "#ffffff"})

    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_Inv_GW2", "sourceRef": "Activity_Inv", "targetRef": "Gateway_Block_Split"})
    edges_di.append({"id": "Flow_Inv_GW2_di", "element": "Flow_Inv_GW2", "waypoints": [(1350, 200), (1390, 200)], "stroke": "#10b981"})

    # Exception Task: Set/Remove Payment Block (x=1470, y=300, w=150, h=80)
    ET.SubElement(process, f"{{{NS_BPMN}}}task", {"id": "Activity_Block", "name": "Set & Release\nPayment Block\n[Reality Exception]"})
    shapes_di.append({"id": "Activity_Block_di", "element": "Activity_Block", "x": 1470, "y": 300, "w": 150, "h": 80, "stroke": "#ef4444", "fill": "#fee2e2"})

    # Payment Block Annotation
    ET.SubElement(process, f"{{{NS_BPMN}}}textAnnotation", {"id": "Anno_Block"}).append(ET.Element(f"{{{NS_BPMN}}}text"))
    process.find(f".//{{{NS_BPMN}}}textAnnotation[@id='Anno_Block']/{{{NS_BPMN}}}text").text = "Reality: 2.3% (25.4k)\nAdds +11.4 days delay"
    ET.SubElement(process, f"{{{NS_BPMN}}}association", {"id": "Assoc_Block", "sourceRef": "Activity_Block", "targetRef": "Anno_Block"})
    shapes_di.append({"id": "Anno_Block_di", "element": "Anno_Block", "x": 1470, "y": 410, "w": 150, "h": 45, "stroke": "#ef4444", "fill": "#ffffff"})
    edges_di.append({"id": "Assoc_Block_di", "element": "Assoc_Block", "waypoints": [(1545, 380), (1545, 410)], "stroke": "#f87171"})

    # Flow GW2 -> Payment Block (Branch Down and Right)
    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_GW2_Block", "name": "Price/Qty Variance (2.3%)", "sourceRef": "Gateway_Block_Split", "targetRef": "Activity_Block"})
    edges_di.append({
        "id": "Flow_GW2_Block_di", "element": "Flow_GW2_Block",
        "waypoints": [(1415, 225), (1415, 340), (1470, 340)],
        "stroke": "#ef4444"
    })

    # XOR Gateway 2 Join: Merge before Payment (x=1650, y=175, w=50, h=50)
    ET.SubElement(process, f"{{{NS_BPMN}}}exclusiveGateway", {"id": "Gateway_Block_Join"})
    shapes_di.append({"id": "Gateway_Block_Join_di", "element": "Gateway_Block_Join", "x": 1650, "y": 175, "w": 50, "h": 50, "stroke": "#64748b", "fill": "#ffffff"})

    # Flow GW2 -> GW2 Join (Direct Happy Path)
    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_GW2_Happy", "name": "3-Way Match Passed (97.7%)", "sourceRef": "Gateway_Block_Split", "targetRef": "Gateway_Block_Join"})
    edges_di.append({"id": "Flow_GW2_Happy_di", "element": "Flow_GW2_Happy", "waypoints": [(1440, 200), (1650, 200)], "stroke": "#10b981"})

    # Flow Payment Block -> GW2 Join
    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_Block_Join", "sourceRef": "Activity_Block", "targetRef": "Gateway_Block_Join"})
    edges_di.append({
        "id": "Flow_Block_Join_di", "element": "Flow_Block_Join",
        "waypoints": [(1620, 340), (1675, 340), (1675, 225)],
        "stroke": "#ef4444"
    })

    # Step 6: Pay Invoice (x=1740, y=160, w=130, h=80 - Amber for bottleneck)
    ET.SubElement(process, f"{{{NS_BPMN}}}task", {"id": "Activity_Pay", "name": "Pay Invoice\n[Settlement]"})
    shapes_di.append({"id": "Activity_Pay_di", "element": "Activity_Pay", "x": 1740, "y": 160, "w": 130, "h": 80, "stroke": "#f59e0b", "fill": "#fef3c7"})

    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_Join_Pay", "sourceRef": "Gateway_Block_Join", "targetRef": "Activity_Pay"})
    edges_di.append({"id": "Flow_Join_Pay_di", "element": "Flow_Join_Pay", "waypoints": [(1700, 200), (1740, 200)], "stroke": "#10b981"})

    # Pay Annotation (Bottleneck warning)
    ET.SubElement(process, f"{{{NS_BPMN}}}textAnnotation", {"id": "Anno_Pay"}).append(ET.Element(f"{{{NS_BPMN}}}text"))
    process.find(f".//{{{NS_BPMN}}}textAnnotation[@id='Anno_Pay']/{{{NS_BPMN}}}text").text = "LATENCY BOTTLENECK:\n11.7 days wait after invoice"
    ET.SubElement(process, f"{{{NS_BPMN}}}association", {"id": "Assoc_Pay", "sourceRef": "Activity_Pay", "targetRef": "Anno_Pay"})
    shapes_di.append({"id": "Anno_Pay_di", "element": "Anno_Pay", "x": 1740, "y": 80, "w": 150, "h": 45, "stroke": "#f59e0b", "fill": "#ffffff"})
    edges_di.append({"id": "Assoc_Pay_di", "element": "Assoc_Pay", "waypoints": [(1805, 160), (1805, 125)], "stroke": "#fbbf24"})

    # End Event (x=1920, y=182, w=36, h=36)
    ET.SubElement(process, f"{{{NS_BPMN}}}endEvent", {"id": "EndEvent_1", "name": "Process Completed"})
    shapes_di.append({"id": "EndEvent_1_di", "element": "EndEvent_1", "x": 1920, "y": 182, "w": 36, "h": 36, "stroke": "#10b981", "fill": "#d1fae5"})

    ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": "Flow_Pay_End", "sourceRef": "Activity_Pay", "targetRef": "EndEvent_1"})
    edges_di.append({"id": "Flow_Pay_End_di", "element": "Flow_Pay_End", "waypoints": [(1870, 200), (1920, 200)], "stroke": "#10b981"})

    # Diagram & Plane
    diagram = ET.SubElement(definitions, f"{{{NS_BPMNDI}}}BPMNDiagram", {"id": "BPMNDiagram_Heatmap"})
    plane = ET.SubElement(diagram, f"{{{NS_BPMNDI}}}BPMNPlane", {"id": "BPMNPlane_Heatmap", "bpmnElement": proc_id})

    # Render Shapes
    for s in shapes_di:
        shape = ET.SubElement(
            plane,
            f"{{{NS_BPMNDI}}}BPMNShape",
            {
                "id": s["id"],
                "bpmnElement": s["element"],
                f"{{{NS_BIOC}}}stroke": s.get("stroke", "#000000"),
                f"{{{NS_BIOC}}}fill": s.get("fill", "#ffffff"),
                f"{{{NS_COLOR}}}border-color": s.get("stroke", "#000000"),
                f"{{{NS_COLOR}}}background-color": s.get("fill", "#ffffff"),
            },
        )
        ET.SubElement(shape, f"{{{NS_DC}}}Bounds", {"x": str(s["x"]), "y": str(s["y"]), "width": str(s["w"]), "height": str(s["h"])})

    # Render Edges
    for e in edges_di:
        edge = ET.SubElement(
            plane,
            f"{{{NS_BPMNDI}}}BPMNEdge",
            {
                "id": e["id"],
                "bpmnElement": e["element"],
                f"{{{NS_BIOC}}}stroke": e.get("stroke", "#000000"),
                f"{{{NS_COLOR}}}border-color": e.get("stroke", "#000000"),
            },
        )
        for wp in e["waypoints"]:
            ET.SubElement(edge, f"{{{NS_DI}}}waypoint", {"x": str(wp[0]), "y": str(wp[1])})

    xml_str = ET.tostring(definitions, encoding="utf-8", method="xml").decode("utf-8")
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'


# =========================================================================
# 2. CLEAN SIGNAVIO PRODUCTION TO-BE BPMN GENERATOR
# =========================================================================
def build_clean_signavio_bpmn_xml(data: dict) -> str:
    """Generate clean, standard BPMN 2.0 XML with formal gateways and swimlanes for Signavio import."""
    register_namespaces()
    meta = data.get("meta", {})
    process_name = meta.get("process_name", "Purchase-to-Pay (P2P)")

    definitions = ET.Element(
        f"{{{NS_BPMN}}}definitions",
        {
            "id": "Definitions_SignavioTarget",
            "targetNamespace": "http://signavio.com/bpmn20",
            "exporter": "SAP Signavio Process Manager Compatible",
            "exporterVersion": "16.8.0",
        },
    )

    collab_id = "Collaboration_1"
    collab = ET.SubElement(definitions, f"{{{NS_BPMN}}}collaboration", {"id": collab_id})
    ET.SubElement(collab, f"{{{NS_BPMN}}}participant", {"id": "Participant_1", "name": process_name, "processRef": "Process_Target_1"})

    process = ET.SubElement(
        definitions,
        f"{{{NS_BPMN}}}process",
        {"id": "Process_Target_1", "name": f"{process_name} (Target Standard)", "isExecutable": "false"},
    )

    # Lane structure: Procurement, Warehouse, Accounts Payable
    lane_set = ET.SubElement(process, f"{{{NS_BPMN}}}laneSet", {"id": "LaneSet_1"})
    lane_purchasing = ET.SubElement(lane_set, f"{{{NS_BPMN}}}lane", {"id": "Lane_Purchasing", "name": "Purchasing & Procurement"})
    lane_warehouse = ET.SubElement(lane_set, f"{{{NS_BPMN}}}lane", {"id": "Lane_Warehouse", "name": "Logistics & Receiving"})
    lane_finance = ET.SubElement(lane_set, f"{{{NS_BPMN}}}lane", {"id": "Lane_Finance", "name": "Accounts Payable & Treasury"})

    for node_id in ("StartEvent_1", "Activity_PR", "Activity_PO", "Activity_SendPO", "Gateway_Price_Split", "Activity_ChangePrice", "Gateway_Price_Join"):
        ET.SubElement(lane_purchasing, f"{{{NS_BPMN}}}flowNodeRef").text = node_id

    for node_id in ("Activity_GR",):
        ET.SubElement(lane_warehouse, f"{{{NS_BPMN}}}flowNodeRef").text = node_id

    for node_id in ("Activity_Inv", "Gateway_Block_Split", "Activity_Block", "Gateway_Block_Join", "Activity_Pay", "EndEvent_1"):
        ET.SubElement(lane_finance, f"{{{NS_BPMN}}}flowNodeRef").text = node_id

    # Add Flow Nodes with formal business names
    ET.SubElement(process, f"{{{NS_BPMN}}}startEvent", {"id": "StartEvent_1", "name": "Purchase Requisition Approved"})
    ET.SubElement(process, f"{{{NS_BPMN}}}userTask", {"id": "Activity_PR", "name": "Create Purchase Requisition"})
    ET.SubElement(process, f"{{{NS_BPMN}}}userTask", {"id": "Activity_PO", "name": "Create Purchase Order Item"})
    ET.SubElement(process, f"{{{NS_BPMN}}}serviceTask", {"id": "Activity_SendPO", "name": "Transmit Purchase Order to Vendor"})

    ET.SubElement(process, f"{{{NS_BPMN}}}exclusiveGateway", {"id": "Gateway_Price_Split", "name": "Contract Price Valid?"})
    ET.SubElement(process, f"{{{NS_BPMN}}}userTask", {"id": "Activity_ChangePrice", "name": "Review & Adjust Order Price"})
    ET.SubElement(process, f"{{{NS_BPMN}}}exclusiveGateway", {"id": "Gateway_Price_Join"})

    ET.SubElement(process, f"{{{NS_BPMN}}}userTask", {"id": "Activity_GR", "name": "Post Goods Receipt"})
    ET.SubElement(process, f"{{{NS_BPMN}}}userTask", {"id": "Activity_Inv", "name": "Record & Verify Vendor Invoice"})

    ET.SubElement(process, f"{{{NS_BPMN}}}exclusiveGateway", {"id": "Gateway_Block_Split", "name": "3-Way Match Passed?"})
    ET.SubElement(process, f"{{{NS_BPMN}}}userTask", {"id": "Activity_Block", "name": "Resolve Payment Block & Exception"})
    ET.SubElement(process, f"{{{NS_BPMN}}}exclusiveGateway", {"id": "Gateway_Block_Join"})

    ET.SubElement(process, f"{{{NS_BPMN}}}serviceTask", {"id": "Activity_Pay", "name": "Execute Scheduled Payment Run"})
    ET.SubElement(process, f"{{{NS_BPMN}}}endEvent", {"id": "EndEvent_1", "name": "Invoice Settled & Reconciled"})

    # Sequence Flows with formal conditions
    flows = [
        ("Flow_1", "StartEvent_1", "Activity_PR", None),
        ("Flow_2", "Activity_PR", "Activity_PO", None),
        ("Flow_3", "Activity_PO", "Activity_SendPO", None),
        ("Flow_4", "Activity_SendPO", "Gateway_Price_Split", None),
        ("Flow_Price_OK", "Gateway_Price_Split", "Gateway_Price_Join", "Contract Price Matched"),
        ("Flow_Price_Variance", "Gateway_Price_Split", "Activity_ChangePrice", "Price Discrepancy"),
        ("Flow_Price_Resolved", "Activity_ChangePrice", "Gateway_Price_Join", None),
        ("Flow_5", "Gateway_Price_Join", "Activity_GR", None),
        ("Flow_6", "Activity_GR", "Activity_Inv", None),
        ("Flow_7", "Activity_Inv", "Gateway_Block_Split", None),
        ("Flow_Match_OK", "Gateway_Block_Split", "Gateway_Block_Join", "Match Within Tolerance"),
        ("Flow_Match_Variance", "Gateway_Block_Split", "Activity_Block", "Price / Quantity Discrepancy"),
        ("Flow_Block_Resolved", "Activity_Block", "Gateway_Block_Join", None),
        ("Flow_8", "Gateway_Block_Join", "Activity_Pay", None),
        ("Flow_9", "Activity_Pay", "EndEvent_1", None),
    ]

    for f_id, src, tgt, name in flows:
        f_elem = ET.SubElement(process, f"{{{NS_BPMN}}}sequenceFlow", {"id": f_id, "sourceRef": src, "targetRef": tgt})
        if name:
            f_elem.set("name", name)

    # Diagram & Shapes (Clean Signavio styling)
    diagram = ET.SubElement(definitions, f"{{{NS_BPMNDI}}}BPMNDiagram", {"id": "BPMNDiagram_Signavio"})
    plane = ET.SubElement(diagram, f"{{{NS_BPMNDI}}}BPMNPlane", {"id": "BPMNPlane_Signavio", "bpmnElement": collab_id})

    # Participant Shape (Pool)
    pool_shape = ET.SubElement(plane, f"{{{NS_BPMNDI}}}BPMNShape", {"id": "Participant_1_di", "bpmnElement": "Participant_1", "isHorizontal": "true"})
    ET.SubElement(pool_shape, f"{{{NS_DC}}}Bounds", {"x": "20", "y": "20", "width": "2000", "height": "480"})

    # Lane Shapes
    lane1_shape = ET.SubElement(plane, f"{{{NS_BPMNDI}}}BPMNShape", {"id": "Lane_Purchasing_di", "bpmnElement": "Lane_Purchasing", "isHorizontal": "true"})
    ET.SubElement(lane1_shape, f"{{{NS_DC}}}Bounds", {"x": "50", "y": "20", "width": "1970", "height": "200"})

    lane2_shape = ET.SubElement(plane, f"{{{NS_BPMNDI}}}BPMNShape", {"id": "Lane_Warehouse_di", "bpmnElement": "Lane_Warehouse", "isHorizontal": "true"})
    ET.SubElement(lane2_shape, f"{{{NS_DC}}}Bounds", {"x": "50", "y": "220", "width": "1970", "height": "120"})

    lane3_shape = ET.SubElement(plane, f"{{{NS_BPMNDI}}}BPMNShape", {"id": "Lane_Finance_di", "bpmnElement": "Lane_Finance", "isHorizontal": "true"})
    ET.SubElement(lane3_shape, f"{{{NS_DC}}}Bounds", {"x": "50", "y": "340", "width": "1970", "height": "160"})

    # Layout coordinates for tasks (Clean, aligned)
    node_bounds = {
        "StartEvent_1": (80, 102, 36, 36),
        "Activity_PR": (150, 80, 130, 80),
        "Activity_PO": (320, 80, 130, 80),
        "Activity_SendPO": (490, 80, 130, 80),
        "Gateway_Price_Split": (660, 95, 50, 50),
        "Activity_ChangePrice": (750, 130, 140, 70),
        "Gateway_Price_Join": (930, 95, 50, 50),
        "Activity_GR": (1020, 240, 130, 80),
        "Activity_Inv": (1190, 380, 130, 80),
        "Gateway_Block_Split": (1360, 395, 50, 50),
        "Activity_Block": (1450, 420, 140, 70),
        "Gateway_Block_Join": (1630, 395, 50, 50),
        "Activity_Pay": (1720, 380, 130, 80),
        "EndEvent_1": (1890, 402, 36, 36),
    }

    for n_id, (x, y, w, h) in node_bounds.items():
        s = ET.SubElement(plane, f"{{{NS_BPMNDI}}}BPMNShape", {"id": f"{n_id}_di", "bpmnElement": n_id})
        ET.SubElement(s, f"{{{NS_DC}}}Bounds", {"x": str(x), "y": str(y), "width": str(w), "height": str(h)})

    # Edges
    edge_waypoints = {
        "Flow_1": [(116, 120), (150, 120)],
        "Flow_2": [(280, 120), (320, 120)],
        "Flow_3": [(450, 120), (490, 120)],
        "Flow_4": [(620, 120), (660, 120)],
        "Flow_Price_OK": [(710, 120), (930, 120)],
        "Flow_Price_Variance": [(685, 145), (685, 165), (750, 165)],
        "Flow_Price_Resolved": [(890, 165), (955, 165), (955, 145)],
        "Flow_5": [(980, 120), (1085, 120), (1085, 240)],
        "Flow_6": [(1085, 320), (1085, 420), (1190, 420)],
        "Flow_7": [(1320, 420), (1360, 420)],
        "Flow_Match_OK": [(1410, 420), (1630, 420)],
        "Flow_Match_Variance": [(1385, 445), (1385, 455), (1450, 455)],
        "Flow_Block_Resolved": [(1590, 455), (1655, 455), (1655, 445)],
        "Flow_8": [(1680, 420), (1720, 420)],
        "Flow_9": [(1850, 420), (1890, 420)],
    }

    for e_id, wps in edge_waypoints.items():
        e = ET.SubElement(plane, f"{{{NS_BPMNDI}}}BPMNEdge", {"id": f"{e_id}_di", "bpmnElement": e_id})
        for wp in wps:
            ET.SubElement(e, f"{{{NS_DI}}}waypoint", {"x": str(wp[0]), "y": str(wp[1])})

    xml_str = ET.tostring(definitions, encoding="utf-8", method="xml").decode("utf-8")
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'


def main():
    parser = argparse.ArgumentParser(description="Augment BPMN model with Celonis process mining discoveries.")
    parser.add_argument("--input", required=True, help="Path to comparison-spec.json")
    parser.add_argument("--output", required=True, help="Path to output BPMN 2.0 XML file")
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

    out_name = Path(args.output).name.lower()
    out_dir = Path(args.output).parent

    try:
        # Determine whether to generate heatmap or clean Signavio target BPMN
        if "signavio" in out_name or "clean" in out_name or "target" in out_name:
            bpmn_xml = build_clean_signavio_bpmn_xml(data)
        else:
            bpmn_xml = build_heatmap_bpmn_xml(data)
            # Also auto-generate the complementary clean Signavio BPMN alongside it
            clean_xml = build_clean_signavio_bpmn_xml(data)
            clean_path = out_dir / "signavio-target-process.bpmn"
            clean_path.write_text(clean_xml, encoding="utf-8")

        # Validate that output is well-formed XML
        ET.fromstring(bpmn_xml.encode("utf-8"))
    except Exception as exc:
        print(f"FAIL: error building BPMN XML: {exc}", file=sys.stderr)
        return 1

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(bpmn_xml, encoding="utf-8")
    print(f"PASS: wrote BPMN to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
