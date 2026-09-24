# Analytic system card

## System

Workplace Learning Recommender

## Purpose

Gap weighted resource ranking baseline with quality, difficulty, recency, and plain language explanation signals.

## Current maturity

Working research prototype. The bundled example checks the software path with synthetic inputs. It does not establish validity for real learners, instructors, courses, or workplaces.

## Inputs

See `../data/README.md` for the current synthetic schema and the documentation expected before real data are connected.

## Outputs

The current code produces a ranked list of resources and a short explanation tied to the target skill gap. These outputs are research signals and should be interpreted with the educational context that produced them.

## Evidence needed before real use

Evaluate ranking relevance against expert or user judgments, compare with simple baselines, and report coverage across skills and resources. If personalization is added, include consent and preference controls.

## Main limitation

The score depends on externally supplied skill gaps and resource metadata. It does not infer employee capability, predict job performance, or learn preferences from hidden behavioral tracking.

## Human oversight

A person must review any output before it can affect a learner, instructor, applicant, or employee.
