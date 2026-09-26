# Calculation reading guide: ../CALCULATIONS.md (repository root).
# Resource score = sum(normalized weight × component score).
# Language, time and prerequisites are filters, not compensable preferences. Scores encode policy weights and supplied quality ratings; high rank is not evidence of a resource’s causal effect on performance.

import math
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import date, datetime
from numbers import Real


DEFAULT_SCALE = {
    "name": "declared proficiency scale",
    "minimum": 0.0,
    "maximum": 5.0,
}

DEFAULT_WEIGHTS = {
    "need_priority": 0.20,
    "gap_coverage": 0.18,
    "task_fit": 0.12,
    "role_fit": 0.07,
    "goal_fit": 0.08,
    "quality": 0.14,
    "modality_fit": 0.08,
    "effort_fit": 0.05,
    "freshness": 0.04,
    "novelty": 0.04,
}


def _finite_number(value, name):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _unit_interval(value, name):
    value = _finite_number(value, name)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def _parse_date(value, name):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be an ISO date string")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{name} must use YYYY-MM-DD format") from exc


def _string_list(value, name):
    if value is None:
        return []
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{name} must be a sequence")
    cleaned = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{name} entries must be non-empty strings")
        item = item.strip()
        if item not in cleaned:
            cleaned.append(item)
    return cleaned


def validate_scale(scale=None):
    scale = dict(DEFAULT_SCALE if scale is None else scale)
    if set(scale) != {"name", "minimum", "maximum"}:
        raise ValueError("scale must contain exactly name, minimum, and maximum")
    if not isinstance(scale["name"], str) or not scale["name"].strip():
        raise ValueError("scale name must be a non-empty string")
    minimum = _finite_number(scale["minimum"], "scale minimum")
    maximum = _finite_number(scale["maximum"], "scale maximum")
    if minimum >= maximum:
        raise ValueError("scale minimum must be lower than maximum")
    return {
        "name": scale["name"].strip(),
        "minimum": minimum,
        "maximum": maximum,
    }


def _level(value, name, scale):
    value = _finite_number(value, name)
    if not scale["minimum"] <= value <= scale["maximum"]:
        raise ValueError(
            f"{name} must be between {scale['minimum']} and {scale['maximum']}"
        )
    return value


def validate_needs(needs, *, scale=None, minimum_confidence=0.5):
    """Validate evidence-backed development needs.

    Only entries with status='gap' are eligible for recommendation.
    Unknown or insufficient evidence remains visible but is not ranked.
    """
    scale = validate_scale(scale)
    minimum_confidence = _unit_interval(
        minimum_confidence,
        "minimum_confidence",
    )
    if not isinstance(needs, Mapping) or not needs:
        raise ValueError("needs must be a non-empty mapping")

    normalized = {}
    for skill, record in needs.items():
        if not isinstance(skill, str) or not skill.strip():
            raise ValueError("skill names must be non-empty strings")
        skill = skill.strip()
        if not isinstance(record, Mapping):
            raise ValueError(
                "each need must be a mapping with status/current/target"
            )

        status = record.get("status")
        if status not in {
            "gap",
            "met",
            "exceeds_target",
            "unknown_evidence",
            "insufficient_evidence",
        }:
            raise ValueError(f"unknown need status for {skill}: {status}")

        confidence = record.get("confidence")
        if confidence is not None:
            confidence = _unit_interval(confidence, f"{skill} confidence")

        target = _level(record.get("target"), f"{skill} target", scale)

        if status == "unknown_evidence":
            normalized[skill] = {
                "status": status,
                "current": None,
                "target": target,
                "gap": None,
                "priority": None,
                "confidence": confidence,
                "eligible": False,
                "reason": "No defensible competency evidence is available.",
            }
            continue

        current = _level(record.get("current"), f"{skill} current", scale)
        gap = record.get("gap", max(0.0, target - current))
        gap = _finite_number(gap, f"{skill} gap")
        if gap < 0:
            raise ValueError("gaps must be non-negative")

        priority = record.get("priority", gap)
        priority = _finite_number(priority, f"{skill} priority")
        if priority < 0:
            raise ValueError("priority must be non-negative")

        confidence_ok = confidence is None or confidence >= minimum_confidence
        eligible = (
            status == "gap"
            and target > current
            and gap > 0
            and confidence_ok
        )

        if status == "gap" and not confidence_ok:
            reason = "Gap exists but evidence confidence is below threshold."
            eligible = False
        elif status == "insufficient_evidence":
            reason = "Evidence is insufficient for recommendation ranking."
        elif status in {"met", "exceeds_target"}:
            reason = "No confirmed development gap."
        elif eligible:
            reason = "Confirmed development gap."
        else:
            reason = "Need is not eligible for recommendation."

        normalized[skill] = {
            "status": status,
            "current": current,
            "target": target,
            "gap": gap,
            "priority": priority,
            "confidence": confidence,
            "eligible": eligible,
            "reason": reason,
        }

    return normalized


def validate_context(context=None, *, as_of=None):
    context = {} if context is None else dict(context)
    if "as_of" in context:
        as_of = context["as_of"]
    as_of = date.today() if as_of is None else _parse_date(as_of, "as_of")

    role = context.get("role")
    if role is not None and (
        not isinstance(role, str) or not role.strip()
    ):
        raise ValueError("role must be a non-empty string when supplied")

    language = context.get("language", "any")
    if not isinstance(language, str) or not language.strip():
        raise ValueError("language must be a non-empty string")

    available_hours = context.get("available_hours")
    if available_hours is not None:
        available_hours = _finite_number(
            available_hours,
            "available_hours",
        )
        if available_hours <= 0:
            raise ValueError("available_hours must be positive")

    recent_exposures = context.get("recent_exposures", {})
    if not isinstance(recent_exposures, Mapping):
        raise ValueError("recent_exposures must be a mapping")
    exposures = {}
    for resource_id, days in recent_exposures.items():
        if not isinstance(resource_id, str) or not resource_id.strip():
            raise ValueError("recent exposure ids must be non-empty strings")
        days = _finite_number(days, f"{resource_id} days_since_seen")
        if days < 0:
            raise ValueError("days_since_seen must be non-negative")
        exposures[resource_id.strip()] = days

    return {
        "role": role.strip() if role else None,
        "role_tags": _string_list(context.get("role_tags"), "role_tags"),
        "task_tags": _string_list(context.get("task_tags"), "task_tags"),
        "goal_tags": _string_list(context.get("goal_tags"), "goal_tags"),
        "preferred_modalities": _string_list(
            context.get("preferred_modalities"),
            "preferred_modalities",
        ),
        "language": language.strip().lower(),
        "available_hours": available_hours,
        "completed_resources": set(
            _string_list(
                context.get("completed_resources"),
                "completed_resources",
            )
        ),
        "recent_exposures": exposures,
        "as_of": as_of,
    }


def validate_resources(resources, *, scale=None):
    scale = validate_scale(scale)
    if not isinstance(resources, Sequence) or isinstance(resources, (str, bytes)):
        raise ValueError("resources must be a sequence")

    ids = set()
    normalized = []
    for index, resource in enumerate(resources):
        if not isinstance(resource, Mapping):
            raise ValueError("each resource must be a mapping")

        required = {
            "id",
            "title",
            "skills",
            "entry_level",
            "target_level",
            "quality",
            "quality_source",
            "modality",
            "effort_hours",
            "available",
            "last_updated",
        }
        missing = required - set(resource)
        if missing:
            raise ValueError(
                f"resource {index} is missing fields: {sorted(missing)}"
            )

        resource_id = resource["id"]
        title = resource["title"]
        modality = resource["modality"]
        quality_source = resource["quality_source"]
        language = resource.get("language", "any")

        for value, name in (
            (resource_id, "resource id"),
            (title, "resource title"),
            (modality, "resource modality"),
            (quality_source, "quality_source"),
            (language, "resource language"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        resource_id = resource_id.strip()
        if resource_id in ids:
            raise ValueError(f"duplicate resource id: {resource_id}")
        ids.add(resource_id)

        skills = _string_list(resource["skills"], "resource skills")
        if not skills:
            raise ValueError("resource skills must not be empty")

        entry_level = _level(
            resource["entry_level"],
            f"{resource_id} entry_level",
            scale,
        )
        target_level = _level(
            resource["target_level"],
            f"{resource_id} target_level",
            scale,
        )
        if target_level <= entry_level:
            raise ValueError("resource target_level must exceed entry_level")

        effort_hours = _finite_number(
            resource["effort_hours"],
            f"{resource_id} effort_hours",
        )
        if effort_hours <= 0:
            raise ValueError("effort_hours must be positive")

        available = resource["available"]
        if not isinstance(available, bool):
            raise ValueError("available must be boolean")

        prerequisites = resource.get("prerequisites", {})
        if not isinstance(prerequisites, Mapping):
            raise ValueError("resource prerequisites must be a mapping")
        normalized_prerequisites = {}
        for skill, minimum_level in prerequisites.items():
            if not isinstance(skill, str) or not skill.strip():
                raise ValueError(
                    "resource prerequisite skills must be non-empty strings"
                )
            normalized_prerequisites[skill.strip()] = _level(
                minimum_level,
                f"{resource_id} prerequisite {skill}",
                scale,
            )

        normalized.append(
            {
                "id": resource_id,
                "title": title.strip(),
                "skills": skills,
                "entry_level": entry_level,
                "target_level": target_level,
                "quality": _unit_interval(
                    resource["quality"],
                    f"{resource_id} quality",
                ),
                "quality_source": quality_source.strip(),
                "modality": modality.strip(),
                "effort_hours": effort_hours,
                "prerequisites": normalized_prerequisites,
                "task_tags": _string_list(
                    resource.get("task_tags"),
                    "task_tags",
                ),
                "role_tags": _string_list(
                    resource.get("role_tags"),
                    "role_tags",
                ),
                "goal_tags": _string_list(
                    resource.get("goal_tags"),
                    "goal_tags",
                ),
                "language": language.strip().lower(),
                "available": available,
                "last_updated": _parse_date(
                    resource["last_updated"],
                    "last_updated",
                ),
            }
        )
    return normalized


def validate_weights(weights=None):
    weights = dict(DEFAULT_WEIGHTS if weights is None else weights)
    if set(weights) != set(DEFAULT_WEIGHTS):
        raise ValueError(
            f"weights must contain exactly {sorted(DEFAULT_WEIGHTS)}"
        )
    normalized = {}
    for name, value in weights.items():
        value = _finite_number(value, f"{name} weight")
        if value < 0:
            raise ValueError("weights must be non-negative")
        normalized[name] = value
    total = sum(normalized.values())
    if total <= 0:
        raise ValueError("at least one score weight must be positive")
    return {
        name: value / total
        for name, value in normalized.items()
    }


def _tag_fit(resource_tags, context_tags):
    if not context_tags:
        return 0.5
    if not resource_tags:
        return 0.0
    overlap = len(set(resource_tags) & set(context_tags))
    return overlap / len(set(context_tags))


def _freshness(last_updated, as_of):
    age_days = max(0, (as_of - last_updated).days)
    if age_days <= 180:
        return 1.0
    if age_days >= 730:
        return 0.0
    return 1.0 - ((age_days - 180) / 550)


def _novelty(resource_id, recent_exposures):
    if resource_id not in recent_exposures:
        return 1.0
    return min(1.0, recent_exposures[resource_id] / 90.0)


def _modality_fit(modality, preferred_modalities):
    if not preferred_modalities:
        return 0.5
    return 1.0 if modality in preferred_modalities else 0.0


def _effort_fit(effort_hours, available_hours):
    if available_hours is None:
        return 0.5
    ratio = min(1.0, effort_hours / available_hours)
    return 1.0 - 0.5 * ratio


def _eligible_need_matches(resource, needs):
    matches = []
    for skill in resource["skills"]:
        need = needs.get(skill)
        if need is None or not need["eligible"]:
            continue
        if need["current"] < resource["entry_level"]:
            continue
        if resource["target_level"] <= need["current"]:
            continue
        matches.append((skill, need))
    return matches


def eligibility_report(needs, resources, context=None, *, scale=None):
    """Return eligible resources and explicit exclusion reasons."""
    scale = validate_scale(scale)
    needs = validate_needs(needs, scale=scale)
    resources = validate_resources(resources, scale=scale)
    context = validate_context(context)

    eligible = []
    excluded = []

    for resource in resources:
        reasons = []

        if not resource["available"]:
            reasons.append("resource_unavailable")

        if resource["last_updated"] > context["as_of"]:
            reasons.append("future_last_updated")

        if resource["id"] in context["completed_resources"]:
            reasons.append("already_completed")

        if (
            context["language"] != "any"
            and resource["language"] not in {"any", context["language"]}
        ):
            reasons.append("language_mismatch")

        if (
            context["available_hours"] is not None
            and resource["effort_hours"] > context["available_hours"]
        ):
            reasons.append("exceeds_available_time")

        matches = _eligible_need_matches(resource, needs)
        if not matches:
            reasons.append("no_eligible_skill_need")

        prerequisite_failures = []
        for skill, minimum_level in resource["prerequisites"].items():
            need = needs.get(skill)
            if (
                need is None
                or need["current"] is None
                or need["current"] < minimum_level
            ):
                prerequisite_failures.append(
                    {
                        "skill": skill,
                        "minimum_level": minimum_level,
                        "current": None if need is None else need["current"],
                    }
                )
        if prerequisite_failures:
            reasons.append("prerequisites_not_met")

        record = {
            "resource": resource,
            "matched_needs": [skill for skill, _ in matches],
            "reasons": reasons,
            "prerequisite_failures": prerequisite_failures,
        }

        if reasons:
            excluded.append(record)
        else:
            eligible.append(record)

    return {
        "eligible": eligible,
        "excluded": excluded,
        "needs": needs,
        "context": context,
    }


def _score_for_need(resource, skill, need, context, max_priority, weights):
    span = max(1e-12, need["target"] - need["current"])
    coverage = min(
        need["target"],
        resource["target_level"],
    ) - need["current"]
    gap_coverage = max(0.0, min(1.0, coverage / span))

    need_priority = (
        0.0 if max_priority <= 0
        else min(1.0, need["priority"] / max_priority)
    )

    components = {
        "need_priority": need_priority,
        "gap_coverage": gap_coverage,
        "task_fit": _tag_fit(
            resource["task_tags"],
            context["task_tags"],
        ),
        "role_fit": _tag_fit(
            resource["role_tags"],
            context["role_tags"],
        ),
        "goal_fit": _tag_fit(
            resource["goal_tags"],
            context["goal_tags"],
        ),
        "quality": resource["quality"],
        "modality_fit": _modality_fit(
            resource["modality"],
            context["preferred_modalities"],
        ),
        "effort_fit": _effort_fit(
            resource["effort_hours"],
            context["available_hours"],
        ),
        "freshness": _freshness(
            resource["last_updated"],
            context["as_of"],
        ),
        "novelty": _novelty(
            resource["id"],
            context["recent_exposures"],
        ),
    }

    score = sum(
        components[name] * weights[name]
        for name in components
    )
    return {
        "matched_skill": skill,
        "score": score,
        "components": components,
        "gap_coverage": gap_coverage,
    }


def score_resources(
    needs,
    resources,
    context=None,
    *,
    scale=None,
    weights=None,
):
    """Score only resources that pass hard eligibility checks."""
    scale = validate_scale(scale)
    weights = validate_weights(weights)
    report = eligibility_report(
        needs,
        resources,
        context,
        scale=scale,
    )

    eligible_needs = [
        need
        for need in report["needs"].values()
        if need["eligible"]
    ]
    max_priority = max(
        (need["priority"] for need in eligible_needs),
        default=0.0,
    )

    scored = []
    for record in report["eligible"]:
        resource = record["resource"]
        need_scores = []
        for skill in record["matched_needs"]:
            need_scores.append(
                _score_for_need(
                    resource,
                    skill,
                    report["needs"][skill],
                    report["context"],
                    max_priority,
                    weights,
                )
            )

        best = sorted(
            need_scores,
            key=lambda row: (-row["score"], row["matched_skill"]),
        )[0]

        scored.append(
            {
                "resource": resource,
                "matched_skill": best["matched_skill"],
                "score": best["score"],
                "components": best["components"],
                "gap_coverage": best["gap_coverage"],
            }
        )

    scored.sort(
        key=lambda row: (
            -row["score"],
            row["resource"]["id"],
        )
    )

    return {
        "scored": scored,
        "excluded": report["excluded"],
        "needs": report["needs"],
        "context": report["context"],
        "weights": weights,
    }


def select_with_coverage(scored, top_k=5, max_per_skill=2):
    """Greedy reranker that gives distinct confirmed gaps a fair chance to appear."""
    if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k <= 0:
        raise ValueError("top_k must be a positive integer")
    if (
        isinstance(max_per_skill, bool)
        or not isinstance(max_per_skill, int)
        or max_per_skill <= 0
    ):
        raise ValueError("max_per_skill must be a positive integer")

    selected = []
    used_ids = set()
    skill_counts = Counter()

    # First pass: best available item for each distinct skill.
    for row in scored:
        skill = row["matched_skill"]
        resource_id = row["resource"]["id"]
        if skill_counts[skill] == 0 and resource_id not in used_ids:
            selected.append(row)
            used_ids.add(resource_id)
            skill_counts[skill] += 1
            if len(selected) == top_k:
                return selected

    # Second pass: fill remaining slots while limiting concentration.
    for row in scored:
        skill = row["matched_skill"]
        resource_id = row["resource"]["id"]
        if resource_id in used_ids:
            continue
        if skill_counts[skill] >= max_per_skill:
            continue
        selected.append(row)
        used_ids.add(resource_id)
        skill_counts[skill] += 1
        if len(selected) == top_k:
            break

    return selected


def explanation(recommendation):
    """Return a plain-language explanation grounded in actual score components."""
    resource = recommendation["resource"]
    skill = recommendation["matched_skill"]
    components = recommendation["components"]

    strongest = sorted(
        components.items(),
        key=lambda item: (-item[1], item[0]),
    )[:3]

    strengths = ", ".join(
        f"{name.replace('_', ' ')}={value:.2f}"
        for name, value in strongest
    )

    return (
        f"{resource['title']} targets the confirmed {skill} need. "
        f"It covers {recommendation['gap_coverage']:.0%} of the remaining level gap "
        f"within this resource's target range. Strongest ranking signals: {strengths}. "
        f"Overall score={recommendation['score']:.3f}."
    )


def recommendation_diagnostics(recommendations, needs):
    eligible_skills = {
        skill
        for skill, need in needs.items()
        if need["eligible"]
    }
    recommended_skills = {
        row["matched_skill"] for row in recommendations
    }
    counts = Counter(
        row["matched_skill"] for row in recommendations
    )
    total = len(recommendations)

    return {
        "recommendation_count": total,
        "eligible_skill_count": len(eligible_skills),
        "covered_skill_count": len(recommended_skills),
        "skill_coverage": (
            len(recommended_skills) / len(eligible_skills)
            if eligible_skills
            else None
        ),
        "max_skill_share": (
            max(counts.values()) / total
            if total
            else None
        ),
        "skill_counts": dict(sorted(counts.items())),
    }


def recommend(
    needs,
    resources,
    context=None,
    *,
    top_k=5,
    max_per_skill=2,
    scale=None,
    weights=None,
):
    """Return explainable, coverage-aware workplace learning recommendations."""
    scored = score_resources(
        needs,
        resources,
        context,
        scale=scale,
        weights=weights,
    )
    selected = select_with_coverage(
        scored["scored"],
        top_k=top_k,
        max_per_skill=max_per_skill,
    )

    recommendations = []
    for row in selected:
        enriched = dict(row)
        enriched["explanation"] = explanation(row)
        recommendations.append(enriched)

    return {
        "recommendations": recommendations,
        "excluded": scored["excluded"],
        "diagnostics": recommendation_diagnostics(
            recommendations,
            scored["needs"],
        ),
        "weights": scored["weights"],
    }


def ranking_sensitivity(
    needs,
    resources,
    context,
    weight_scenarios,
    *,
    top_k=5,
    max_per_skill=2,
    scale=None,
):
    """Compare recommendation order under alternative transparent weight sets."""
    if not isinstance(weight_scenarios, Mapping) or not weight_scenarios:
        raise ValueError("weight_scenarios must be a non-empty mapping")

    rankings = {}
    for name, weights in weight_scenarios.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("scenario names must be non-empty strings")
        result = recommend(
            needs,
            resources,
            context,
            top_k=top_k,
            max_per_skill=max_per_skill,
            scale=scale,
            weights=weights,
        )
        rankings[name] = [
            row["resource"]["id"]
            for row in result["recommendations"]
        ]

    resource_ids = sorted(
        {
            resource_id
            for ranking in rankings.values()
            for resource_id in ranking
        }
    )
    rank_ranges = {}
    for resource_id in resource_ids:
        positions = []
        for ranking in rankings.values():
            if resource_id in ranking:
                positions.append(ranking.index(resource_id) + 1)
        rank_ranges[resource_id] = {
            "best_rank": min(positions),
            "worst_rank": max(positions),
            "stable_rank": len(set(positions)) == 1,
            "present_in_all": len(positions) == len(rankings),
        }

    return {
        "rankings": rankings,
        "rank_ranges": rank_ranges,
    }
