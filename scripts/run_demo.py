import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from workplace_learning_recommender.core import (
    DEFAULT_WEIGHTS,
    recommend,
    ranking_sensitivity,
)


def load_json(name):
    with (ROOT / "data" / name).open(encoding="utf-8") as handle:
        return json.load(handle)


need_payload = load_json("needs.json")
context = load_json("context.json")
resources = load_json("resources.json")

result = recommend(
    need_payload["needs"],
    resources,
    context,
    top_k=5,
    max_per_skill=2,
    scale=need_payload["scale"],
)

print("Workplace Learning Recommender synthetic demo")
print("Role:", context["role"])
print("As of:", context["as_of"])
print()

print("Recommendations:")
for index, row in enumerate(result["recommendations"], start=1):
    resource = row["resource"]
    print(
        index,
        resource["id"],
        {
            "title": resource["title"],
            "skill": row["matched_skill"],
            "score": round(row["score"], 3),
            "components": {
                name: round(value, 3)
                for name, value in row["components"].items()
            },
        },
    )
    print("  ", row["explanation"])

print("\nDiagnostics:")
print(result["diagnostics"])

reason_counts = Counter()
for row in result["excluded"]:
    for reason in row["reasons"]:
        reason_counts[reason] += 1

print("\nExcluded resources by reason:")
for reason, count in sorted(reason_counts.items()):
    print(reason, count)

balanced = dict(DEFAULT_WEIGHTS)
quality_heavy = dict(DEFAULT_WEIGHTS)
quality_heavy["quality"] = 0.40
quality_heavy["need_priority"] = 0.10
quality_heavy["gap_coverage"] = 0.10

task_heavy = dict(DEFAULT_WEIGHTS)
task_heavy["task_fit"] = 0.35
task_heavy["quality"] = 0.08
task_heavy["need_priority"] = 0.12

sensitivity = ranking_sensitivity(
    need_payload["needs"],
    resources,
    context,
    {
        "balanced": balanced,
        "quality_heavy": quality_heavy,
        "task_heavy": task_heavy,
    },
    top_k=5,
    max_per_skill=2,
    scale=need_payload["scale"],
)

print("\nRanking sensitivity:")
for name, ranking in sensitivity["rankings"].items():
    print(name, ranking)

print(
    "\nNote: all needs, resource metadata, quality values, "
    "context tags, and constraints are synthetic. "
    "The demo tests software behavior; it does not show that "
    "these recommendations improve real workplace learning."
)
