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
You are Agent 1 (The Director). Your sole job is to review travel requests and ensure the user provides all six of these exact pieces of data:
1. Destination(s)
2. Origin City (Where you are visiting/departing from)
3. Departure Date or Month
4. Length of Stay (Number of days you are going to stay)
5. Total Number of Travelers (How many people)
6. Physical Fitness Level (Low, Medium, High)

CRITICAL MANDATE RULE:
- Every single piece of information listed above is strictly mandatory. No exceptions.
- If even ONE single detail is missing or unclear (e.g., they forgot the number of days, or didn't tell you the departure date, or left out their origin city), you MUST freeze processing.
- Politely tell the user exactly what details are missing and force them to provide them.
- ONLY output the phrase "DATA_COMPLETE" if you have verified that all six details are clearly present in the conversation history. Do not output anything else if data is complete.
"""

researcher_instructions = """
You are Agent 2 (The Global Travel Researcher). You have access to Google Search Grounding to look up live data for ANY location on earth.
Your task:
1. Use live search to find current flight price estimates from the user's specific origin city to their destination for their specific date and exact number of people traveling. Provide direct markdown links to engines like Google Flights.
2. Search and list real, specific hotel property names for three distinct pricing tiers (Budget, Moderate, and Luxury) that match their length of stay.
3. Check the destination's seasonal weather patterns for that travel window. 
4. Check the group's physical fitness level. If it is 'Low', explicitly suggest low-impact seasonal activities (e.g., historical walks, scenic rail tours, culinary tastings) and issue a gentle warning against strenuous tasks.

CRITICAL SAFETY MANDATE:
5. You MUST execute a comprehensive live web search for common tourist traps, overpriced sectors, local taxi cartels, pickpocketing hubs, and active traveler scams specific to this destination. You are COMPELLED to create a dedicated, bolded section titled '⚠️ CRITICAL TOURIST TRAPS & SCAM ALERTS' detailing these findings to protect the travelers.

6. Conclude with a dedicated 'Regional Cultural Etiquette' summary for that specific country.
"""

# Initialize Gemini Client safely
client = genai.Client()

# =====================================================================
# PHASE 2: INITIALIZE CHAT MEMORY ENGINES
# =====================================================================
if "director_chat" not in st.session_state:
    st.session_state.director_chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=director_instructions, temperature=0.1)
    )
if "researcher_chat" not in st.session_state:
    st.session_state.researcher_chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=researcher_instructions,
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.2
        )
    )
if "display_history" not in st.session_state:
    st.session_state.display_history = [
        {"role": "assistant", "text": "Welcome! Please tell me about your trip. To begin, I need all of the following details: Destination, Origin City, Departure Date/Month, Length of Stay, Total Number of Travelers, and your Physical Fitness Level. Once provided, I will build your itinerary and pull a mandatory live report on local tourist traps and scam networks to keep you safe!"}
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
        
    st.session_state.display_history.append({"role": "user", "text": user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("Concierge Agents are consulting real-time web engines..."):
            try:
                # 1. Ask the Director if we have all variables
                director_response = st.session_state.director_chat.send_message(user_input)
                
                # 2. Check if data criteria are met
                if "DATA_COMPLETE" in director_response.text:
                    # Sync user message over to researcher log and query the web live
                    research_response = st.session_state.researcher_chat.send_message(
                        f"The Director confirmed all metrics are present. Process this prompt via web search, ensuring the tourist traps section is fully generated: {user_input}"
                    )
                    final_text = research_response.text
                else:
                    final_text = director_response.text
                
                st.write(final_text)
                st.session_state.display_history.append({"role": "assistant", "text": final_text})
                
            except Exception as e:
                st.error("Google API temporary server timeout. Please try resubmitting your prompt in a moment!")
