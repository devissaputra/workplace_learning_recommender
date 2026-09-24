# Research protocol

## Project

Workplace Learning Recommender

## Questions

1. Can recommendations balance skill fit, difficulty, modality, and recency?
2. How can recommendations avoid repeatedly steering users toward already-strong skills?
3. What explanations make recommendations useful to learners and managers?

## Baseline methods

- skill gap weighting
- resource quality term
- difficulty mismatch penalty
- recency penalty
- deterministic ranking explanation

## Evidence to collect

Start from the current transparent baseline and record every transformation needed to produce a ranked list of resources and a short explanation tied to the target skill gap. Keep a clear boundary between synthetic demonstration data and any future empirical dataset.

## Validation

Evaluate ranking relevance against expert or user judgments, compare with simple baselines, and report coverage across skills and resources. If personalization is added, include consent and preference controls.

## What counts as a useful result

The next version should add a meaningful diversity or coverage objective and test recommendations against real task contexts. Offline ranking metrics are not enough; users should be able to judge relevance and reject poor suggestions.

## Threats to validity

Poor skill labels, stale resource metadata, popularity bias, inferred preferences, and narrow catalogs can make recommendations repetitive or irrelevant.
