
from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from forge.loader import load_workflows_from_csv
from forge.task_builders import build_t_sad_tasks, build_a_sad_tasks, build_s_nap_tasks


def dump_jsonl(path, rows):
    with open(path, 'w', encoding='utf-8') as f:
        for i, row in enumerate(rows):
            obj = row.to_dict() if hasattr(row, 'to_dict') else dict(row)
            if 'id' not in obj:
                obj['id'] = i
            f.write(json.dumps(obj, ensure_ascii=False) + '
')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    workflows = load_workflows_from_csv(args.csv)
    dump_jsonl(os.path.join(args.out, 'workflows.jsonl'), workflows)
    dump_jsonl(os.path.join(args.out, 't_sad.jsonl'), build_t_sad_tasks(workflows))
    dump_jsonl(os.path.join(args.out, 'a_sad.jsonl'), build_a_sad_tasks(workflows))
    dump_jsonl(os.path.join(args.out, 's_nap.jsonl'), build_s_nap_tasks(workflows))
    print(f'Built {len(workflows)} workflows into {args.out}')


if __name__ == '__main__':
    main()
