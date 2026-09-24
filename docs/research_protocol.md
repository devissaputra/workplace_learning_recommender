# Research protocol

## Project

Workplace Learning Recommender

## Research questions

1. How should confirmed competency needs be combined with work context, learner constraints, and resource metadata?
2. Which constraints should exclude a resource before ranking?
3. How much do task, role, goal, modality, effort, quality, freshness, and prior exposure change the recommendation order?
4. How can the system avoid returning five nearly identical resources for one high-priority skill?
5. Which score components make a recommendation understandable enough for a learner or L&D reviewer to challenge?
6. How stable are recommendations under plausible alternative weight settings?

## Current baseline

The implementation separates two decisions:

### 1. Eligibility

A resource must first pass hard constraints:

- available
- not already completed
- compatible language
- within the declared time budget
- connected to a confirmed development need
- learner meets the resource entry level
- resource advances beyond the current level
- declared prerequisites are met

### 2. Ranking

Only eligible resources receive a score.

The baseline score contains ten normalized components:

- confirmed-need priority
- gap coverage
- current-task fit
- role fit
- learning-goal fit
- resource quality
- modality fit
- effort fit
- resource freshness
- novelty relative to recent exposure

The score weights are explicit, configurable, and normalized.

## Why eligibility is separate from ranking

A high-quality resource should not outrank a prerequisite failure, an unavailable course, an incompatible language, or a course that does not address a confirmed need.

Treating constraints as small penalties can allow unsuitable items to survive because other features compensate for them.

The current baseline therefore uses hard filtering for clear constraints and soft scoring for preference or relevance dimensions.

## Confirmed development need

The recommender does not infer employee competency.

It expects an upstream need record with:

- status
- current level
- target level
- gap
- priority
- confidence

Only sufficiently supported records with `status="gap"` enter recommendation ranking.

Unknown evidence, insufficient evidence, met targets, and exceeded targets are visible but ineligible.

## Resource-level fit

A resource is eligible only when:

`entry_level <= current_level < resource_target_level`

Gap coverage is then:

`min(role_target, resource_target) - current_level`

divided by the learner's remaining level gap.

This prevents a resource that teaches below the learner's current level from receiving full credit simply because it targets the right skill.

## Context fit

The baseline uses declared tags rather than free-text inference:

- task tags
- role tags
- learning-goal tags

Overlap is transparent.

If a context dimension is not provided, it receives a neutral value rather than an invented match.

## Preferences and constraints

Preferred modalities affect soft ranking.

Available time is treated as a hard upper bound in the baseline.

This is a design choice that should be tested. A production system may instead allow learners to override the budget or save longer resources for later.

## Quality

Resource quality is an externally supplied value from 0 to 1.

Every resource must also declare a `quality_source`.

The baseline does not infer quality from popularity, completion rate, or clicks.

Future studies should compare different evidence sources and check whether quality judgments predict useful learning outcomes.

## Freshness and prior exposure

These are deliberately separate.

### Freshness

Derived from the resource's `last_updated` date.

The baseline gives full freshness credit to resources updated within 180 days and linearly reduces the score until 730 days.

This is a heuristic, not evidence that newer material is inherently better.

### Novelty

Derived from days since the learner last saw the resource.

Recently seen resources receive lower novelty; resources not seen in the supplied exposure history receive full novelty.

This should not become a mechanism for constant novelty seeking. Repetition can be instructionally useful.

## Coverage control

The first selection pass gives distinct confirmed skill gaps a chance to appear.

A second pass fills remaining positions while respecting `max_per_skill`.

This is a transparent coverage heuristic, not a learned diversification model.

It addresses a common failure mode where the numerically largest gap dominates the whole list.

## Explanation

Each returned recommendation exposes:

- matched skill
- total score
- every score component
- gap coverage
- strongest ranking signals
- resource metadata

The explanation is generated from the values actually used by the scorer.

It does not claim contextual fit that was never measured.

## Ranking sensitivity

`ranking_sensitivity()` repeats recommendation under alternative weight sets.

The output records:

- recommendation order by scenario
- best rank
- worst rank
- whether rank is stable
- whether the item appears in every scenario

A resource that only appears under one narrow weighting scheme should be treated as a fragile recommendation.

## Evaluation study

A meaningful empirical evaluation should include several layers.

### Eligibility precision

Ask experts and affected learners whether filtered resources were genuinely infeasible or irrelevant.

### Ranking relevance

Compare the transparent baseline with simpler alternatives such as:

- gap-only ranking
- quality-only ranking
- popularity ranking
- random eligible resource

### Coverage

Measure how many confirmed development needs receive at least one useful recommendation.

### Concentration

Track how much of the list is devoted to one skill or one resource family.

### User judgment

Collect:

- relevance
- actionability
- explanation usefulness
- rejection reasons
- preference corrections
- whether the user wants more or less control

### Learning impact

Do not treat clicks, starts, or completions as proof of learning.

Where ethically appropriate, evaluate whether accepted recommendations lead to stronger independent competency evidence or useful work performance outcomes.

## Threats to validity

Major threats include:

- wrong or stale competency needs
- misleading role/task tags
- shallow taxonomies
- poor resource metadata
- arbitrary quality scores
- popularity or catalog bias
- over-reliance on freshness
- treating user preferences as permanent
- employer pressure disguised as personalization
- missing informal or on-the-job learning options
- optimizing engagement rather than development
- narrow catalogs that create the appearance of personalization
- assuming a ranked course list is the right intervention when mentoring, practice, job aids, or workflow redesign may be better
