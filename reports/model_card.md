# Recommendation system card

## System

Workplace Learning Recommender

## Purpose

Transparent recommendation of workplace-learning resources for confirmed development needs under explicit learner and workplace constraints.

## Current maturity

Working research prototype.

The bundled example is fully synthetic.

No empirical study in this repository demonstrates that the recommendations improve learning, job performance, or career outcomes.

## Inputs

### Development needs

For each competency:

- status
- current level
- target level
- gap
- priority
- confidence

Only sufficiently supported confirmed gaps are eligible.

### Workplace-learning context

- role label
- role tags
- task tags
- learning-goal tags
- preferred modalities
- language
- available hours
- completed resources
- recent exposures
- recommendation date

### Resource metadata

- id
- title
- target skills
- entry level
- target level
- quality
- quality source
- modality
- effort
- prerequisites
- task tags
- role tags
- goal tags
- language
- availability
- last-updated date

## Eligibility

A resource is filtered out when it is:

- unavailable
- already completed
- incompatible with the selected language
- longer than the declared time budget
- unrelated to any confirmed need
- above the learner's entry level
- unable to advance beyond the current level
- blocked by unmet prerequisites

Eligibility is separated from ranking so unsuitable items cannot compensate with a high quality or context score.

## Ranking components

Eligible resources receive normalized values for:

- need priority
- gap coverage
- task fit
- role fit
- goal fit
- quality
- modality fit
- effort fit
- freshness
- novelty

Weights are explicit and normalized.

The default weight vector is a design baseline, not an empirically validated optimum.

## Coverage-aware selection

The first pass gives distinct confirmed competency gaps an opportunity to appear.

The second pass fills remaining positions while respecting a configurable maximum number of resources per skill.

This is a simple deterministic coverage heuristic.

## Outputs

Each recommendation contains:

- resource metadata
- matched competency
- total score
- every score component
- gap coverage
- explanation grounded in the computed values

The system also returns:

- excluded resources
- exclusion reasons
- recommendation count
- skill coverage
- skill concentration
- ranking-sensitivity results when requested

## Explanation boundary

The explanation can state what the software actually measured.

It should not claim:

- that a learner will like the resource
- that the resource will improve performance
- that the resource is objectively best
- that a preference was inferred when it was not supplied
- that a contextual match exists when no relevant tags were provided

## Main limitations

The current baseline:

- depends on externally supplied competency needs
- depends on hand-authored resource metadata
- uses simple tag overlap for task/role/goal fit
- uses heuristic freshness and novelty functions
- uses hand-selected default weights
- does not model resource cost
- does not model accessibility beyond what could be added to metadata
- does not represent mentoring, job aids, stretch assignments, peer learning, or workflow redesign
- does not learn from user behavior
- does not estimate causal learning impact

## Evidence needed before real use

A production-oriented study should evaluate:

- need validity
- catalog completeness
- resource metadata reliability
- prerequisite validity
- quality-score provenance
- language and accessibility coverage
- expert relevance judgments
- user relevance judgments
- rejection reasons
- skill coverage
- list concentration
- sensitivity to weights
- learning outcomes after accepted recommendations
- whether different worker groups receive systematically different opportunity quality

## Human oversight

A learner or L&D professional should be able to inspect, reject, postpone, or correct recommendations and the data behind them.

The system should not automatically convert recommendation outputs into employment decisions or mandatory development requirements.
