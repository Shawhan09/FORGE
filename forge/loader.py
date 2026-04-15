
from __future__ import annotations
import ast
import json
from typing import Any, Dict, List, Optional
import pandas as pd
from .graph_utils import edges_from_paths, start_end_nodes
from .schema import Hierarchy, WorkNode, WorkflowInstance, WorkflowSemantics


def _parse_json_like(value: Any):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, (dict, list)):
        return value
    s = str(value).strip()
    if not s:
        return None
    for parser in (json.loads, ast.literal_eval):
        try:
            return parser(s)
        except Exception:
            pass
    return None


def _extract_nodes(row: pd.Series) -> List[WorkNode]:
    nodes = []
    idx = 1
    while True:
        key_id = f'node_{idx:02d}_id'
        key_name = f'node_{idx:02d}_name'
        key_desc = f'node_{idx:02d}_desc'
        if key_id not in row.index:
            break
        nid = row.get(key_id)
        name = row.get(key_name)
        desc = row.get(key_desc)
        if pd.notna(nid) and str(nid).strip():
            nodes.append(WorkNode(id=str(nid).strip(), name='' if pd.isna(name) else str(name), desc='' if pd.isna(desc) else str(desc)))
        idx += 1
    return nodes


def _extract_semantics(labels_json: Any, canonical_ids: List[str]) -> tuple[WorkflowSemantics, Dict[str, str]]:
    data = _parse_json_like(labels_json) or []
    sem = WorkflowSemantics()
    alias_map: Dict[str, str] = {}
    if not isinstance(data, list):
        return sem, alias_map
    fallback = {f'w1_n{i+1}': nid for i, nid in enumerate(canonical_ids)}
    for item in data:
        if not isinstance(item, dict):
            sem.other.append({'raw': item})
            continue
        applies = item.get('applies_to', {}) or {}
        for k in applies.get('node_ids', []) or []:
            if k in fallback:
                alias_map[k] = fallback[k]
        label_type = str(item.get('label_type', item.get('type', 'other'))).lower()
        if 'branch' in label_type:
            sem.branch_conditions.append(item)
        elif 'order' in label_type or 'preced' in label_type:
            sem.ordering_semantics.append(item)
        elif 'uncertain' in label_type:
            sem.uncertainty_notes.append(item)
        elif 'scope' in label_type or 'applic' in label_type:
            sem.scope_notes.append(item)
        elif 'ref' in label_type or 'source' in label_type:
            sem.references.append(item)
        else:
            sem.other.append(item)
    return sem, alias_map


def load_workflows_from_csv(csv_path: str) -> List[WorkflowInstance]:
    df = pd.read_csv(csv_path)
    workflows: List[WorkflowInstance] = []
    for _, row in df.iterrows():
        nodes = _extract_nodes(row)
        node_ids = [n.id for n in nodes]
        paths = _parse_json_like(row.get('paths_json')) or []
        cleaned_paths = []
        for p in paths:
            if not isinstance(p, list):
                continue
            cp = []
            for nid in p:
                nid = str(nid)
                cp.append(nid)
            if cp:
                cleaned_paths.append(cp)
        edges = edges_from_paths(cleaned_paths)
        starts, ends = start_end_nodes(node_ids, edges)
        sem, alias_map = _extract_semantics(row.get('labels_json'), node_ids)
        wid = str(row.get('workflow_id', row.get('workflow_index', row.get('workflow_name', 'unknown'))))
        inst = WorkflowInstance(
            instance_id=wid,
            source_pdf=None if pd.isna(row.get('pdf_name')) else str(row.get('pdf_name')),
            hierarchy=Hierarchy(
                domain=None if pd.isna(row.get('domain')) else str(row.get('domain')),
                subdomain=None if pd.isna(row.get('subdomain')) else str(row.get('subdomain')),
                topic=None if pd.isna(row.get('topic_name')) else str(row.get('topic_name')),
                workflow_id=wid,
                workflow_name=None if pd.isna(row.get('workflow_name')) else str(row.get('workflow_name')),
            ),
            nodes=nodes,
            paths=cleaned_paths,
            edges=edges,
            start_nodes=starts,
            end_nodes=ends,
            workflow_semantics=sem,
            node_id_alias_map=alias_map,
            parse_error=None if pd.isna(row.get('parse_error')) else str(row.get('parse_error')),
        )
        workflows.append(inst)
    return workflows
