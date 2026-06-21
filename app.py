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
You are Agent 1 (The Director). Your sole job is to review travel requests and ensure the user provides five pieces of data:
1. Destination(s)
2. Origin City
3. Departure Date/Month & Length of Stay (Number of days)
4. Total Number of Travelers
5. Physical Fitness Level (Low, Medium, High)

If ANY of these five parameters are missing or unclear, you must ask for the missing details. 
If ALL five metrics are clearly present, output exactly: "DATA_COMPLETE" and nothing else.
"""

researcher_instructions = """
You are Agent 2 (The Global Travel Researcher). You have access to Google Search Grounding to look up live data for ANY location on earth.
Your task:
1. Use live search to find current flight price estimates from the origin to the destination for the exact number of people traveling. Provide direct markdown links to engines like Google Flights.
2. Search and list real hotel property names for three distinct pricing tiers (Budget, Moderate, and Luxury) matching the length of stay.
3. Check the destination's seasonal weather patterns for that travel window. 
4. Check the group's physical fitness level. If it is 'Low', explicitly suggest low-impact seasonal activities and issue a safety warning against strenuous tasks.
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
        {"role": "assistant", "text": "Welcome! Tell me about your dream vacation. Please include your destination, origin city, departure date, duration, travelers count, and fitness level."}
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
