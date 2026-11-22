"""CareerPilot AI - Results Dashboard Module
===========================================
Displays a comprehensive post-interview analytics dashboard:
- Total & average scores out of 10
- Performance tier badge
- Interactive score progression chart (Altair / Streamlit native)
- Aggregated strengths and areas for improvement
- Detailed question-by-question review with expandable feedback
- Actionable next steps for candidate career preparation
- Restart interview button
"""

from typing import List, Dict, Any
import streamlit as st
from modules.answer_evaluator import EvaluationResult
from modules.question_generator import InterviewQuestion


def calculate_interview_metrics(
    evaluations: List[EvaluationResult],
    questions: List[InterviewQuestion],
) -> Dict[str, Any]:
    """Compute aggregate performance statistics."""
    if not evaluations:
        return {
            "total_questions": len(questions),
            "answered_count": 0,
            "average_score": 0.0,
            "total_score": 0.0,
            "highest_score": 0.0,
            "lowest_score": 0.0,
            "tier": "No Data",
        }

    scores = [e.score for e in evaluations]
    total_score = sum(scores)
    avg_score = round(total_score / len(scores), 1)
    highest = max(scores)
    lowest = min(scores)

    if avg_score >= 8.5:
        tier = "🎯 Job-Ready / Exceptional Candidate"
        tier_color = "#55A987"  # Success
    elif avg_score >= 7.0:
        tier = "⭐ Strong Contender / Proficient"
        tier_color = "#36A6A0"  # Accent Teal
    elif avg_score >= 5.0:
        tier = "📈 Emerging Potential / Needs Focused Practice"
        tier_color = "#E4B35E"  # Warning
    else:
        tier = "⚠️ High Development Area / Revisit Fundamentals"
        tier_color = "#D77B69"  # Error / Coral

    return {
        "total_questions": len(questions),
        "answered_count": len(evaluations),
        "average_score": avg_score,
        "total_score": round(total_score, 1),
        "highest_score": highest,
        "lowest_score": lowest,
        "tier": tier,
        "tier_color": tier_color,
    }


def render_results_dashboard(
    session_config: Dict[str, Any],
    questions: List[InterviewQuestion],
    evaluations: List[EvaluationResult],
    user_answers: Dict[int, str],
):
    """Render the full results dashboard in Streamlit."""
    metrics = calculate_interview_metrics(evaluations, questions)

    # Header Card
    st.markdown(
        f"""
        <div class="cp-card" style="border-top: 4px solid {metrics.get('tier_color', '#36A6A0')}; text-align: center; padding: 28px;">
            <span style="font-size:0.8rem; color:#A5B7B3; text-transform:uppercase; letter-spacing:2px; font-weight:600;">
                Interview Performance Summary
            </span>
            <h1 style="color:#F3F7F5; margin: 8px 0 12px 0; font-size: 2.2rem; font-weight:800;">
                Overall Average: <span style="color:{metrics.get('tier_color', '#36A6A0')}">{metrics['average_score']} / 10.0</span>
            </h1>
            <div style="display:inline-block; background:rgba(255,255,255,0.04); 
                        border: 1px solid {metrics.get('tier_color', '#36A6A0')}; 
                        color: {metrics.get('tier_color', '#36A6A0')}; 
                        padding: 6px 18px; border-radius: 20px; font-weight: 700; font-size: 0.95rem;">
                {metrics['tier']}
            </div>
            <p style="color:#A5B7B3; margin-top:14px; font-size:0.95rem;">
                Role: <strong style="color:#F3F7F5;">{session_config.get('role', 'N/A')}</strong> | 
                Level: <strong style="color:#F3F7F5;">{session_config.get('experience_level', 'N/A')}</strong> | 
                Type: <strong style="color:#F3F7F5;">{session_config.get('interview_type', 'N/A')}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top Metric Columns
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("📊 Questions Answered", f"{metrics['answered_count']} of {metrics['total_questions']}")
    with m2:
        st.metric("🏆 Total Score", f"{metrics['total_score']} / {metrics['total_questions'] * 10}")
    with m3:
        st.metric("🌟 Peak Score", f"{metrics['highest_score']} / 10")
    with m4:
        st.metric("⚡ Lowest Score", f"{metrics['lowest_score']} / 10")

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 24px 0;'>", unsafe_allow_html=True)

    # Question Performance Breakdown Chart
    st.subheader("📈 Performance Breakdown by Question")

    chart_data = {f"Q{idx} ({q.category.split('/')[0].strip()})": ev.score for idx, (q, ev) in enumerate(zip(questions, evaluations), start=1)}
    if chart_data:
        st.bar_chart(
            chart_data,
            height=260,
            color="#36A6A0",
        )

    # Aggregated Strengths & Areas for Improvement
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    c_str, c_opp = st.columns(2)

    with c_str:
        st.markdown(
            """
            <div style="background: rgba(85, 169, 135, 0.08); border: 1px solid rgba(85, 169, 135, 0.3); border-left: 4px solid #55A987;
                        border-radius: 12px; padding: 20px; min-height: 240px;">
                <h3 style="color:#55A987; margin-top:0; font-size:1.2rem;">🌟 Top Observed Strengths</h3>
            """,
            unsafe_allow_html=True,
        )
        seen_strengths = set()
        count = 0
        for ev in evaluations:
            for s in ev.strengths:
                if s not in seen_strengths and count < 6:
                    seen_strengths.add(s)
                    st.markdown(f"✅ {s}")
                    count += 1
        if count == 0:
            st.markdown("_No specific strengths recorded._")
        st.markdown("</div>", unsafe_allow_html=True)

    with c_opp:
        st.markdown(
            """
            <div style="background: rgba(215, 123, 105, 0.08); border: 1px solid rgba(215, 123, 105, 0.3); border-left: 4px solid #D77B69;
                        border-radius: 12px; padding: 20px; min-height: 240px;">
                <h3 style="color:#D77B69; margin-top:0; font-size:1.2rem;">🎯 Priority Growth Opportunities</h3>
            """,
            unsafe_allow_html=True,
        )
        seen_weaknesses = set()
        count = 0
        for ev in evaluations:
            for w in ev.weaknesses:
                if w not in seen_weaknesses and count < 6:
                    seen_weaknesses.add(w)
                    st.markdown(f"🔍 {w}")
                    count += 1
        if count == 0:
            st.markdown("_No major weaknesses detected. Keep up the high standard!_")
        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed Question Review Accordion
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.subheader("📝 Detailed Question-by-Question Review")

    for idx, (q, ev) in enumerate(zip(questions, evaluations), start=1):
        user_ans = user_answers.get(q.id, "_No answer submitted_")
        with st.expander(f"Question {idx} ({q.category}) — Score: {ev.score}/10 — {ev.verdict}", expanded=(idx == 1)):
            st.markdown(f"**Question:** {q.question}")
            st.markdown(f"**Target Competency:** _{q.expected_competency}_")
            
            st.markdown("**Your Answer:**")
            st.markdown(
                f"""
                <div style="background:#172728; padding:14px; border-radius:8px; 
                            border:1px solid #304747; border-left:4px solid #36A6A0; font-family:monospace; font-size:0.9rem; color:#F3F7F5;">
                    {user_ans}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Strengths:**")
                for s in ev.strengths:
                    st.markdown(f"- {s}")
            with col_b:
                st.markdown("**Areas to Improve:**")
                for w in ev.weaknesses:
                    st.markdown(f"- {w}")

            if ev.missing_points:
                st.markdown("**Key Missing Points:**")
                for mp in ev.missing_points:
                    st.markdown(f"- ❗ {mp}")

            st.markdown("**AI Improved Model Answer:**")
            st.markdown(
                f"""
                <div style="background:#172728; padding:16px; border-radius:8px; 
                            border:1px solid #36A6A0; color:#F3F7F5; font-size:0.92rem; line-height:1.6;">
                    {ev.improved_sample_answer}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Recommended Next Steps
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.subheader("🚀 Suggested Action Plan for Success")
    st.markdown(
        """
        1. **Master the STAR Method:** For behavioral and HR questions, structure answers strictly around **Situation, Task, Action, and Result**.
        2. **Explain Trade-offs:** In technical rounds, do not just offer one solution—mention time/space complexity, edge cases, and why you chose your specific approach.
        3. **Bridge Missing Points:** Review the missing points highlighted in this session and read up on the relevant architecture or language design patterns.
        4. **Repeat Mock Rounds:** Practice again with higher difficulty levels or different interview categories to build natural confidence under pressure.
        """
    )

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 28px 0;'>", unsafe_allow_html=True)

    # Action Buttons: Restart & Download
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("🔄 Start a New Interview Session", use_container_width=True, type="primary"):
            # Clear relevant session keys
            for key in ["interview_started", "questions", "current_question_index", "evaluations", "user_answers", "setup_config"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    with c_btn2:
        # Generate summary text for download
        report_lines = [
            f"# CareerPilot AI - Mock Interview Report",
            f"Role: {session_config.get('role')}",
            f"Experience Level: {session_config.get('experience_level')}",
            f"Interview Type: {session_config.get('interview_type')}",
            f"Average Score: {metrics['average_score']} / 10.0 ({metrics['tier']})",
            f"Questions Answered: {metrics['answered_count']} of {metrics['total_questions']}\n",
            "## Question Breakdown:",
        ]
        for idx, (q, ev) in enumerate(zip(questions, evaluations), start=1):
            report_lines.append(f"\n### Q{idx}: {q.question}")
            report_lines.append(f"Score: {ev.score}/10 ({ev.verdict})")
            report_lines.append(f"Candidate Answer:\n{user_answers.get(q.id, 'N/A')}")
            report_lines.append(f"\nStrengths:\n" + "\n".join(f"- {s}" for s in ev.strengths))
            report_lines.append(f"\nWeaknesses:\n" + "\n".join(f"- {w}" for w in ev.weaknesses))
            report_lines.append(f"\nImproved Model Answer:\n{ev.improved_sample_answer}\n")

        report_content = "\n".join(report_lines)
        st.download_button(
            label="📥 Download Full Interview Report (.md)",
            data=report_content,
            file_name=f"careerpilot_report_{session_config.get('role', 'interview').lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )
