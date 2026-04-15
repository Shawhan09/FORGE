
from __future__ import annotations
import json
from typing import Any, Dict, Iterable, List, Sequence


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def accuracy(golds: Sequence[Any], preds: Sequence[Any]) -> float:
    if not golds:
        return 0.0
    return sum(int(g == p) for g, p in zip(golds, preds)) / len(golds)


def evaluate_task_examples(task_rows: List[Dict[str, Any]], pred_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    pred_map = {str(r['id']): r['prediction'] for r in pred_rows}
    golds, preds = [], []
    missing = 0
    task_name = task_rows[0]['task'] if task_rows else 'unknown'
    for row in task_rows:
        rid = str(row['id'])
        if rid not in pred_map:
            missing += 1
            continue
        golds.append(row['target'])
        preds.append(pred_map[rid])
    return {
        'task': task_name,
        'num_examples': len(task_rows),
        'num_scored': len(golds),
        'missing_predictions': missing,
        'accuracy': accuracy(golds, preds),
    }
