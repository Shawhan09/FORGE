
from __future__ import annotations
from collections import defaultdict, deque
from typing import Dict, Iterable, List, Sequence, Set, Tuple


def edges_from_paths(paths: Sequence[Sequence[str]]) -> List[List[str]]:
    seen = set()
    out = []
    for path in paths:
        for a, b in zip(path, path[1:]):
            if a and b and (a, b) not in seen:
                seen.add((a, b))
                out.append([a, b])
    return out


def build_adj(edges: Iterable[Sequence[str]]) -> Dict[str, List[str]]:
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
    return dict(adj)


def build_rev_adj(edges: Iterable[Sequence[str]]) -> Dict[str, List[str]]:
    radj = defaultdict(list)
    for a, b in edges:
        radj[b].append(a)
    return dict(radj)


def start_end_nodes(node_ids: Sequence[str], edges: Sequence[Sequence[str]]) -> Tuple[List[str], List[str]]:
    indeg = {n: 0 for n in node_ids}
    outdeg = {n: 0 for n in node_ids}
    for a, b in edges:
        if a in outdeg:
            outdeg[a] += 1
        if b in indeg:
            indeg[b] += 1
    starts = [n for n in node_ids if indeg[n] == 0]
    ends = [n for n in node_ids if outdeg[n] == 0]
    return starts, ends


def is_valid_path(path: Sequence[str], edge_set: Set[Tuple[str, str]]) -> bool:
    if not path:
        return False
    return all((a, b) in edge_set for a, b in zip(path, path[1:]))


def reachable_from(source: str, adj: Dict[str, List[str]]) -> Set[str]:
    seen = {source}
    q = deque([source])
    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return seen


def validate_executability(node_ids: Sequence[str], paths: Sequence[Sequence[str]], edges: Sequence[Sequence[str]]) -> Dict[str, object]:
    node_set = set(node_ids)
    edge_set = {(a, b) for a, b in edges}
    bad_paths = [list(p) for p in paths if not set(p).issubset(node_set) or not is_valid_path(p, edge_set)]
    covered = set()
    for p in paths:
        covered.update(p)
    uncovered = sorted(node_set - covered)
    return {
        'num_nodes': len(node_ids),
        'num_edges': len(edges),
        'num_paths': len(paths),
        'bad_paths': bad_paths,
        'uncovered_nodes': uncovered,
        'is_executable': len(paths) > 0 and len(bad_paths) == 0,
    }
