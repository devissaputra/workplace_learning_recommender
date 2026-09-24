import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from workplace_learning_recommender import core


class CoreTests(unittest.TestCase):
    def test_gap_drives_ranking(self):
        resources = [{"id": "a", "skill": "python"}, {"id": "b", "skill": "writing"}]
        ranked = core.recommend({"python": 1, "writing": 0}, resources, 1)
        self.assertEqual(ranked[0]["id"], "a")

    def test_explanation_names_target_skill(self):
        text = core.explanation({"skill": "python"}, 0.4)
        self.assertIn("python", text)

    def test_invalid_quality_is_rejected(self):
        with self.assertRaises(ValueError):
            core.recommend({"python": 0.4}, [{"skill": "python", "quality": 1.2}])


if __name__ == "__main__":
    unittest.main()
