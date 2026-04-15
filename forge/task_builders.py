
from __future__ import annotations
import random
from typing import Dict, Iterable, List, Sequence, Tuple
from .graph_utils import build_adj, reachable_from
from .schema import TaskExample, WorkflowInstance


def build_t_sad_tasks(workflows: Sequence[WorkflowInstance], negatives_per_positive: int = 1, seed: int = 13) -> List[TaskExample]:
    rng = random.Random(seed)
    examples: List[TaskExample] = []
    for wf in workflows:
        for idx, path in enumerate(wf.paths):
            if len(path) < 2:
                continue
            examples.append(TaskExample(
                task='t_sad',
                workflow_id=wf.instance_id,
                input={'sequence': path},
                target=1,
                meta={'source': 'gold_path', 'path_index': idx},
            ))
            made = 0
            attempts = 0
            while made < negatives_per_positive and attempts < 10:
                attempts += 1
                neg = list(path)
                mode = rng.choice(['swap', 'drop', 'splice'])
                if mode == 'swap' and len(neg) >= 3:
                    i = rng.randrange(len(neg) - 1)
                    neg[i], neg[i+1] = neg[i+1], neg[i]
                elif mode == 'drop' and len(neg) >= 3:
                    del neg[rng.randrange(1, len(neg)-1)]
                elif mode == 'splice' and len(wf.nodes) >= 2:
                    pos = rng.randrange(1, len(neg))
                    candidate = rng.choice([n.id for n in wf.nodes])
                    if candidate not in neg:
                        neg.insert(pos, candidate)
                if neg != path:
                    examples.append(TaskExample(
                        task='t_sad',
                        workflow_id=wf.instance_id,
                        input={'sequence': neg},
                        target=0,
                        meta={'source': mode, 'path_index': idx},
                    ))
                    made += 1
    return examples


def build_a_sad_tasks(workflows: Sequence[WorkflowInstance]) -> List[TaskExample]:
    examples: List[TaskExample] = []
    for wf in workflows:
        adj = build_adj(wf.edges)
        node_ids = [n.id for n in wf.nodes]
        reach = {nid: reachable_from(nid, adj) for nid in node_ids}
        for a in node_ids:
            for b in node_ids:
                if a == b:
                    continue
                label = 1 if b in (reach.get(a) or set()) else 0
                examples.append(TaskExample(
                    task='a_sad',
                    workflow_id=wf.instance_id,
                    input={'step_a': a, 'step_b': b},
                    target=label,
                    meta={},
                ))
    return examples


def build_s_nap_tasks(workflows: Sequence[WorkflowInstance]) -> List[TaskExample]:
    examples: List[TaskExample] = []
    for wf in workflows:
        for path_idx, path in enumerate(wf.paths):
            for cut in range(1, len(path)):
                prefix = path[:cut]
                nxt = path[cut]
                examples.append(TaskExample(
                    task='s_nap',
                    workflow_id=wf.instance_id,
                    input={'prefix': prefix},
                    target=nxt,
                    meta={'path_index': path_idx, 'cut': cut},
                ))
    return examples
