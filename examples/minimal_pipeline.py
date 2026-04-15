
from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

print('Minimal pipeline placeholder:')
print('1. Build tasks with scripts/build_tasks.py')
print('2. Inspect workflows with scripts/inspect_instance.py')
print('3. Evaluate model predictions with scripts/evaluate_predictions.py')
print('Supported tasks: T-SAD, A-SAD, S-NAP')
