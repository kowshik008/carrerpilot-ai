"""CareerPilot AI — Settings Module
==================================
Settings for configuring API keys, user profile defaults, and system diagnostics.
"""

import sys
import streamlit as st
from config import GEMINI_MODEL
from utils.gemini_helper import test_api_connection


def render_settings():
    """Render the Settings and Preferences view."""
    st.markdown(
        """
        <div class="cp-card" style="border-left: 4px solid #36A6A0; margin-bottom: 24px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 style="margin:0 0 6px 0; color:#F3F7F5; font-size:1.6rem; font-weight:700;">
                        ⚙️ Platform Settings & Preferences
                    </h2>
                    <p style="color:#A5B7B3; font-size:0.95rem; margin:0;">
                        Configure your AI credentials, model selection, and profile preferences.
                    </p>
                </div>
                <span class="cp-badge-teal">Preferences</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Section 1: Gemini API Credentials
    st.subheader("🔑 Google Gemini API Configuration")
    st.markdown(
        f"""
        <p style="color:#A5B7B3; font-size:0.9rem; margin-bottom:14px;">
            CareerPilot AI uses Google <strong style="color:#36A6A0;">{GEMINI_MODEL}</strong> for high-speed question generation, 
            multimodal audio transcription, and structured evaluations.
        </p>
        """,
        unsafe_allow_html=True,
    )

    current_key = st.session_state.get("api_key", "")
    new_key = st.text_input(
        "Gemini API Key",
        value=current_key,
        type="password",
        placeholder="AIzaSy...",
        help="Paste your Gemini API key from Google AI Studio.",
    )

    if new_key != current_key:
        st.session_state.api_key = new_key.strip()
        st.success("API Key updated in active session.")

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        if st.button("🔌 Test API Connection", use_container_width=True, type="primary"):
            if not st.session_state.get("api_key"):
                st.error("Please enter an API key.")
            else:
                with st.spinner("Connecting to Gemini API..."):
                    ok, msg = test_api_connection(st.session_state.api_key)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(f"Connection test failed: {msg}")
    with col_btn2:
        st.markdown(
            """
            <a href="https://aistudio.google.com/app/apikey" target="_blank" 
               style="text-decoration:none; display:inline-block; padding:10px 16px; 
                      background:#172728; border:1px solid #304747; border-radius:10px; 
                      color:#36A6A0; font-size:0.9rem; font-weight:600;">
                Get Free Gemini API Key from Google AI Studio ↗
            </a>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='border-color:#304747; margin:28px 0;'>", unsafe_allow_html=True)

    # Section 2: Model & Profile Preferences
    st.subheader("🎛️ AI Hyperparameters & Defaults")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.selectbox(
            "Default AI Model",
            options=["gemini-3.8-flash (Recommended)", "gemini-3.5-flash-lite", "gemini-3.5-flash"],
            index=0,
            help="Gemini 3.8 Flash provides state-of-the-art reasoning, low latency, and native audio support.",
        )
    with col_p2:
        st.selectbox(
            "Default Evaluation Strictness",
            options=["Standard Senior Hiring Manager", "Strict FAANG / Tier-1 Bar", "Supportive & Mentoring"],
            index=0,
        )

    st.markdown("<hr style='border-color:#304747; margin:28px 0;'>", unsafe_allow_html=True)

    # Section 3: Diagnostic Info
    st.subheader("🖥️ System Diagnostics")
    st.markdown(
        f"""
        <div style="background:#172728; border:1px solid #304747; border-radius:10px; padding:16px; font-size:0.85rem; color:#A5B7B3;">
            <div>• <strong>Python Version:</strong> {sys.version.split()[0]}</div>
            <div>• <strong>Streamlit Version:</strong> {st.__version__}</div>
            <div>• <strong>Theme Engine:</strong> CareerPilot Dark Teal (#101C1D / #172728 / #36A6A0)</div>
            <div>• <strong>Local Status:</strong> Server running on localhost:8501</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
