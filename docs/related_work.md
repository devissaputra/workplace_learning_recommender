# Related work and methodological context

Workplace Learning Recommender is an original transparent implementation.

It does not claim to reproduce the methods or results of the work below.

## Workplace learning recommender goals

Hemmler, Rasch, and Ifenthaler reviewed workplace-learning goals for multi-stakeholder recommender systems and highlighted that workplace learning recommendations can serve different stakeholders and development objectives.

- Hemmler YM, Rasch J, Ifenthaler D. *A Categorization of Workplace Learning Goals for Multi-Stakeholder Recommender Systems: A Systematic Review.* TechTrends. 2023;67:98–111.
- https://doi.org/10.1007/s11528-022-00777-y

This supports an important design boundary in this repository: a recommendation should be tied to an explicit development goal rather than treated as universally useful.

## Task-oriented workplace recommendation

Research on knowledge recommendation for workplace learning has emphasized that workplace needs are dynamic and task-oriented.

- *Knowledge recommendation for workplace learning: a system design and evaluation perspective.*
- Internet Research. 2020;30(1):243–261.
- https://doi.org/10.1108/INTR-07-2018-0336

The current baseline represents this idea with explicit task tags supplied in the request context.

It does not infer task relevance automatically from employee behavior.

## Explainable talent-training recommendation

Research on enterprise training recommendation has also examined explainable course recommendation in the context of employee development.

- *Contextualized Knowledge Graph Embedding for Explainable Talent Training Course Recommendation.*
- ACM Transactions on Information Systems. 2024;42(2), Article 33.
- https://doi.org/10.1145/3597022

This repository uses a much simpler transparent baseline. It does not implement knowledge-graph embeddings or a learned model.

Its explanation strategy is deliberately decomposable: every returned recommendation exposes the actual score components used by the ranker.

## Learner control and privacy

Recent workplace-learning recommender research has examined how control over data disclosure affects user perceptions of AI-based learning recommender systems.

- *The Power of Choice: Understanding the Role of Control in Learning Recommender Systems for Workplace Learning.*
- International Journal of Human–Computer Interaction. 2026.
- https://doi.org/10.1080/10447318.2026.2617137

The current repository therefore treats role tags, task tags, goals, modality preferences, and recent exposures as explicit inputs rather than silently inferred personal attributes.

## Adult-learning constraints

OECD adult-learning work emphasizes that time constraints are a major barrier to training participation and that much job-related learning takes place in the workplace.

- OECD Adult Learning topic: https://www.oecd.org/en/topics/adult-learning.html
- OECD. *Trends in Adult Learning: New Data from the 2023 Survey of Adult Skills.* 2025.
- https://doi.org/10.1787/ec0624a6-en

The baseline models an explicit available-hours constraint rather than assuming every relevant course is practically feasible.

## Recommender-system evaluation

A recommendation list should not be judged only by whether its top item looks plausible.

This repository therefore distinguishes several evaluation questions:

- ranking relevance
- catalog coverage
- skill coverage
- concentration
- explanation usefulness
- rejection reasons
- ranking sensitivity
- eventual learning impact

The current code implements skill-coverage and concentration diagnostics plus weight sensitivity.

It does not yet implement offline relevance metrics such as nDCG because the repository contains no empirical relevance judgments.

## Scope boundary

Implemented:

- evidence-backed development-need eligibility
- resource entry/target levels
- prerequisites
- availability and time-budget filtering
- language filtering
- role/task/goal tags
- modality preference
- resource quality with provenance field
- resource freshness
- prior-exposure novelty
- normalized transparent scoring
- coverage-aware reranking
- component-level explanations
- recommendation diagnostics
- weight sensitivity

Not implemented:

- collaborative filtering
- matrix factorization
- knowledge graphs
- embeddings
- large language model ranking
- click-based preference learning
- hidden behavioral profiling
- causal estimates of learning impact
- automatic career-path decisions
