"""CareerPilot AI — Progress & History Module
===========================================
Tracks learning velocity, past interview rounds, scores, and readiness stats.
"""

import streamlit as st


def render_progress_history():
    """Render the Progress and History tracking page."""
    st.markdown(
        """
        <div class="cp-card" style="border-left: 4px solid #36A6A0; margin-bottom: 24px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 style="margin:0 0 6px 0; color:#F3F7F5; font-size:1.6rem; font-weight:700;">
                        📊 Progress & Performance History
                    </h2>
                    <p style="color:#A5B7B3; font-size:0.95rem; margin:0;">
                        Monitor your cumulative score trends, strengths evolution, and mock interview milestones.
                    </p>
                </div>
                <span class="cp-badge-teal">Analytics Tracker</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    evals = st.session_state.get("evaluations", [])
    questions = st.session_state.get("questions", [])

    # High-level Statistics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🎯 Total Questions Evaluated", len(evals))
    with c2:
        avg = round(sum(e.score for e in evals) / len(evals), 1) if evals else 0.0
        st.metric("⭐ Average Performance", f"{avg}/10" if evals else "—")
    with c3:
        peak = max([e.score for e in evals]) if evals else 0.0
        st.metric("🏆 Peak Answer Score", f"{peak}/10" if evals else "—")
    with c4:
        checked_tasks = len(st.session_state.get("roadmap_checked_tasks", set()))
        st.metric("🗺️ Completed Roadmap Tasks", checked_tasks)

    st.markdown("<hr style='border-color:#304747; margin:24px 0;'>", unsafe_allow_html=True)

    # Detailed Evaluation History Table
    st.subheader("📋 Session Answer Log")

    if evals and questions:
        for idx, (q, ev) in enumerate(zip(questions, evals), start=1):
            badge_cls = "cp-badge-success" if ev.score >= 8.0 else ("cp-badge-teal" if ev.score >= 6.0 else "cp-badge-error")
            badge_color = "#55A987" if ev.score >= 8.0 else ("#36A6A0" if ev.score >= 6.0 else "#D77B69")

            with st.expander(f"Question #{idx}: {q.question[:75]}... — {ev.score}/10", expanded=(idx == 1)):
                st.markdown(f"**Full Question:** {q.question}")
                st.markdown(f"**Category:** `{q.category}` | **Target Competency:** _{q.expected_competency}_")
                
                user_ans = st.session_state.get("user_answers", {}).get(q.id, "_Answer recorded_")
                st.markdown(
                    f"""
                    <div style="background:#172728; border:1px solid #304747; border-left:4px solid {badge_color}; 
                                border-radius:8px; padding:12px; margin:10px 0; font-family:monospace; font-size:0.88rem; color:#F3F7F5;">
                        {user_ans}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(f"**Verdict:** <span class='{badge_cls}'>{ev.verdict}</span>", unsafe_allow_html=True)
                st.markdown(f"**Model Answer:** {ev.improved_sample_answer}")
    else:
        st.markdown(
            """
            <div class="cp-card" style="text-align:center; padding:32px;">
                <p style="color:#A5B7B3; font-size:1.0rem; margin:0 0 12px 0;">
                    No practice sessions logged yet. Head over to <strong>Mock Interviewer</strong> to complete your first session!
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Clear History Action
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Reset Session History", type="secondary"):
        for key in ["evaluations", "user_answers", "questions", "interview_started", "interview_completed"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Session history reset.")
        st.rerun()
