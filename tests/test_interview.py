"""CareerPilot AI - Unit and Integration Tests
==============================================
Validates core application logic, input validations, Pydantic schemas,
rubric calculations, and error resilience without needing network or active API calls.
"""

import unittest
from modules.interview_setup import validate_setup_inputs
from modules.question_generator import InterviewQuestion, QuestionSet
from modules.answer_evaluator import EvaluationResult, validate_user_answer
from modules.results_dashboard import calculate_interview_metrics
from modules.resume_analyzer import ResumeAnalysisResult
from modules.career_roadmap import CareerRoadmapPlan, RoadmapPhase, RoadmapTask
from utils.gemini_helper import get_api_key, test_api_connection


class TestCareerPilotLogic(unittest.TestCase):

    def test_setup_validation_success(self):
        valid, err = validate_setup_inputs("Python Developer", "Intermediate", "Technical", 5)
        self.assertTrue(valid)
        self.assertIsNone(err)

    def test_setup_validation_empty_role(self):
        valid, err = validate_setup_inputs("   ", "Intermediate", "Technical", 5)
        self.assertFalse(valid)
        self.assertIn("Target Job Role cannot be empty", err)

    def test_setup_validation_invalid_question_count(self):
        valid, err = validate_setup_inputs("Data Analyst", "Beginner", "Mixed", 0)
        self.assertFalse(valid)
        valid2, err2 = validate_setup_inputs("Data Analyst", "Beginner", "Mixed", 15)
        self.assertFalse(valid2)

    def test_answer_validation_empty(self):
        valid, err = validate_user_answer("")
        self.assertFalse(valid)
        self.assertIn("cannot be empty", err)

    def test_answer_validation_too_short(self):
        valid, err = validate_user_answer("hi there")
        self.assertFalse(valid)
        self.assertIn("too brief", err)

    def test_answer_validation_valid(self):
        valid, err = validate_user_answer(
            "In Python, a generator is a function that returns an iterator using the yield keyword instead of return."
        )
        self.assertTrue(valid)
        self.assertIsNone(err)

    def test_question_schema_validation(self):
        q = InterviewQuestion(
            id=1,
            question="Explain the difference between mutable and immutable types in Python.",
            category="Technical",
            difficulty="Intermediate",
            expected_competency="Memory model and data structures",
        )
        self.assertEqual(q.id, 1)
        self.assertEqual(q.category, "Technical")

        qs = QuestionSet(
            role="Python Developer",
            experience_level="Intermediate",
            interview_type="Technical",
            questions=[q],
        )
        self.assertEqual(len(qs.questions), 1)

    def test_evaluation_schema_validation(self):
        ev = EvaluationResult(
            question_id=1,
            score=8.5,
            relevance_score=9.0,
            technical_correctness_score=8.5,
            clarity_score=8.0,
            completeness_score=8.5,
            strengths=["Clear explanation of mutability", "Good examples with lists vs tuples"],
            weaknesses=["Did not mention memory ID and id() function"],
            missing_points=["Hashability requirement for dict keys"],
            suggestions=["Mention that immutable objects are hashable and can be dictionary keys."],
            improved_sample_answer="In Python, mutable objects like lists can be modified in place...",
            verdict="Strong Answer",
        )
        self.assertEqual(ev.score, 8.5)
        self.assertEqual(ev.verdict, "Strong Answer")

    def test_metrics_calculation(self):
        questions = [
            InterviewQuestion(id=1, question="Q1", category="Technical", difficulty="Beginner", expected_competency="C1"),
            InterviewQuestion(id=2, question="Q2", category="HR", difficulty="Beginner", expected_competency="C2"),
        ]
        evaluations = [
            EvaluationResult(
                question_id=1, score=9.0, relevance_score=9.0, technical_correctness_score=9.0,
                clarity_score=9.0, completeness_score=9.0, strengths=["Great"], weaknesses=[],
                missing_points=[], suggestions=[], improved_sample_answer="Good", verdict="Excellent"
            ),
            EvaluationResult(
                question_id=2, score=7.0, relevance_score=7.0, technical_correctness_score=7.0,
                clarity_score=7.0, completeness_score=7.0, strengths=["Good"], weaknesses=["Vague"],
                missing_points=[], suggestions=[], improved_sample_answer="Better", verdict="Competent"
            ),
        ]
        metrics = calculate_interview_metrics(evaluations, questions)
        self.assertEqual(metrics["answered_count"], 2)
        self.assertEqual(metrics["average_score"], 8.0)
        self.assertEqual(metrics["highest_score"], 9.0)
        self.assertEqual(metrics["lowest_score"], 7.0)
        self.assertIn("Strong Contender", metrics["tier"])

    def test_resume_analysis_schema(self):
        res = ResumeAnalysisResult(
            target_role="AI Engineer",
            ats_score=85,
            structural_clarity_score=90,
            impact_metrics_score=80,
            key_strengths=["Solid PyTorch projects", "Quantifiable latency improvements"],
            critical_missing_keywords=["Docker", "Kubernetes"],
            actionable_improvements=["Add container deployment experience"],
            enhanced_summary="AI Engineer with proven track record...",
        )
        self.assertEqual(res.ats_score, 85)
        self.assertEqual(len(res.critical_missing_keywords), 2)

    def test_career_roadmap_schema(self):
        task = RoadmapTask(
            task_id="p1_t1",
            title="Master Asyncio",
            description="Deep dive into Python event loops",
            recommended_resource="Python Docs",
        )
        phase = RoadmapPhase(
            phase_number=1,
            phase_name="Core Systems",
            estimated_duration="Weeks 1-4",
            core_competencies=["Asyncio", "Concurrency"],
            tasks=[task],
        )
        plan = CareerRoadmapPlan(
            role="Python Developer",
            experience_level="Intermediate",
            target_timeline="3 Months",
            summary="Strategic acceleration",
            phases=[phase],
        )
        self.assertEqual(len(plan.phases), 1)
        self.assertEqual(plan.phases[0].tasks[0].task_id, "p1_t1")

    def test_api_connection_without_key_fails_safely(self):
        ok, msg = test_api_connection(api_key="")
        self.assertFalse(ok)
        self.assertIn("Gemini API Key is missing", msg)


if __name__ == "__main__":
    unittest.main()
