# Data documentation

## Included data

All files in this folder are synthetic demonstration inputs.

- `needs.json` contains evidence-backed development needs and the declared proficiency scale.
- `context.json` contains the workplace-learning request context and constraints.
- `resources.json` contains the structured learning-resource catalog.
- `sample.csv` is a compact tabular view of the synthetic resource catalog.

No employee or learner records are included.

## Development needs

The recommender expects upstream competency evidence to distinguish:

- confirmed gap
- target met
- target exceeded
- unknown evidence
- insufficient evidence

Only **confirmed gaps with sufficient confidence** are eligible for recommendation ranking.

Missing evidence is never converted into a zero skill level.

The synthetic need record contains:

- current level
- target level
- gap
- priority
- confidence
- status

This structure is intentionally compatible with the output concepts used in the separate `competency_gap_intelligence` project, although the repositories do not depend on one another.

## Request context

The synthetic context contains:

- role label
- role tags
- current task tags
- learning-goal tags
- preferred modalities
- language
- available hours
- completed resources
- recent resource exposures
- explicit `as_of` date for reproducible freshness calculations

Context is supplied deliberately. The baseline does not infer role, goals, preferences, or interests from hidden behavioral tracking.

## Resource catalog

Each resource declares:

- id
- title
- one or more target skills
- entry level
- target level
- quality
- quality source
- modality
- effort hours
- competency prerequisites
- task tags
- role tags
- goal tags
- language
- availability
- last-updated date

Resource metadata are claims that require governance.

A quality value should have a documented source, such as expert review, validated learner feedback, outcome evidence, or another defensible procedure.

## Eligibility versus ranking

Hard constraints are checked before scoring.

A resource is excluded when, for example:

- it is unavailable
- it was already completed
- its language is incompatible
- it exceeds the available time budget
- no confirmed development need matches its skill
- the learner does not meet the entry level
- a prerequisite is not met

Only resources that pass those checks are scored.

## Exposure and freshness are different

The repository keeps two concepts separate:

- **resource freshness** comes from `last_updated`
- **novelty / repetition** comes from `recent_exposures`, expressed as days since the learner last saw that resource

A resource updated recently is not necessarily novel to a learner, and a resource never seen before is not necessarily current.

## Proficiency scale

Entry levels, target levels, and competency levels must use the same declared scale for one recommendation request.

The demo uses a synthetic 0–5 scale only for illustration.

A production adapter should preserve the semantics of the source competency framework.

## Before connecting real data

Document:

- competency framework and scale
- source of development needs
- evidence-confidence policy
- role/task/goal collection method
- whether preferences are volunteered or inferred
- resource metadata governance
- quality-rating method
- availability updates
- prerequisite validation
- completed-resource history
- retention period for learning history
- correction and appeal mechanisms

## Do not commit

Do not commit identifiable employee profiles, private performance records, confidential work samples, manager notes, disability or health information, compensation data, raw browsing histories, private course histories, or proprietary training catalogs that cannot legally be redistributed.
