import streamlit as st
from google import genai
from google.genai import types

# Set up visual web page configuration
st.set_page_config(page_title="Global Travel Concierge", page_icon="✈️", layout="wide")
st.title("✈️ Global Travel Concierge Agent")
st.markdown("---")

# =====================================================================
# PHASE 1: AGENT RESEARCHER INSTRUCTIONS
# =====================================================================
researcher_instructions = """
You are the Global Travel Researcher Agent. You have access to Google Search Grounding to look up live data for ANY location on earth.
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
# PHASE 2: VISUAL SIDEBAR INPUT FORM (ELIMINATES PARSING BUGS)
# =====================================================================
with st.sidebar:
    st.header("📋 Travel Parameter Form")
    st.markdown("Please fill in every parameter below to generate your safe itinerary.")
    
    # Individual input boxes and dropdown elements
    destination = st.text_input("Destination City/Country", placeholder="e.g., Manali, Paris, Tokyo")
    origin = st.text_input("Origin City", placeholder="e.g., Mumbai, New York, London")
    dep_date = st.text_input("Departure Date/Month", placeholder="e.g., 5th May, October 12th")
    duration = st.text_input("Length of Stay (Days)", placeholder="e.g., 5, 7, 14")
    travelers = st.text_input("Number of Travelers", placeholder="e.g., 1, 3, 5")
    fitness = st.selectbox("Group Physical Fitness Level", ["Low", "Medium", "High"])
    
    st.markdown("---")
    generate_btn = st.button("🚀 Generate Live Itinerary", use_container_width=True)

# =====================================================================
# PHASE 3: MAIN DISPLAY MATRIX
# =====================================================================
if generate_btn:
    # 1. Validation Check right in Python code (Fast, completely local, no AI timeout)
    if not (destination and origin and dep_date and duration and travelers):
        st.error("⚠️ All input form details are strictly mandatory. Please fill in the missing boxes in the sidebar and try again!")
    else:
        with st.spinner("Concierge Agents are executing live web search grounding..."):
            try:
                # Compile a solid, flawless data profile to feed into the researcher agent
                consolidated_prompt = (
                    f"Create a complete travel plan for {travelers} travelers flying from {origin} to {destination} "
                    f"on {dep_date} staying for {duration} days. The group physical fitness level is {fitness}. "
                    f"Execute all grounding tasks including flight routing, real hotel property options, niche traditional gems, "
                    f"compulsory travel scam watchlists, and local etiquette reviews."
                )
                
                # Execute single low-latency content generation call with Google Search Grounding active
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=consolidated_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=researcher_instructions,
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        temperature=0.2
                    )
                )
                
                # Render the clean, beautiful markdown results right onto the center page area
                st.balloons()
                st.markdown(response.text)
                
            except Exception as e:
                st.error("The live search grounding sequence timed out. Please click the button to re-trigger the data retrieval panel!")
else:
    # Welcome banner shown before clicking generate
    st.info("👋 Welcome to the Global Travel Concierge application dashboard! Please fill in the parameters inside the left sidebar form panel and click the generate button to spawn your customized web-grounded itinerary report.")
