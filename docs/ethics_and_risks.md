# Ethics, safety, and misuse risks

## Intended use

Workplace Learning Recommender is a transparent research prototype for development planning.

It is not an employment decision system, performance score, promotion engine, surveillance system, or proof that a recommended resource will improve performance.

## Learner control

A workplace recommender can become coercive if an employer treats suggestions as mandatory without saying so.

A real system should distinguish:

- optional recommendation
- manager-assigned development
- compliance training
- required role qualification

Do not present mandatory requirements as if they were personalized learner choices.

Learners should be able to reject, postpone, or correct a recommendation where the workplace context permits.

## Hidden preference inference

The baseline accepts declared preferences and recent exposures.

It does not infer interests, motivation, personality, or career intent from browsing, communication, keystrokes, or other hidden behavioral traces.

If future personalization uses behavioral data, affected people should understand what is collected, why it is used, how long it is retained, and how to opt out where applicable.

## Development need versus employee worth

A confirmed competency gap is a development need relative to a particular role profile.

It is not a statement about intelligence, potential, commitment, or overall employee value.

Do not convert recommendation inputs or outputs into hidden performance ratings.

## Catalog bias

A recommender can only choose from the catalog it sees.

If the catalog overrepresents certain vendors, modalities, languages, regions, or expensive programs, the ranking can reproduce that bias while still appearing personalized.

Evaluate catalog coverage before evaluating the algorithm.

## Opportunity and access

A learner may be unable to use an otherwise relevant resource because of:

- workload
- schedule
- cost
- language
- accessibility
- device or bandwidth limits
- manager approval
- geographic restrictions

The baseline models only some of these constraints.

Do not interpret resource rejection as lack of motivation.

## Time pressure

Adult learners frequently face work and family time constraints.

The baseline uses an explicit available-hours limit so a 24-hour course cannot quietly outrank a feasible four-hour alternative.

A real system should allow the learner to change this constraint rather than infer availability from work patterns.

## Quality signals

Quality is not the same as popularity.

High completion, rating, or click-through rates can reflect easy content, incentives, or organizational pressure.

Every quality value should have documented provenance.

Avoid presenting a quality score as objective if its source is weak.

## Freshness versus usefulness

Newer content is not automatically better.

Older foundational material may remain excellent.

The freshness signal is intentionally small in the baseline and should be tested rather than assumed.

## Repetition versus novelty

Recently viewed resources receive a small novelty penalty, but repetition can be beneficial.

A production system should distinguish accidental repetition from deliberate practice or spaced review.

## Workplace privacy

Learning histories can reveal career plans, perceived weaknesses, manager concerns, and sensitive professional information.

Collect only what is needed.

Define:

- access rights
- retention periods
- correction mechanisms
- deletion rules
- whether managers can see rejected recommendations
- whether learning history can be reused for performance management

## Fairness

Recommendation quality may differ across languages, job families, contract types, locations, accessibility needs, or groups with unequal access to development opportunities.

Fairness review should inspect the whole pipeline:

- competency evidence
- role requirements
- catalog availability
- metadata quality
- filtering
- ranking
- acceptance constraints

A fair ranking algorithm cannot repair an unfair catalog or biased development-need process by itself.

## Excluded uses

Do not use this prototype alone for:

- hiring or rejection
- termination
- promotion
- pay
- discipline
- forced employee ranking
- psychological profiling
- covert monitoring
- automatic career-path assignment
- withholding opportunities because the recommender did not select them

## Before real deployment

Document the source of development needs, resource catalog governance, preference collection, privacy controls, learner override, accessibility, quality methodology, catalog coverage, human review, explanation testing, rejection handling, monitoring for unintended employment use, and a clear process for correcting wrong data.
