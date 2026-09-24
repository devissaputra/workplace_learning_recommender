# Workplace Learning Recommender

> Gap weighted resource ranking baseline with quality, difficulty, recency, and plain language explanation signals.

[![CI](https://github.com/devissaputra/workplace-learning-recommender/actions/workflows/ci.yml/badge.svg)](https://github.com/devissaputra/workplace-learning-recommender/actions/workflows/ci.yml)

![Workplace Learning Recommender workflow](assets/architecture.svg)

**Area:** Workplace Learning & Capability Development    
**Status:** working research prototype  
**Author:** Devis Wawan Saputra

## What this project is for

Workplace learning recommendations should respond to the skills a person needs next, not simply repeat popular courses. This prototype ranks resources against skill gaps and quality signals while keeping the reason for each recommendation visible.

**Who may find it useful:** L&D teams and researchers studying explainable recommendation for workplace learning.

## Research questions

1. Can recommendations balance skill fit, difficulty, modality, and recency?
2. How can recommendations avoid repeatedly steering users toward already-strong skills?
3. What explanations make recommendations useful to learners and managers?

## How it works

Each resource receives a transparent score from the current skill gap, resource quality, difficulty mismatch, and a small recency penalty. Results are sorted deterministically, and a separate function explains which skill gap motivated a recommendation.

![Workplace Learning Recommender data and reasoning flow](assets/data_flow.svg)

Role and task context define a skill need, resources are scored against that need, and the ranked result can be inspected before it is shown to a learner. Diversity optimization is not implemented in the current baseline.

![Synthetic demo snapshot for Workplace Learning Recommender](assets/demo_snapshot.svg)

This snapshot shows the bundled synthetic example for Workplace Learning Recommender. It checks the software path; it is not an empirical performance result.

## Methods in the current baseline

- skill gap weighting
- resource quality term
- difficulty mismatch penalty
- recency penalty
- deterministic ranking explanation

## Data

Synthetic employee profiles and learning-resource metadata are included.

`data/README.md` documents the sample schema and the conditions that should be recorded before any real dataset is connected. Restricted or identifiable learner data should stay outside the repository.

## Run the demo

```bash
git clone https://github.com/devissaputra/workplace-learning-recommender.git
cd workplace-learning-recommender
python scripts/run_demo.py
python -m unittest discover -s tests -v
```

The demo ranks two resources for different skills. The larger Python gap puts the Python practice resource first even though both resources have the same quality score.

## What to evaluate next

The next version should add a meaningful diversity or coverage objective and test recommendations against real task contexts. Offline ranking metrics are not enough; users should be able to judge relevance and reject poor suggestions.

## Evaluation view

![Workplace Learning Recommender evaluation dashboard](assets/evaluation_dashboard.svg)

The Workplace Learning Recommender dashboard is an evaluation checklist rather than a result chart. The bars are illustrative only; the labels show the evidence a real study would need to collect.

## Limits and responsible use

The score depends on externally supplied skill gaps and resource metadata. It does not infer employee capability, predict job performance, or learn preferences from hidden behavioral tracking. See `docs/ethics_and_risks.md` for the broader risk review.

## Repository map

```text
.
├── .github/workflows/ci.yml
├── assets/
│   ├── architecture.svg
│   ├── data_flow.svg
│   ├── demo_snapshot.svg
│   └── evaluation_dashboard.svg
├── data/
│   ├── README.md
│   └── sample.csv
├── docs/
│   ├── ethics_and_risks.md
│   ├── related_work.md
│   └── research_protocol.md
├── reports/model_card.md
├── scripts/run_demo.py
├── src/workplace_learning_recommender/core.py
├── tests/test_core.py
├── CITATION.cff
├── LICENSE
├── pyproject.toml
└── README.md
```

## Research path

A credible next version would:

1. build a small resource catalog with reviewed skill and difficulty metadata
2. compare the ranking with simple gap only and popularity baselines
3. measure task relevance, coverage, and user rejection reasons

## Related work

`docs/related_work.md` points to open projects that are relevant to this problem area. They are context for comparison and study design; this repository does not present their code as its own.

## Citation and license

`CITATION.cff` contains the software citation. The code and original SVG visuals use the MIT License. Any external dataset keeps its own license and usage conditions.
