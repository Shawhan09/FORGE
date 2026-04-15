# FORGE Benchmark SDK

This repository exposes FORGE as an evaluation-ready workflow benchmark.
It supports exactly three reasoning tasks released in the paper:

- T-SAD: Trace-level Semantic Anomaly Detection
- A-SAD: Activity-order Semantic Anomaly Detection
- S-NAP: Semantic Next Activity Prediction

It does **not** generate HRA or suffix-prediction task files.

## Repository structure

- `forge/schema.py`: canonical benchmark data classes
- `forge/loader.py`: load the CSV release into workflow instances
- `forge/graph_utils.py`: executable-graph utilities and validation
- `forge/task_builders.py`: build T-SAD / A-SAD / S-NAP task instances
- `forge/evaluators.py`: evaluation helpers for the three tasks
- `scripts/build_tasks.py`: command-line task builder
- `scripts/inspect_instance.py`: inspect one workflow instance
- `scripts/evaluate_predictions.py`: score prediction files
- `examples/minimal_pipeline.py`: minimal runnable example

## Installation

```bash
pip install -r requirements.txt
```

## Build task files

```bash
python scripts/build_tasks.py --csv dataset.csv --out data/
```

This produces:

- `workflows.jsonl`
- `t_sad.jsonl`
- `a_sad.jsonl`
- `s_nap.jsonl`

## Inspect one instance

```bash
python scripts/inspect_instance.py --data data/workflows.jsonl --wid your_workflow_id
```

## Evaluate predictions

```bash
python scripts/evaluate_predictions.py --task data/t_sad.jsonl --pred preds.jsonl
```
