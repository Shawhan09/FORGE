
from __future__ import annotations
import argparse, json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from forge.graph_utils import validate_executability
from forge.evaluators import load_jsonl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', required=True)
    ap.add_argument('--wid', required=True)
    args = ap.parse_args()
    rows = load_jsonl(args.data)
    row = next((r for r in rows if str(r['instance_id']) == str(args.wid)), None)
    if row is None:
        raise SystemExit('workflow not found')
    print(json.dumps(row, ensure_ascii=False, indent=2))
    node_ids = [n['id'] for n in row['nodes']]
    report = validate_executability(node_ids, row['paths'], row['edges'])
    print('
Executability report:')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
