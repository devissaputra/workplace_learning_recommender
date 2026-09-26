# Calculation guide

## Question and evidence

Which feasible resource best addresses a confirmed gap?

Supplied competency needs, work context and resource metadata.

**Status:** SYNTHETIC / RULE-BASED PROTOTYPE | no educational validity claim.

## Design

Apply hard eligibility filters; score eligible resources with exposed components; select for coverage and inspect weight sensitivity.

## Calculation and interpretation

`Resource score = sum(normalized weight × component score).`

Language, time and prerequisites are filters, not compensable preferences. Scores encode policy weights and supplied quality ratings; high rank is not evidence of a resource’s causal effect on performance.

## Evidence table

Worked example — illustrative, not a measured research result. Full precision below is for traceability, not a claim of measurement precision.

| Quantity | Value | Unit / meaning | JSON path |
|---|---:|---|---|
| weighted score: .6×.8 + .4×.5 | 0.6799999999999999 | unitless | `outputs.weighted score: .6×.8 + .4×.5` |
| gap coverage: current 2 to 3 of target 4 | 0.5 | unitless | `outputs.gap coverage: current 2 to 3 of target 4` |

Source: [results/review_examples.json](results/review_examples.json). Values resolve directly from this file when figures are regenerated.

This workplace-learning recommender filters resources for feasibility before ranking them against confirmed competency gaps and work context. It exposes contributions from need priority, gap coverage, task fit, quality, effort, and other declared factors, then checks coverage and sensitivity to weights. The output is a reasoned recommendation based on supplied metadata, not a validated estimate of learning impact.

## Verification performed in this review

34 existing unittest checks passed. The bundled demonstration executed successfully in this review.

The figure-generation check verifies agreement between the selected source values and SVGs. It does not validate the raw dataset, fitted model, identification assumptions, or external generalization.

```bash
python scripts/build_review_figures.py
python scripts/build_review_figures.py --check
```

For the explicitly illustrative example:

```bash
python scripts/review_examples.py
```

## Implementation map

Follow these functions to inspect each transformation. Validation helpers and private functions remain visible in the linked modules.

| Function | Purpose / documented behavior |
|---|---|
| [`load_json`](scripts/run_demo.py#L16) | Inspect the explicit implementation and its callers. |
| [`validate_scale`](src/workplace_learning_recommender/core.py#L76) | Inspect the explicit implementation and its callers. |
| [`validate_needs`](src/workplace_learning_recommender/core.py#L102) | Validate evidence-backed development needs. |
| [`validate_context`](src/workplace_learning_recommender/core.py#L200) | Inspect the explicit implementation and its callers. |
| [`validate_resources`](src/workplace_learning_recommender/core.py#L259) | Inspect the explicit implementation and its callers. |
| [`validate_weights`](src/workplace_learning_recommender/core.py#L391) | Inspect the explicit implementation and its callers. |
| [`eligibility_report`](src/workplace_learning_recommender/core.py#L463) | Return eligible resources and explicit exclusion reasons. |
| [`score_resources`](src/workplace_learning_recommender/core.py#L598) | Score only resources that pass hard eligibility checks. |
| [`select_with_coverage`](src/workplace_learning_recommender/core.py#L673) | Greedy reranker that gives distinct confirmed gaps a fair chance to appear. |
| [`explanation`](src/workplace_learning_recommender/core.py#L716) | Return a plain-language explanation grounded in actual score components. |
| [`recommendation_diagnostics`](src/workplace_learning_recommender/core.py#L740) | Inspect the explicit implementation and its callers. |
| [`recommend`](src/workplace_learning_recommender/core.py#L772) | Return explainable, coverage-aware workplace learning recommendations. |
| [`ranking_sensitivity`](src/workplace_learning_recommender/core.py#L813) | Compare recommendation order under alternative transparent weight sets. |

## What remains before a stronger research claim

Language, time and prerequisites are filters, not compensable preferences. Scores encode policy weights and supplied quality ratings; high rank is not evidence of a resource’s causal effect on performance. A successful software test is not validation of a scientific construct. New experiments should state their split unit, comparator, outcome, uncertainty procedure and failure criteria before examining final test results.
