def recommend(gaps, resources, top_k=5):
    """Rank resources with transparent gap, quality, difficulty, and recency terms."""
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    scored = []
    for resource in resources:
        if "skill" not in resource:
            raise ValueError("each resource must include a skill")
        gap = gaps.get(resource["skill"], 0.0)
        if gap < 0:
            raise ValueError("skill gaps must be non-negative")
        quality = resource.get("quality", 0.5)
        difficulty = resource.get("difficulty", 0.5)
        target_difficulty = resource.get("target_difficulty", 0.5)
        recently_seen = resource.get("recently_seen", 0)
        for name, value in (
            ("quality", quality),
            ("difficulty", difficulty),
            ("target_difficulty", target_difficulty),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")
        if recently_seen < 0:
            raise ValueError("recently_seen must be non-negative")
        difficulty_penalty = abs(difficulty - target_difficulty)
        score = 2 * gap + quality - 0.4 * difficulty_penalty - 0.2 * recently_seen
        scored.append((score, str(resource.get("id", "")), resource))
    scored.sort(key=lambda row: (-row[0], row[1]))
    return [resource for _, _, resource in scored[:top_k]]


def explanation(resource, gap):
    """Return a plain language explanation for one ranked resource."""
    if "skill" not in resource:
        raise ValueError("resource must include a skill")
    if gap < 0:
        raise ValueError("gap must be non-negative")
    return (
        f"Recommended because it targets {resource['skill']} "
        f"(current gap {gap:.2f}) and fits the requested learning context."
    )
