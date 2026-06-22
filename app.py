import streamlit as st
from google import genai
from google.genai import types

# Set up visual web page configuration
st.set_page_config(page_title="Global Travel Concierge", page_icon="✈️", layout="wide")
st.title("✈️ Global Travel Concierge Agent")
st.markdown("---")

# Initialize Gemini Client safely
client = genai.Client()

# Initialize session memory states to remember data across button clicks
if "itinerary_text" not in st.session_state:
    st.session_state.itinerary_text = None
if "safety_text" not in st.session_state:
    st.session_state.safety_text = None

# =====================================================================
# PHASE 1: VISUAL SIDEBAR INPUT FORM Elements
# =====================================================================
with st.sidebar:
    st.header("📋 Travel Parameter Form")
    st.markdown("Fill in the fields below to plan your safe vacation.")
    
    destination = st.text_input("Destination City/Country", placeholder="e.g., Manali, Paris, Tokyo")
    origin = st.text_input("Origin City", placeholder="e.g., Mumbai, New York, London")
    dep_date = st.text_input("Departure Date/Month", placeholder="e.g., 5th May, October 12th")
    duration = st.text_input("Length of Stay (Days)", placeholder="e.g., 5, 7, 14")
    travelers = st.text_input("Number of Travelers", placeholder="e.g., 1, 3, 5")
    fitness = st.selectbox("Group Physical Fitness Level", ["Low", "Medium", "High"])
    
    st.markdown("---")
    generate_btn = st.button("🚀 Stage 1: Build Core Itinerary", use_container_width=True)
    
    # Second button is clickable only after Stage 1 finishes to prevent processing traffic jams
    safety_btn = st.button("🔍 Stage 2: Fetch Live Flights & Scam Reports", use_container_width=True, disabled=(st.session_state.itinerary_text is None))

# =====================================================================
# PHASE 2: TASK-SPLITTING EXECUTION WORKFLOW
# =====================================================================

# STAGE 1: CORE ITINERARY & REAL HOTELS
if generate_btn:
    if not (destination and origin and dep_date and duration and travelers):
        st.error("⚠️ All input form details are strictly mandatory. Please fill in the boxes in the sidebar.")
    else:
        with st.spinner("Analyzing destination metrics and traditional local properties..."):
            try:
                stage1_prompt = (
                    f"Build a custom travel plan for {travelers} travelers flying from {origin} to {destination} on {dep_date} staying for {duration} days. "
                    f"The group fitness level is {fitness}. Provide a list of real, specific hotel property names across three pricing tiers (Budget, Moderate, Luxury). "
                    f"List 2-3 unique, lesser-known hidden traditional gems and niche spots in a section titled '💎 UNEXPLORED TRADITIONAL GEMS & NICHE SPOTS'. "
                    f"Adjust activities to match their {fitness} fitness level. Do not look up flights or scams yet."
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=stage1_prompt,
                    config=types.GenerateContentConfig(temperature=0.2)
                )
                
                # Save results to memory and clear out any old Stage 2 reports
                st.session_state.itinerary_text = response.text
                st.session_state.safety_text = None
                st.rerun()
                
            except Exception as e:
                st.error("Connection hiccup while compiling core data. Please click the button to try again!")

# STAGE 2: FLIGHT GROUNDING & SCAM RADAR
if safety_btn:
    with st.spinner("Connecting to live web engines to scan flight channels and active scams..."):
        try:
            stage2_prompt = (
                f"Perform a live web search for current travel metrics for a trip from {origin} to {destination} around {dep_date}. "
                f"Task 1: Find current flight baseline price estimates for {travelers} people and provide direct markdown links to booking search engines like Google Flights. "
                f"Task 2: Search for common tourist traps, overpriced sectors, and traveler scams active in {destination} right now. Create a dedicated section titled '⚠️ CRITICAL TOURIST TRAPS & SCAM ALERTS' detailing these findings. "
                f"Task 3: Append a short 'Regional Cultural Etiquette' summary."
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=stage2_prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())], # Live Search active only here!
                    temperature=0.2
                )
            )
            
            st.session_state.safety_text = response.text
            st.rerun()
            
        except Exception as e:
            st.error("The search grounding task took too long to read live web nodes. Click Stage 2 to re-trigger the data retrieval!")

# =====================================================================
# PHASE 3: MAIN VIEW RENDER ENGINE
# =====================================================================
if st.session_state.itinerary_text:
    st.subheader("🗺️ Your Curated Traditional Itinerary & Property Tiers")
    st.markdown(st.session_state.itinerary_text)
    st.markdown("---")

if st.session_state.safety_text:
    st.balloons()
    st.subheader("🚨 Live Flight Routings & Scam Safety Analysis")
    st.markdown(st.session_state.safety_text)
elif st.session_state.itinerary_text:
    st.info("💡 Core Itinerary built successfully! Now, click the **Stage 2: Fetch Live Flights & Scam Reports** button inside the left sidebar to activate the live web search grounding tool safely.")
else:
    st.info("👋 Welcome to your Global Travel Concierge! Fill in your destination details in the left sidebar form and click **Stage 1** to compile your personalized vacation plan.")
