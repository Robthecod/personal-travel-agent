import streamlit as st
from google import genai
from google.genai import types

# Set up visual web page configuration
st.set_page_config(page_title="Global Travel Concierge", page_icon="✈️", layout="centered")
st.title("✈️ Global Travel Concierge Agent")
st.markdown("---")

# =====================================================================
# PHASE 1: AGENT SYSTEM RULES AND INSTRUCTIONS
# =====================================================================
director_instructions = """
You are Agent 1 (The Director). Your sole job is to review travel requests and ensure the user provides three core metrics:
1. Destination(s)
2. Total Number of Travelers
3. Physical Fitness Level (Low, Medium, High)

CRITICAL RULE FOR TIMING/DATES:
- Specific departure and arrival dates are COMPLETELY OPTIONAL. Do not force the user to provide exact dates.
- If the user provides a general season (like 'Autumn' or 'Summer'), or provides no time frame at all, accept the input.
- ONLY freeze processing if the Destination, Traveler Count, or Fitness Level are missing.
- If those three core metrics are present, output exactly: "DATA_COMPLETE" and nothing else.
"""

researcher_instructions = """
You are Agent 2 (The Global Travel Researcher). You have access to Google Search Grounding to look up live data for ANY location on earth.
Your task:
1. Analyze the timing context provided by the user. If they specified a concrete date, search flights for that date. If they named a general season (e.g., Autumn), find optimal travel months for that season. If they provided NO timing parameter, default your calculations to the upcoming 1-2 months from today (June 2026).
2. Use live search to find current estimated flight baseline pricing routes from a logical global hub (or their origin if stated) to the destination. Provide direct markdown links to search engines like Google Flights.
3. List real, specific hotel property names for three distinct pricing tiers (Budget, Moderate, and Luxury).
4. Evaluate the group's physical fitness level. If it is 'Low', explicitly suggest low-impact seasonal activities (e.g., historical walks, scenic rail tours, culinary tastings) and issue a gentle warning against strenuous tasks.
5. Conclude with a dedicated 'Regional Cultural Etiquette' summary for that specific country.
"""

# Initialize Gemini Client safely
client = genai.Client()

# =====================================================================
# PHASE 2: STREAMLIT STATEFUL MEMORY RETENTION
# =====================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "display_history" not in st.session_state:
    st.session_state.display_history = [
        {"role": "assistant", "text": "Welcome! Tell me about your dream vacation. Just let me know your destination, how many people are coming, and your group's fitness level. (Dates and flight origins are completely optional!)"}
    ]

# Render prior message logs cleanly onto the screen
for msg in st.session_state.display_history:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

# =====================================================================
# PHASE 3: MULTI-AGENT EXECUTION ENGINE
# =====================================================================
if user_input := st.chat_input("Type your travel details here..."):
    # Render user prompt visually
    with st.chat_message("user"):
        st.write(user_input)
        
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": user_input}]})
    st.session_state.display_history.append({"role": "user", "text": user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("Concierge Agents are consulting real-time web engines..."):
            
            # 1. Run Director Agent
            director_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=st.session_state.chat_history,
                config=types.GenerateContentConfig(system_instruction=director_instructions, temperature=0.1)
            )
            
            # 2. Condition-Based Handoff to Researcher Agent
            if "DATA_COMPLETE" in director_response.text:
                research_response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=st.session_state.chat_history,
                    config=types.GenerateContentConfig(
                        system_instruction=researcher_instructions,
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        temperature=0.2
                    )
                )
                final_text = research_response.text
            else:
                final_text = director_response.text
            
            # Output final result to page
            st.write(final_text)
            
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": final_text}]})
    st.session_state.display_history.append({"role": "assistant", "text": final_text})
