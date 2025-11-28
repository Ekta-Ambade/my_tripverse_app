### 🌍 TRIPVERSE – AI Travel Planner

Your intelligent travel companion powered by Streamlit, Gemini AI, and Tavily Search.

### 🚀 About the Project

TRIPVERSE is an AI-powered travel planning application that generates personalized travel itineraries, including:

### ✈️ Intercity transport options

🌤 Weather updates

🏨 Best hotels and restaurants

🚌 Local transport guide

🏥 Emergency hospitals nearby

📅 Full day-wise itinerary based on interests

The app uses Gemini Generative AI for natural-language trip generation and Tavily Search API for real-time web information.

### 📦 Features
🔍 Smart Web Search

Powered by Tavily API to fetch hotel details, local transport data, hospitals, and more.

🤖 Intelligent Itinerary Generation

Uses Gemini 2.0 Flash via langchain_google_genai to generate human-friendly, emoji-rich travel plans.

🌦 Live Weather Updates

Fetches weather data using OpenWeatherMap API.

📍 Complete Travel Assistance

Intercity transport

Local travel inside the city

Top hotels & restaurants

Day-wise sightseeing plan

Safety info (nearby hospitals)

### 🛠 Tech Stack
UI Framework- Streamlit|
AI Model-Gemini 2.0 Flash (Google)|
Tools Framework-LangChain|
Search API-Tavily Search API|
Weather API-OpenWeatherMap API|
Backend	Python-3.13.7

### 🔐 API Keys Required

You must generate and add the following API keys in the sidebar:

1️⃣ Gemini API Key

Get it from:
https://aistudio.google.com

2️⃣ Tavily API Key

Get it from:
https://app.tavily.com

3️⃣ OpenWeatherMap API
Already added in the script.

### 🧩 How It Works
➤ 1. User Inputs

Starting city

Destination

Duration

Interests

Preferred time of the day

➤ 2. Tools Run Automatically

web_search() → For hotels, hospitals, transport

get_weather() → Live weather

get_transport_options() → Flights, trains, buses

get_local_transport() → Metro, taxis, buses

get_hospitals() → Emergency centers

➤ 3. AI Agent Generates Output

LangChain’s create_agent() takes all tools and uses Gemini to craft a detailed travel plan.

### 📜 Run the App Locally
1. Install Dependencies

Create a requirements.txt with:
streamlit |
requests  |
tavily-python |
langchain-google-genai |
pillow |
langchain |
langchain-core |
langchain-community |
google-genai |

Then run:
pip install -r requirements.txt

2. Run the App
streamlit run app.py
A browser tab will open automatically.

### 🧠 Agent Prompting Logic

Your system prompt ensures:

Tools are used only when required

AI generates natural, human-friendly itineraries

No JSON output

Rich emojis & formatting included

### 🌈 Output Example
The generated response includes:
✔ Weather summary
✔ Transport options
✔ Full day-wise itinerary
✔ Top hotels
✔ Local transport inside the city
✔ Emergency hospital info
Each day includes:
🌅 Morning plan
☀️ Afternoon plan
🌇 Evening plan
📍 Places to visit
💡 Tips

### 📌 Notes

Make sure API keys are correct in sidebar
Tavily free plan limits search calls
Gemini API may require region availability



### 🏁 Conclusion
This project is a fully functional AI-powered travel planner that combines:
Real-time web data
AI reasoning
Beautiful UI
Multi-tool integration

You can deploy this app on Streamlit Cloud.






