import streamlit as st
import requests
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent
from PIL import Image

# -------------------------
# STREAMLIT SETUP
# -------------------------
st.set_page_config(page_title="AI Travel Planner", page_icon="🌍")

st.markdown("""
<style>
.big-title { font-size: 55px; font-weight: 900; text-align: center;
background: linear-gradient(to right, #00eaff, #5e00ff); -webkit-background-clip: text; color: transparent; }
.glass-box { background: rgba(255, 255, 255, 0.15); padding: 25px; border-radius: 20px;
box-shadow: 0px 8px 25px rgba(0,0,0,0.1); backdrop-filter: blur(12px); }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'> TRIPVERSE </div>", unsafe_allow_html=True)

st.markdown("""
<style>
.glass-card {
    padding: 12px 25px;
    font-size: 22px;
    font-weight: 700;
    color: white;
    border-radius: 15px;
    background: rgba(0, 34, 68, 0.5);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 140, 255, 0.4);
    text-align: center;
    max-width: 400px;
    margin: 20px auto;
}
.gradient-text {
    background: linear-gradient(to right, #00eaff, #5e00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>

<div class="glass-card">
    🌟 <span class="gradient-text">Plan Smarter, Travel Better</span> 🌟
</div>
""", unsafe_allow_html=True)

# -------------------------
# API KEYS
# -------------------------
st.sidebar.subheader("🔐 Enter Your API Keys")
tavily_key = st.sidebar.text_input("Tavily API Key", type="password")
gemini_key = st.sidebar.text_input("Gemini API Key", type="password")

if not tavily_key or not gemini_key:
    st.sidebar.warning("Please enter both API keys to continue.")
    st.stop()

# -------------------------
#  TOOLS
# -------------------------

def web_search(query: str) -> str:
    """Search the web using Tavily"""
    client = TavilyClient(api_key=tavily_key)
    res = client.search(query=query, max_results=5)
    text = ""
    for r in res.get("results", []):
        text += r.get("content", "") + "\n\n"
    return text



def get_weather(city: str) -> str:
    """Fetch clean weather info text (not JSON)."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=38256733f0cfc980a07f4163097f8d28&units=metric"
    data = requests.get(url).json()

    try:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].title()
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
    except:
        return "Weather data not available."

    return (
        f"🌤️ **Weather in {city}:**\n"
        f"• Temperature: {temp}°C\n"
        f"• Condition: {desc}\n"
        f"• Humidity: {humidity}%\n"
        f"• Wind Speed: {wind} m/s\n"
    )



def get_hotels(city: str) -> str:
    """Fetch hotel details in clean format."""
    raw = web_search(f"Best hotels in {city} with ratings prices reviews amenities")

    hotels = []
    for block in raw.split("\n"):
        if ("hotel" in block.lower() or "resort" in block.lower()) and len(block) > 5:
            hotels.append(block.strip())

    output = "🏨 **Top Hotels**\n\n"

    for h in hotels[:5]:
        output += (
            f"🏨 **Hotel Name:** {h}\n"
            f"⭐ **Rating:** Approx 4.0+ ⭐\n"
            f"💰 **Price:** Starts from ₹3000+\n"
            f"🛎️ **Amenities:** Free Wi-Fi, Breakfast, lunch, dinner, Parking\n\n"
        )

    return output


def get_transport_options(start: str, end: str) -> str:
    """Get flight, train, bus options in clean text."""
    raw = web_search(
        f"Transport from {start} to {end} flights trains buses cheapest fastest travel time cost"
    )

    lines = raw.split("\n")
    transport_data = []

    for line in lines:
        if any(x in line.lower() for x in ["flight", "train", "bus"]):
            if len(line.strip()) > 8:
                transport_data.append(line.strip())

    output = f"🛣️ **Transport Options: {start} → {end}**\n\n"

    for t in transport_data[:3]:
        output += (
            f"🚍 **Mode:** {t}\n"
            f"⏳ **Travel Time:** 2–12 hours (approx)\n"
            f"💰 **Estimated Budget:** ₹800 – ₹6000\n\n"
        )

    return output

def get_hospitals(city: str) -> str:
    """Fetch nearby emergency hospitals in clean text."""
    raw = web_search(f"best emergency hospitals in {city} 24/7 emergency care address contact")

    hospitals = []
    for line in raw.split("\n"):
        if any(word in line.lower() for word in ["hospital", "medical", "clinic"]):
            if len(line.strip()) > 6:
                hospitals.append(line.strip())

    if not hospitals:
        return "No clear hospital data found."

    output = f"🏥 **Emergency Hospitals in {city}**\n\n"

    for h in hospitals[:5]:
        output += (
            f"🏥 **Hospital:** {h}\n"
            f"⏱️ **Emergency:** 24/7 Available (approx)\n"
            f"📞 **Contact:** Check locally\n\n"
        )

    return output

def get_local_transport(city: str) -> str:
    """Get local transport guide inside the destination city."""
    raw = web_search(
        f"local transport guide in {city} metro timings, bus routes fares, taxi prices, auto rickshaw cost ,transport passes"
    )

    lines = raw.split("\n")
    transport_info = []

    for line in lines:
        if any(x in line.lower() for x in ["metro", "bus", "taxi", "cab"]):
            if len(line.strip()) > 6:
                transport_info.append(line.strip())

    if not transport_info:
        return "🚉 Local transport details not available."

    output = f"🚉 **Local Transport Guide — {city}**\n\n"

    for t in transport_info[:5]:
        output += (
            f"🚍 **Mode:** {t}\n"
            f"💲 **Approx Fare:** ₹20 – ₹300\n"
            f"⏱️ **Availability:** 5 AM – 11 PM (varies)\n\n"
        )

    return output


# -------------------------
# LLM & Agent
# -------------------------
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=gemini_key,temperature=1.0)

system_prompt = """
You are a Travel assistant.Use tools only when it's required,in case give the response by your pre-trained data.
"""

agent = create_agent(
    model=llm,
    tools=[web_search, get_weather, get_hotels, get_transport_options, get_hospitals, get_local_transport],
    system_prompt=system_prompt
)

# -------------------------
# INPUTS
# -------------------------
st.markdown("""
<style>
.cool-subheader {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
    text-align: center;
    text-shadow: 0 0 8px rgba(255,255,255,0.25);
}
</style>

<div class="cool-subheader">✈️ Let's Begin Your Journey ✈️ </div>
""", unsafe_allow_html=True)

start_city = st.text_input("🏙️ Starting City (From)")
city = st.text_input("📍 Destination City (To)")
duration = st.number_input("⏳ Number of Days you want to spend", min_value=1, max_value=30)
interests = st.selectbox("🎯 Your Interest", ["🌿 Nature", "🧗 Adventure", "🏛️ Culture"])
time_pref = st.selectbox("🕒 Preferred Time Plan", ["🌞 Full Day", "🌅 Morning", "☀️ Afternoon", "🌇 Evening", "🌙 Night"])
generate = st.button("🎒Get My Itinerary")



# -------------------------
# RUN AGENT
# -------------------------
if generate:
    with st.spinner("Crafting your perfect travel experience… 🌟"):

        user_query = f"""
Create a beautiful, emoji-rich, human-friendly travel plan.
DO NOT return JSON.

Trip Details:
• From: {start_city}
• To: {city}
• Duration: {duration} days
• Interest: {interests}
• Time Preference: {time_pref}

Include:

1️⃣ Weather summary  
2️⃣ Transport options from {start_city} to {city}  
3️⃣ A full day-wise itinerary (from Day 1 to Day {duration}) including:
   • Morning plan  
   • Afternoon plan  
   • Evening plan  
   • Best places to visit  
   • Approx timings  
   • Small tips for each day
4️⃣ Top hotels/restaurents
5️⃣ Local transport guide inside {city}
6️⃣ Emergency hospital services in {city}  

Hotel / Restaurant Format:
🏨 Name  
⭐ Rating  
💰 Price  
🛎️ Amenities

Intercity Transport Format:
🚍 Mode  
⏳ Travel Time  
💰 Estimated Budget

Hospital Format:
🏥 Hospital Name  
⏱️ Emergency Availability  
📞 Contact

Local Transport Format:
🚉 Mode  
💲 Approx Fare  
⏱️ Service Hours  

Day-Wise Plan Format:
📅 **Day X:**  
🌅 Morning:  
☀️ Afternoon:  
🌇 Evening:  
📍 Places to Visit:  
💡 Tip:  
"""


        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_query}]}
        )

        result_metrics=result["messages"][-1].content
        st.success("🎉 Your AI Travel Plan is Ready!")
        st.write(result_metrics)



