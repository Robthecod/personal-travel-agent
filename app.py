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
You are Agent 1 (The Director). Your sole job is to review the consolidated user travel profile provided and ensure it contains all six of these exact pieces of data:
1. Destination(s)
2. Origin City (Where you are visiting/departing from)
3. Departure Date or Month
4. Length of Stay (Number of days you are going to stay)
5. Total Number of Travelers (How many people)
6. Physical Fitness Level (Low, Medium, High)

CRITICAL MANDATE RULE:
- Read the text carefully. If ANY of these six pieces are missing or marked as 'None', you must output a polite message listing EXACTLY what specific details are still missing.
- ONLY output the phrase "DATA_COMPLETE" if all six fields have valid data filled in. Do not output anything else if data is complete.
"""

researcher_instructions = """
You are Agent 2 (The Global Travel Researcher). You have access to Google Search Grounding to look up live data for ANY location on earth.
Your task:
1. Use live search to find current flight price estimates from the user's specific origin city to their destination for their specific date and exact number of people traveling. Provide direct markdown links to engines like Google Flights.
2. Search and list real, specific hotel property names for three distinct pricing tiers (Budget, Moderate, and Luxury) that match their length of stay.
3. Check the destination's seasonal weather patterns for that travel window. 

CRITICAL TRADITIONAL EXPERIENCE MANDATE:
4. You MUST search for unique, lesser-known, non-mainstream niche tourist spots and hidden traditional gems specific to this destination that regular tourists bypass. List at least 2-3 of these spots in a dedicated section titled '💎 UNEXPLORED TRADITIONAL GEMS & NICHE SPOTS'.
5. Check the group's physical fitness level. If it is 'Low', explicitly suggest low-impact seasonal activities matching these niche areas and issue a gentle warning against strenuous tasks.

CRITICAL SAFETY MANDATE:
6. You MUST execute a comprehensive live web search for common tourist traps, overpriced sectors, local taxi cartels, pickpocketing hubs, and active traveler scams specific to this destination. You are COMPELLED to create a dedicated, bolded section titled '⚠️ CRITICAL TOURIST TRAPS & SCAM ALERTS' detailing these findings to protect the travelers.

7. Conclude with a dedicated 'Regional Cultural Etiquette' summary for that specific country.
"""

# Initialize Gemini Client safely
client = genai.Client()

# =====================================================================
# PHASE 2: STREAMLIT ADVANCED CONTEXT SLOTS
# =====================================================================
# Initialize memory logs for the visual page display
if "display_history" not in st.session_state:
    st.session_state.display_history = [
        {"role": "assistant", "text": "Welcome! Please tell me about your trip. To begin, I need all of the following details: Destination, Origin City, Departure Date/Month, Length of Stay, Total Number of Travelers, and your Physical Fitness Level. You can give them to me all at once or separate them across multiple messages!"}
    ]

# Render prior message logs cleanly onto the screen
for msg in st.session_state.display_history:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

# =====================================================================
# PHASE 3: PARAMETER AGGREGATION MOTOR
# =====================================================================
if user_input := st.chat_input("Type your travel details here..."):
    with st.chat_message("user"):
        st.write(user_input)
        
    st.session_state.display_history.append({"role": "user", "text": user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("Concierge Agents are updating your travel profile..."):
            try:
                # We ask Gemini to parse the new user message and extract any travel variables it can find
                extractor_prompt = f"""
                Analyze the following user input and extract any travel parameters present.
                User Input: "{user_input}"
                
                Respond by updating this template form. If a value isn't mentioned in the text, leave it exactly as 'None'. Do not assume or guess values:
                Destination: 
                Origin: 
                Date: 
                Duration: 
                Travelers: 
                Fitness: 
                """
                
                extraction = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=extractor_prompt,
                    config=types.GenerateContentConfig(temperature=0.0)
                )
                
                # Combine the extraction history text into a running profile string
                if "running_profile" not in st.session_state:
                    st.session_state.running_profile = ""
                
                st.session_state.running_profile += f"\nNew details found:\n{extraction.text}"
                
                # 1. Evaluate total accumulated profile metrics using the Director Agent
                director_response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=st.session_state.running_profile,
                    config=types.GenerateContentConfig(
                        system_instruction=director_instructions,
                        temperature=0.1,
                    )
                )
                
                # 2. Condition Handoff to Web Grounding Engine
                if "DATA_COMPLETE" in director_response.text:
                    research_response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"Generate the full search itinerary using this completed user profile:\n{st.session_state.running_profile}",
                        config=types.GenerateContentConfig(
                            system_instruction=researcher_instructions,
                            tools=[types.Tool(google_search=types.GoogleSearch())],
                            temperature=0.2
                        )
                    )
                    final_text = research_response.text
                    # Reset the profile collector once the final itinerary is successfully built
                    st.session_state.running_profile = ""
                else:
                    final_text = director_response.text
                
                st.write(final_text)
                st.session_state.display_history.append({"role": "assistant", "text": final_text})
                
            except Exception as e:
                st.error("The search extraction task encountered a processing delay. Please try resubmitting your parameters slightly differently!")
