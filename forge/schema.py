
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

@dataclass
class Hierarchy:
    root: str = "FORGE"
    domain: Optional[str] = None
    subdomain: Optional[str] = None
    topic: Optional[str] = None
    workflow_id: Optional[str] = None
    workflow_name: Optional[str] = None

@dataclass
class WorkNode:
    id: str
    name: str
    desc: str = ""

@dataclass
class WorkflowSemantics:
    branch_conditions: List[Dict[str, Any]] = field(default_factory=list)
    ordering_semantics: List[Dict[str, Any]] = field(default_factory=list)
    uncertainty_notes: List[Dict[str, Any]] = field(default_factory=list)
    scope_notes: List[Dict[str, Any]] = field(default_factory=list)
    references: List[Dict[str, Any]] = field(default_factory=list)
    other: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class WorkflowInstance:
    instance_id: str
    source_pdf: Optional[str]
    hierarchy: Hierarchy
    nodes: List[WorkNode]
    paths: List[List[str]]
    edges: List[List[str]]
    start_nodes: List[str]
    end_nodes: List[str]
    workflow_semantics: WorkflowSemantics
    node_id_alias_map: Dict[str, str] = field(default_factory=dict)
    parse_error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class TaskExample:
    task: str
    workflow_id: str
    input: Dict[str, Any]
    target: Any
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
