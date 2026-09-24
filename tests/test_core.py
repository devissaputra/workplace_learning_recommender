import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from workplace_learning_recommender import core


SCALE = {
    "name": "Synthetic 0-5 proficiency scale",
    "minimum": 0,
    "maximum": 5,
}

NEEDS = {
    "python": {
        "status": "gap",
        "current": 2.0,
        "target": 4.0,
        "gap": 2.0,
        "priority": 2.4,
        "confidence": 0.9,
    },
    "statistics": {
        "status": "gap",
        "current": 1.5,
        "target": 3.0,
        "gap": 1.5,
        "priority": 2.1,
        "confidence": 0.9,
    },
    "facilitation": {
        "status": "gap",
        "current": 2.0,
        "target": 3.0,
        "gap": 1.0,
        "priority": 0.9,
        "confidence": 0.8,
    },
    "instructional_design": {
        "status": "exceeds_target",
        "current": 4.5,
        "target": 4.0,
        "gap": 0.0,
        "priority": 0.0,
        "confidence": 0.95,
    },
    "stakeholder_communication": {
        "status": "unknown_evidence",
        "current": None,
        "target": 4.0,
        "gap": None,
        "priority": None,
        "confidence": None,
    },
}

RESOURCES = [
    {
        "id": "python-lab",
        "title": "Applied Python Analysis Lab",
        "skills": ["python"],
        "entry_level": 1.5,
        "target_level": 4.0,
        "quality": 0.90,
        "quality_source": "expert review",
        "modality": "project",
        "effort_hours": 8,
        "prerequisites": {},
        "task_tags": ["analysis", "automation"],
        "role_tags": ["learning-analytics"],
        "goal_tags": ["workflow-automation"],
        "language": "en",
        "available": True,
        "last_updated": "2026-07-01",
    },
    {
        "id": "python-short",
        "title": "Python Refresher",
        "skills": ["python"],
        "entry_level": 1.0,
        "target_level": 3.0,
        "quality": 0.82,
        "quality_source": "expert review",
        "modality": "self-paced",
        "effort_hours": 3,
        "prerequisites": {},
        "task_tags": ["analysis"],
        "role_tags": ["learning-analytics"],
        "goal_tags": ["workflow-automation"],
        "language": "en",
        "available": True,
        "last_updated": "2026-08-15",
    },
    {
        "id": "stats-foundations",
        "title": "Statistics Foundations Lab",
        "skills": ["statistics"],
        "entry_level": 1.0,
        "target_level": 3.0,
        "quality": 0.88,
        "quality_source": "expert review",
        "modality": "project",
        "effort_hours": 7,
        "prerequisites": {},
        "task_tags": ["analysis"],
        "role_tags": ["learning-analytics"],
        "goal_tags": ["evidence-quality"],
        "language": "en",
        "available": True,
        "last_updated": "2026-06-15",
    },
    {
        "id": "facilitation-practice",
        "title": "Facilitation Practice Sprint",
        "skills": ["facilitation"],
        "entry_level": 1.0,
        "target_level": 3.0,
        "quality": 0.84,
        "quality_source": "expert review",
        "modality": "workshop",
        "effort_hours": 4,
        "prerequisites": {},
        "task_tags": ["workshop"],
        "role_tags": ["learning-partner"],
        "goal_tags": ["facilitation"],
        "language": "en",
        "available": True,
        "last_updated": "2026-08-01",
    },
]


CONTEXT = {
    "role": "Learning Analytics Specialist",
    "role_tags": ["learning-analytics"],
    "task_tags": ["analysis", "automation"],
    "goal_tags": ["workflow-automation"],
    "preferred_modalities": ["project"],
    "language": "en",
    "available_hours": 10,
    "completed_resources": [],
    "recent_exposures": {},
}


class CoreTests(unittest.TestCase):
    def test_scale_validates(self):
        self.assertEqual(
            core.validate_scale(SCALE)["maximum"],
            5.0,
        )

    def test_invalid_scale_rejected(self):
        with self.assertRaises(ValueError):
            core.validate_scale(
                {"name": "bad", "minimum": 5, "maximum": 1}
            )

    def test_unknown_evidence_is_not_eligible(self):
        needs = core.validate_needs(NEEDS, scale=SCALE)
        self.assertFalse(
            needs["stakeholder_communication"]["eligible"]
        )

    def test_met_skill_is_not_eligible(self):
        needs = core.validate_needs(NEEDS, scale=SCALE)
        self.assertFalse(
            needs["instructional_design"]["eligible"]
        )

    def test_low_confidence_gap_is_not_eligible(self):
        needs = {
            "python": {
                "status": "gap",
                "current": 2,
                "target": 4,
                "gap": 2,
                "priority": 2,
                "confidence": 0.2,
            }
        }
        result = core.validate_needs(
            needs,
            scale=SCALE,
            minimum_confidence=0.5,
        )
        self.assertFalse(result["python"]["eligible"])

    def test_nan_priority_rejected(self):
        bad = {
            "python": {
                "status": "gap",
                "current": 2,
                "target": 4,
                "gap": 2,
                "priority": math.nan,
                "confidence": 0.9,
            }
        }
        with self.assertRaises(ValueError):
            core.validate_needs(bad, scale=SCALE)

    def test_boolean_quality_rejected(self):
        bad = [dict(RESOURCES[0], quality=True)]
        with self.assertRaises(ValueError):
            core.validate_resources(bad, scale=SCALE)

    def test_duplicate_resource_id_rejected(self):
        with self.assertRaises(ValueError):
            core.validate_resources(
                [RESOURCES[0], dict(RESOURCES[0])],
                scale=SCALE,
            )

    def test_target_must_exceed_entry_level(self):
        bad = [
            dict(
                RESOURCES[0],
                entry_level=4,
                target_level=3,
            )
        ]
        with self.assertRaises(ValueError):
            core.validate_resources(bad, scale=SCALE)

    def test_context_rejects_negative_exposure_days(self):
        with self.assertRaises(ValueError):
            core.validate_context(
                {"recent_exposures": {"r1": -1}}
            )

    def test_unavailable_resource_is_excluded(self):
        resources = [
            dict(RESOURCES[0], available=False)
        ]
        report = core.eligibility_report(
            NEEDS,
            resources,
            CONTEXT,
            scale=SCALE,
        )
        self.assertEqual(len(report["eligible"]), 0)
        self.assertIn(
            "resource_unavailable",
            report["excluded"][0]["reasons"],
        )

    def test_completed_resource_is_excluded(self):
        context = dict(
            CONTEXT,
            completed_resources=["python-lab"],
        )
        report = core.eligibility_report(
            NEEDS,
            [RESOURCES[0]],
            context,
            scale=SCALE,
        )
        self.assertIn(
            "already_completed",
            report["excluded"][0]["reasons"],
        )

    def test_language_mismatch_is_excluded(self):
        context = dict(CONTEXT, language="id")
        report = core.eligibility_report(
            NEEDS,
            [RESOURCES[0]],
            context,
            scale=SCALE,
        )
        self.assertIn(
            "language_mismatch",
            report["excluded"][0]["reasons"],
        )

    def test_excessive_effort_is_excluded(self):
        context = dict(CONTEXT, available_hours=2)
        report = core.eligibility_report(
            NEEDS,
            [RESOURCES[0]],
            context,
            scale=SCALE,
        )
        self.assertIn(
            "exceeds_available_time",
            report["excluded"][0]["reasons"],
        )

    def test_no_confirmed_need_excludes_resource(self):
        resource = dict(
            RESOURCES[0],
            id="id-course",
            skills=["instructional_design"],
        )
        report = core.eligibility_report(
            NEEDS,
            [resource],
            CONTEXT,
            scale=SCALE,
        )
        self.assertIn(
            "no_eligible_skill_need",
            report["excluded"][0]["reasons"],
        )

    def test_entry_level_is_enforced(self):
        resource = dict(
            RESOURCES[0],
            entry_level=3.0,
        )
        report = core.eligibility_report(
            NEEDS,
            [resource],
            CONTEXT,
            scale=SCALE,
        )
        self.assertIn(
            "no_eligible_skill_need",
            report["excluded"][0]["reasons"],
        )

    def test_prerequisite_is_enforced(self):
        resource = dict(
            RESOURCES[0],
            prerequisites={"statistics": 2.5},
        )
        report = core.eligibility_report(
            NEEDS,
            [resource],
            CONTEXT,
            scale=SCALE,
        )
        self.assertIn(
            "prerequisites_not_met",
            report["excluded"][0]["reasons"],
        )

    def test_weights_normalize(self):
        weights = core.validate_weights(
            {name: 1 for name in core.DEFAULT_WEIGHTS}
        )
        self.assertAlmostEqual(sum(weights.values()), 1.0)

    def test_task_context_changes_score(self):
        matching = core.score_resources(
            NEEDS,
            [RESOURCES[0]],
            CONTEXT,
            scale=SCALE,
        )["scored"][0]["score"]
        other_context = dict(
            CONTEXT,
            task_tags=["presentation"],
        )
        mismatching = core.score_resources(
            NEEDS,
            [RESOURCES[0]],
            other_context,
            scale=SCALE,
        )["scored"][0]["score"]
        self.assertGreater(matching, mismatching)

    def test_goal_context_changes_score(self):
        matching = core.score_resources(
            NEEDS,
            [RESOURCES[0]],
            CONTEXT,
            scale=SCALE,
        )["scored"][0]["score"]
        other_context = dict(
            CONTEXT,
            goal_tags=["facilitation"],
        )
        mismatching = core.score_resources(
            NEEDS,
            [RESOURCES[0]],
            other_context,
            scale=SCALE,
        )["scored"][0]["score"]
        self.assertGreater(matching, mismatching)

    def test_modality_preference_changes_score(self):
        project_context = dict(
            CONTEXT,
            preferred_modalities=["project"],
        )
        workshop_context = dict(
            CONTEXT,
            preferred_modalities=["workshop"],
        )
        first = core.score_resources(
            NEEDS,
            [RESOURCES[0]],
            project_context,
            scale=SCALE,
        )["scored"][0]["score"]
        second = core.score_resources(
            NEEDS,
            [RESOURCES[0]],
            workshop_context,
            scale=SCALE,
        )["scored"][0]["score"]
        self.assertGreater(first, second)

    def test_recent_exposure_reduces_novelty(self):
        fresh_context = dict(CONTEXT, recent_exposures={})
        recent_context = dict(
            CONTEXT,
            recent_exposures={"python-lab": 0},
        )
        first = core.score_resources(
            NEEDS,
            [RESOURCES[0]],
            fresh_context,
            scale=SCALE,
        )["scored"][0]
        second = core.score_resources(
            NEEDS,
            [RESOURCES[0]],
            recent_context,
            scale=SCALE,
        )["scored"][0]
        self.assertGreater(
            first["components"]["novelty"],
            second["components"]["novelty"],
        )

    def test_old_resource_has_lower_freshness(self):
        old = dict(
            RESOURCES[0],
            id="old",
            last_updated="2023-01-01",
        )
        new = dict(
            RESOURCES[0],
            id="new",
            last_updated="2026-08-01",
        )
        result = core.score_resources(
            NEEDS,
            [old, new],
            CONTEXT,
            scale=SCALE,
        )["scored"]
        by_id = {
            row["resource"]["id"]: row
            for row in result
        }
        self.assertGreater(
            by_id["new"]["components"]["freshness"],
            by_id["old"]["components"]["freshness"],
        )

    def test_quality_source_is_required(self):
        resource = dict(RESOURCES[0])
        del resource["quality_source"]
        with self.assertRaises(ValueError):
            core.validate_resources(
                [resource],
                scale=SCALE,
            )

    def test_coverage_selects_distinct_skills_first(self):
        scored = core.score_resources(
            NEEDS,
            RESOURCES,
            CONTEXT,
            scale=SCALE,
        )["scored"]
        selected = core.select_with_coverage(
            scored,
            top_k=3,
            max_per_skill=2,
        )
        self.assertEqual(
            len({row["matched_skill"] for row in selected}),
            3,
        )

    def test_max_per_skill_limits_concentration(self):
        scored = core.score_resources(
            NEEDS,
            RESOURCES,
            CONTEXT,
            scale=SCALE,
        )["scored"]
        selected = core.select_with_coverage(
            scored,
            top_k=4,
            max_per_skill=1,
        )
        counts = {}
        for row in selected:
            counts[row["matched_skill"]] = (
                counts.get(row["matched_skill"], 0) + 1
            )
        self.assertLessEqual(max(counts.values()), 1)

    def test_explanation_uses_actual_components(self):
        result = core.recommend(
            NEEDS,
            RESOURCES,
            CONTEXT,
            top_k=2,
            scale=SCALE,
        )
        text = result["recommendations"][0]["explanation"]
        self.assertIn("Overall score=", text)
        self.assertIn("confirmed", text)

    def test_diagnostics_reports_skill_coverage(self):
        result = core.recommend(
            NEEDS,
            RESOURCES,
            CONTEXT,
            top_k=3,
            scale=SCALE,
        )
        self.assertEqual(
            result["diagnostics"]["covered_skill_count"],
            3,
        )
        self.assertEqual(
            result["diagnostics"]["skill_coverage"],
            1.0,
        )

    def test_recommendation_is_deterministic(self):
        first = core.recommend(
            NEEDS,
            RESOURCES,
            CONTEXT,
            top_k=3,
            scale=SCALE,
        )
        second = core.recommend(
            NEEDS,
            RESOURCES,
            CONTEXT,
            top_k=3,
            scale=SCALE,
        )
        self.assertEqual(
            [
                row["resource"]["id"]
                for row in first["recommendations"]
            ],
            [
                row["resource"]["id"]
                for row in second["recommendations"]
            ],
        )

    def test_top_k_rejects_boolean(self):
        with self.assertRaises(ValueError):
            core.select_with_coverage([], top_k=True)

    def test_ranking_sensitivity_returns_scenarios(self):
        equal = {
            name: 1.0
            for name in core.DEFAULT_WEIGHTS
        }
        quality_heavy = dict(equal)
        quality_heavy["quality"] = 5.0
        result = core.ranking_sensitivity(
            NEEDS,
            RESOURCES,
            CONTEXT,
            {
                "balanced": equal,
                "quality_heavy": quality_heavy,
            },
            top_k=3,
            scale=SCALE,
        )
        self.assertEqual(
            set(result["rankings"]),
            {"balanced", "quality_heavy"},
        )

    def test_missing_gap_is_not_silently_zero(self):
        resource = dict(
            RESOURCES[0],
            id="unknown-skill",
            skills=["unknown_skill"],
        )
        report = core.eligibility_report(
            NEEDS,
            [resource],
            CONTEXT,
            scale=SCALE,
        )
        self.assertIn(
            "no_eligible_skill_need",
            report["excluded"][0]["reasons"],
        )


if __name__ == "__main__":
    unittest.main()
