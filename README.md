# 🎯 CareerPilot AI — Navigate Your Future.

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.15-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-155E63.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-3.8%20Flash-36A6A0.svg)](https://ai.google.dev/)
[![Theme](https://img.shields.io/badge/Theme-Dark%20Teal%20%23101C1D-101C1D.svg)](styles/theme.css)
[![License: MIT](https://img.shields.io/badge/License-MIT-55A987.svg)](LICENSE)

> **Product:** CareerPilot AI  
> **Tagline:** *Navigate Your Future.*  
> An intelligent career-tech platform designed with a premium, human-centered dark theme. Features an AI-powered Mock Interviewer, Smart Resume Analyzer, and Personalized Career Roadmap powered by **Google Gemini 3.8 Flash**.

---

## 🎨 Exact Dark Color Palette

CareerPilot AI uses a cohesive, custom-engineered dark teal palette throughout:

| Token | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Main Background** | `#101C1D` | Global canvas and base background |
| **Secondary Background** | `#172728` | Sidebar, input fields, and tab bars |
| **Card Background** | `#203536` | Elevated cards, metric containers, and expanders |
| **Primary Teal** | `#155E63` | Primary action buttons and badges |
| **Accent Teal** | `#36A6A0` | Highlights, active navigation, focus rings, links |
| **Soft Mint** | `#A9C9BD` | Subtle badges, secondary accents |
| **Primary Text** | `#F3F7F5` | High-contrast headings and readable body text |
| **Secondary Text** | `#A5B7B3` | Muted labels, timestamps, and subtitles |
| **Borders** | `#304747` | Clean card outlines and dividers |
| **Success** | `#55A987` | High scores, positive indicators, completed tasks |
| **Warning** | `#E4B35E` | Medium scores, tips, alerts |
| **Error / Accent** | `#D77B69` | Low scores, growth areas, missing keywords |

---

## 📖 Table of Contents
1. [Project Overview](#-project-overview)
2. [Problem Statement Addressed](#-problem-statement-addressed)
3. [Key Features](#-key-features)
4. [Technology Stack](#-technology-stack)
5. [Application Architecture & File Structure](#-application-architecture--file-structure)
6. [Design System](#-design-system)
7. [Installation & Setup Guide](#-installation--setup-guide)
8. [Configuring the Gemini API Key](#-configuring-the-gemini-api-key)
9. [Running the Application](#-running-the-application)
10. [End-to-End Workflow & User Journey](#-end-to-end-workflow--user-journey)
11. [Testing & Quality Assurance](#-testing--quality-assurance)
12. [Streamlit Community Cloud Deployment](#-streamlit-community-cloud-deployment)
13. [GitHub Submission Instructions](#-github-submission-instructions)
14. [Limitations & Future Roadmap](#-limitations--future-roadmap)

---

## 🌟 Project Overview

**CareerPilot AI** bridges the gap between theoretical knowledge and interview readiness. Job seekers and students often struggle with the pressure, ambiguity, and technical articulation demanded in live interviews. CareerPilot AI acts as an always-available, objective technical interviewer and hiring manager that:
- Generates dynamic, role-tailored questions at Beginner, Intermediate, or Senior levels.
- Accepts both typed responses and voice recordings.
- Uses **Google Gemini 3.8 Flash** with structured Pydantic schema validation for objective, multi-criteria evaluations.
- Pinpoints omitted concepts, provides actionable improvement tips, and generates exemplary benchmark answers.
- Aggregates performance in a post-interview analytics dashboard with interactive charts and downloadable markdown reports.

---

## 🎯 Problem Statement Addressed

This project is built strictly to fulfill **Problem Statement 2: AI Mock Interviewer**.  
Per the assignment criteria, this project maintains strict focus on the mock interview lifecycle and intentionally omits unrelated modules like Resume Analyzers or Career Roadmaps to maximize depth and polish.

---

## ⚡ Key Features

| Feature | Description |
| :--- | :--- |
| **Intelligent Setup** | Select from pre-configured industry roles (Python Developer, AI Engineer, Data Analyst, etc.) or enter custom roles. Choose experience level (Beginner, Intermediate, Advanced) and interview format (Technical, HR/Behavioral, Mixed). |
| **Dynamic Question Engine** | Leverages Gemini to synthesize realistic, non-repetitive interview prompts matching exact experience calibration and competencies. |
| **Dual Answer Modalities** | Answer via formatted **Text Input** or **Voice Input** using native microphone recording (`st.audio_input`). |
| **Native Multimodal Speech-to-Text** | Spoken audio is transcribed directly using Gemini’s native multimodal audio capabilities—eliminating complex external C-binaries (like FFmpeg). Users can inspect, edit, and refine the transcription before submission. |
| **Objective 5-Point Evaluation Rubric** | Scores answers from 0.0 to 10.0 across: Relevance, Technical Correctness, Communication Clarity, and Completeness. |
| **Concrete Strengths & Growth Areas** | Categorized bullet points showing exactly what was done well versus critical industry concepts omitted. |
| **Exemplary Model Answer** | Generates an AI-crafted high-scoring answer illustrating how an ideal candidate would frame the response. |
| **Analytics Dashboard** | Displays overall average, peak score, tier badge, bar chart score distribution, question review accordions, and downloadable report. |

---

## 🛠️ Technology Stack

- **Language:** Python 3.10+ (tested on Python 3.15.2)
- **Web UI Framework:** Streamlit (v1.40+)
- **Large Language Model & SDK:** Google Gemini 3.8 Flash via official `google-genai` (v2.34+)
- **Data Validation & Schemas:** Pydantic v2
- **Environment Management:** `python-dotenv`
- **Data Handling:** Native Python data structures (`dict`, `list`, `dataclass`) for cross-platform stability
- **Styling:** Centralized stylesheet (`styles/theme.css`) with custom CSS selectors and Inter typography

---

## 📂 Application Architecture & File Structure

```text
career_pilot_ai/
│
├── app.py                      # Application controller, sidebar navigation & session routing
├── requirements.txt            # Python dependencies (Streamlit, google-genai, python-dotenv, pydantic)
├── .env.example                # Safe environment variable template
├── .gitignore                  # Git ignore rules (secrets, venv, pycache)
├── README.md                   # Comprehensive documentation
├── VIVA_PREPARATION.md         # Viva guide, code breakdown & 20 Q&As
├── careerpilot_ai_submission.zip # Ready-to-submit archive
│
├── .streamlit/
│   └── config.toml             # Theme settings (base dark, teal primary, #101C1D background)
│
├── styles/
│   └── theme.css               # Centralized Dark Teal stylesheet (cards, inputs, badges, buttons)
│
├── modules/
│   ├── __init__.py             # Modules namespace
│   ├── dashboard.py            # Welcome overview, student profile, KPI metrics & quick actions
│   ├── resume_analyzer.py      # ATS match scoring, keyword extraction & section critique
│   ├── interview_setup.py      # Setup form rendering & input validation
│   ├── question_generator.py   # AI prompt orchestration & Pydantic question schemas
│   ├── answer_evaluator.py     # 5-pillar rubric scoring & structured JSON parsing
│   ├── results_dashboard.py    # Analytics, metrics calculation & report generator
│   ├── career_roadmap.py       # 4-phase milestone timeline with interactive task checklists
│   ├── progress_history.py     # Cumulative evaluation tracking & session logs
│   └── settings_view.py        # Gemini API credentials, connection tester & preferences
│
├── utils/
│   ├── __init__.py             # Utilities namespace
│   ├── gemini_helper.py        # Gemini client wrapper, error handling & structured output
│   └── voice_helper.py         # Audio buffer ingestion & transcription dispatcher
│
└── tests/
    └── test_interview.py       # Automated unit test suite (12 test cases)
```

---

## 🎨 Design System

CareerPilot AI follows a SaaS-grade design direction:
- **Main Background:** Deep Obsidian Teal (`#101C1D`)
- **Secondary Surface:** Slate Teal (`#172728`)
- **Card Background:** Elevated Forest Teal (`#203536`)
- **Primary Teal:** Deep Accent (`#155E63`)
- **Accent Teal:** Vibrant Mint Highlight (`#36A6A0`)
- **Soft Mint:** Secondary Badge Accent (`#A9C9BD`)
- **Primary Typography:** Crisp Off-White (`#F3F7F5`)
- **Secondary Typography:** Muted Sage (`#A5B7B3`)
- **Borders:** Clean Structural Slate (`#304747`)
- **Success:** Soft Jade (`#55A987`)
- **Warning:** Amber Gold (`#E4B35E`)
- **Error / Growth:** Coral Terracotta (`#D77B69`)
- **Spacing & Elevation:** Rounded borders (8px–14px), subtle box-shadows, and high-contrast accessibility.

---

## 🚀 Installation & Setup Guide

### 1. Clone or Extract the Project
```bash
git clone https://github.com/your-username/careerpilot-ai.git
cd "career pilot ai"
```

### 2. Create and Activate a Python Virtual Environment (Recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Required Dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 🔑 Configuring the Gemini API Key

You can obtain a 100% free API key from **Google AI Studio**:
1. Visit [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).
2. Sign in with your Google Account and click **"Create API Key"**.
3. Configure the key in the project using **either** of these two methods:

### Method A: Local `.env` File (Recommended for Local Dev)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` in any text editor and paste your key:
```ini
GEMINI_API_KEY=AIzaSyYourActualKeyHere12345
```

### Method B: Directly in the Web UI Sidebar
If you prefer not to touch `.env`, simply launch the app and paste your key into the **"Gemini API Key"** input box in the left sidebar! You can click **"🔌 Verify Key"** to confirm connectivity in real time.

---

## 💻 Running the Application

Run the following command from the root project directory:
```bash
python -m streamlit run app.py
```

Streamlit will launch local server instances:
- **Local URL:** `http://localhost:8501`
- **Network URL:** `http://<your-ip>:8501`

Open `http://localhost:8501` in your web browser.

---

## 🔄 End-to-End Workflow & User Journey

1. **Step 1: Setup:** Select your target role (e.g., *Python Developer*), experience level (*Intermediate*), interview type (*Mixed*), and question count (*5*).
2. **Step 2: Question Generation:** Click *Generate Interview Questions*. Gemini produces calibrated questions adhering to the Pydantic schema.
3. **Step 3: Answer Submission:**
   - **Text Mode:** Type your response in the provided text area.
   - **Voice Mode:** Click the microphone icon to record your answer. Click *Transcribe Audio* to inspect Gemini’s speech-to-text transcript. Make any corrections, then submit.
4. **Step 4: AI Evaluation:** Gemini reviews the response against relevance, technical correctness, clarity, and completeness. You receive an instant score out of 10, identified strengths, growth areas, missing concepts, and an improved benchmark answer.
5. **Step 5: Question Progression:** Click *Next Question ➡️* to advance through all questions.
6. **Step 6: Results Dashboard:** Review your aggregate score, performance tier, question bar chart, collective strengths, and download the full `.md` report.

---

## 🧪 Testing & Quality Assurance

A dedicated unit test suite is included in `tests/test_interview.py` covering:
- Setup input validation rules (empty roles, negative/excess question counts).
- User answer validation (rejecting empty or low-effort submissions).
- Pydantic schema integrity for `InterviewQuestion`, `QuestionSet`, and `EvaluationResult`.
- Metric calculations (averages, peak/lowest score, tier assignment).
- Safe failure handling when no API key is supplied.

To execute the tests:
```bash
python -m unittest tests/test_interview.py
```
*Expected Result:*
```text
..........
Ran 10 tests in 0.006s
OK
```

---

## ☁️ Streamlit Community Cloud Deployment

To deploy this app publicly for college evaluation:
1. Push your code to a public or private GitHub repository (ensure `.env` is NOT committed!).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **"New app"**.
4. Select your repository, branch (`main`), and set the main file path to `app.py`.
5. Under **"Advanced settings..."**, click **"Secrets"** and enter:
   ```toml
   GEMINI_API_KEY = "your-actual-gemini-api-key"
   ```
6. Click **"Deploy!"**. Your application will be live with a shareable public URL.

---

## 📦 GitHub Submission Instructions

```bash
# Initialize git repository
git init

# Add all files (the .gitignore automatically ignores .env and caches)
git add .

# Create initial commit
git commit -m "feat: complete CareerPilot AI mock interview platform"

# Link to your remote GitHub repository
git remote add origin https://github.com/<your-username>/careerpilot-ai.git
git branch -M main
git push -u origin main
```

---

## ⚠️ Limitations & Future Roadmap

### Current Version Limitations
- Requires an active internet connection to communicate with Google Gemini APIs.
- Voice transcription requires an active microphone with browser permissions enabled.
- API rate limits are bound by the user's Google AI Studio quota tier.

### Future Roadmap
- Integration with live video / facial expression feedback via WebRTC.
- Historical user profile storage and progress tracking across multiple interview sessions.
- Company-specific interview question sets (e.g., Google, Amazon, Microsoft style rounds).
- Export to PDF with graphical score badges.
