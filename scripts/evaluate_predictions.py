
from __future__ import annotations
import argparse, json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from forge.evaluators import load_jsonl, evaluate_task_examples


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--task', required=True)
    ap.add_argument('--pred', required=True)
    args = ap.parse_args()
    task_rows = load_jsonl(args.task)
    pred_rows = load_jsonl(args.pred)
    print(json.dumps(evaluate_task_examples(task_rows, pred_rows), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
