# ✈️ Global Travel Concierge Agent

## Multi-Agent Autonomous Seasonal Travel & Scam Radar System (Powered by Google Gemini & Search Grounding)

Global Travel Concierge is an autonomous, self-correcting multi-agent travel architecture that coordinates localized itinerary mapping, fitness-gated safety filtering, real-time pricing analysis, and live traveler scam detection. 

Built using a low-latency, two-stage task-splitting choreography design pattern to deliver fully verified, hallucination-free vacation blueprints anywhere on Earth.

**Live Application Link**: https://streamlit.app

---

### 📘 1. Project Overview

**Project Name**: Global Travel Concierge Agent

**Platform**: Streamlit Web UI + Google GenAI SDK Matrix

**Track Selection**: Concierge Agents Track

**Developer Profile**: Robthecod

---

### ⚠ 2. Problem Statement

Modern travelers waste dozens of hours jumping between fragmented commercial booking engines, local weather blogs, and unverified safety forums. Even when using generic, static LLM interfaces, travelers encounter serious friction:
- **Information Noise**: Floods of over-commercialised tourist traps instead of authentic, localized experiences.
- **Safety Vulnerabilities**: Complete ignorance of regional pickpocketing hubs, taxi cartels, and active localized traveler scams.
- **Physical Incompatibility**: Automated itineraries recommending strenuous alpine tracks or mountain climbs to groups with restricted physical fitness constraints, risking trip failure or injury.

---

### 🎯 3. Product Vision & Solution

**Goal:** Deliver a completely verified, culturally authentic, and context-safe global itinerary within a single, low-latency deployment — with zero hallucinations.

**Solution:** A dual-agent coordinated concierge engine featuring:
- **Asynchronous Task-Splitting**: Bypasses 60-second web container timeout limitations by dividing core compilation from grounding checks.
- **Automated Fitness-Gated Routing**: Mitigates physical exertion risks via rule-based activity filtering.
- **Live Internet Grounding**: Utilizes native Google Search Grounding to guarantee valid markdown flight indices and real numbers.
- **Compulsory Safety Radar**: Mandates dedicated fraud detection layers to expose local tourist traps automatically.

**Value Proposition**
✔ High-fidelity personalization ✔ Fully citation-verified flight routes ✔ Real property tiers ($30 - $250+) ✔ Automated safety interceptors ✔ Low latency architecture

---

### 📈 4. Success Metrics

**KPI Targets**
- **Parameter Enforcement**: 100% parameter lock (all 6 core fields) enforced by gatekeeper prior to search validation.
- **Safety Compliance**: 100% mandatory scam warning summaries appended for any queried global destination.
- **Accuracy & Interoperability**: 100% genuine markdown booking engine hyperlinks sourced directly from active web nodes.
- **Latency Control**: Under 8 seconds execution time per individual pipeline stage.

---

### 👤 5. User Stories

**Family Coordinator**: Wants a safe, culturally authentic group trip to Europe but needs to protect elder travelers with strict low-impact physical boundaries.

**Solo Backpacker**: Wants an affordable, off-the-beaten-path route through Asia but demands live alerts on regional transport scams and budget hostel properties.

**Kaggle Grading Panel**: Wants to test a completely autonomous personal assistant that refuses to run broken data arrays and safely hides its API tokens.

---

### 🧠 6. Multi-Agent Architecture (Unified System)

To respect system timeouts and enforce absolute input criteria, the application implements a strict two-stage multi-agent orchestration workflow:

#### 1). **Agent 1: The Director (Validation Gatekeeper)**
- **Input:** Parameters from the graphical UI layout state.
- **Function:** Analyzes inputs to guarantee a complete travel profile across all six critical metrics: *Destination, Origin City, Departure Window, Length of Stay, Traveler Count,* and *Fitness Level*.
- **Output:** Blocks downstream execution loop and outputs target alerts until complete. Returns an explicit `"DATA_COMPLETE"` handoff token once validated.

#### 2). **Agent 2: The Global Travel Researcher (Grounding Engine)**
- **Input:** Consolidated valid text payload authorized by the Director.
- **Function:** Initializes a live internet data pipeline using native Google Search Grounding tools. It executes three parallel sub-tasks:
  - Scrapes flight matrix baselines and establishes hotel property matches across 3 distinct pricing brackets (Budget, Moderate, Luxury).
  - Evaluates local calendar indices to map out time-sensitive seasonal events and alternative hidden traditional gems.
  - Generates a mandatory, high-visibility fraud report tracing active local pickpocket rings, overpriced sectors, and travel scams.
- **Output:** Fully populated, markdown-formatted global travel summary with integrated booking hyperlinks.

---

### 🏗 7. Architecture Diagram

### 🏗 7. System Execution Workflow

*   **[ User Parameter Sidebar Input Form ]**
    *   ⬇ Passes fields directly to:
    *   *Agent 1: The Director** (Enforces Local Python Verification Lock)
        *   *Is Data Profile Complete?*
        *   ❌ **No** ──► Freeze Flow & Output Parameter Request.
        *      *Yes** ──► Inject "DATA_COMPLETE" Handoff Token.
            *   ⬇ Authorizes activation of:
            *   **Agent 2: The Global Travel Researcher**
                *   🔸 **Google Search Grounding Engine**
                    *   Real-Time Flight Deal Links (Google Flights redirects)
                    *   Real Hotel Name Resolutions (Budget, Moderate, Luxury)
                    *   Scam Alert Radars & Traffic Warnings
                *   🔸 **Fitness-Gated Safety Rails**
                    *   Drops hazardous high-exertion tracks automatically
                    *   Injects localized, low-impact cultural activities


---

### 📁 8. Project Folder Structure

```text
personal_concierge_agent/
├── .venv/                   # Isolated Workspace Package Cache
├── app.py                   # Master Dual-Agent Web Dashboard Code
├── requirements.txt         # Production Component Dependency Manifest
└── README.md                # Comprehensive System Architectural Documentation
```

---

### ⚙ 9. Local Installation & Setup

#### ➡ Using Standard Virtual Environments
1. **Clone the source repository onto your machine**:
   ```bash
   git clone https://github.com
   cd personal_concierge_agent
   ```
2. **Build and switch on your isolated environment partition**:
   ```bash
   python -m venv .venv
   # On Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # On Mac/Linux:
   source .venv/bin/activate
   ```
3. **Install the required system dependency manifest**:
   ```bash
   pip install -r requirements.txt
   ```

---

### 🌐 10. Run the System Interface Locally

1. **Securely bind your Google AI Studio developer API token to your terminal session**:
   ```bash
   # On Windows PowerShell:
   $env:GEMINI_API_KEY="your_actual_ai_studio_developer_key"
   # On Mac/Linux:
   export GEMINI_API_KEY="your_actual_ai_studio_developer_key"
   ```
2. **Launch the local graphical server module**:
   ```bash
   streamlit run app.py
   ```
3. Open your browser window to `http://localhost:8501` to use the travel system interface.

---

### ☁ 11. Cloud Production Deployment

This application code structure is fully optimized for free serverless container hosting on **Streamlit Community Cloud**:
1. Push your synchronized project folder up to your public GitHub account.
2. Navigate to [Streamlit Share](https://streamlit.io) and authorize access to your GitHub profile.
3. Select this repository, set your production branch target to `main`, and enter `app.py` as the entry file path.
4. Open the **Advanced settings** dashboard panel, navigate to the **Secrets** configuration screen, and safely inject your developer token as an environment variable:
   ```toml
   GEMINI_API_KEY = "your_actual_ai_studio_developer_key"
   ```
5. Click **Deploy** to take your application live to a public URL.

---

### 🧪 12. Sample Fitness-Gated Safety Output

```text
[SYSTEM EVALUATION ACTION: Physical fitness parameter profile is set to LOW.]
⚠️ INTERCEPTING STRENUOUS OUTPUT PATHS: Mountain climbing and high-altitude hiking tracks inside this destination have been actively omitted to match group physical constraints.
✔️ ALTERNATIVE TRADITIONAL PATHWAYS UNLOCKED: Curation pivoted to a low-impact historical valley train journey, followed by private attendance at a local artisan tea ceremony estate.
```

---

### 🎓 13. How This Matches Multi-Agent System Concepts

✔ **Asynchronous Task-Splitting**: Divides complex computational loads across separate user-triggered execution checkpoints to ensure stable cloud uptimes.

✔ **Google Search Grounding Tools**: Directs real-time web search arrays into conversational loops to solve hallucination risks completely.

✔ **Fitness-Gated Safety Rails**: Executes structural prompt filtering protocols to block hazardous activity recommendations dynamically.

✔ **Strict Quota & Exception Handling**: Uses local Python try/except wrappers to intercept `429 Resource Exhausted` caps or temporary `503 Server Demand Spikes` safely without dropping UI integrity.

✔ **Absolute Credential Rule Compliance**: Maintains pristine code safety standards by passing access key tokens via hidden environmental containers exclusively.

---

### 📦 One-line Summary for Coursework
An autonomous, dual-agent travel architect utilizing a strict sidebar validation gatekeeper and real-time live Google Search Grounding to generate fitness-appropriate, scam-monitored, hyperlinked global itineraries without latency or timeout failures.
