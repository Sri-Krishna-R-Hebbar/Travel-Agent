# 🌍 AI Travel Planning Agent

A comprehensive, end-to-end travel planning application that combines LangChain agent orchestration, LLM reasoning (Gemini/LLaMA), and Model Context Protocol (MCP) tools to create intelligent, personalized travel plans.

## ✨ Features

### Core Functionality
- **Intelligent Trip Planning**: Input destination, duration, and travel month to get complete trip plans
- **Real-time Data Integration**: Weather, flights, hotels, and attractions via MCP tools
- **LLM-Powered Insights**: Cultural and historical context generation using Gemini or LLaMA-3
- **Comprehensive Itineraries**: Day-wise plans with attractions, activities, and timing suggestions

### Detailed Outputs
1. **Cultural Context**: AI-generated paragraph on destination's significance
2. **Weather Information**: Current conditions + forecast for trip duration
3. **Travel Date Suggestions**: Multiple date range options within selected month
4. **Flight Options**: Sorted flight choices with pricing and schedules
5. **Hotel Recommendations**: Top-rated hotels with amenities and pricing
6. **Day-wise Itinerary**: Curated attractions with ratings, descriptions, and visit durations

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit UI  │  ← User Interface
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Travel Planning Agent  │  ← LangChain Orchestration
└────────┬────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│         LLM (Gemini/LLaMA)         │  ← AI Reasoning
└────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│          MCP Tools (Real-time Data)         │
├──────────┬──────────┬──────────┬────────────┤
│ Weather  │ Flights  │ Hotels   │  Places    │
└──────────┴──────────┴──────────┴────────────┘
```

## 📁 Project Structure

```
travel-planning-agent/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
│
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration management
│
├── agents/
│   ├── __init__.py
│   └── travel_agent.py        # LangChain travel planning agent
│
├── tools/                     # MCP Tools
│   ├── __init__.py
│   ├── weather_tool.py        # Weather API integration
│   ├── flight_tool.py         # Flight search tool
│   ├── hotel_tool.py          # Hotel search tool
│   └── places_tool.py         # Places/attractions tool
│
└── utils/
    ├── __init__.py
    └── helpers.py             # Utility functions
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google API key for Gemini (or HuggingFace token for LLaMA)

### Step 1: Clone or Download
Download this project to your local machine.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` and add your API keys:
```env
# Required: LLM API Key
GOOGLE_API_KEY=your_google_api_key_here

# Optional: For real weather data
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Optional: Mock data toggle
USE_MOCK_DATA=True
```

### Step 4: Get API Keys

#### Google Gemini API (Required)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in `.env` as `GOOGLE_API_KEY`

#### OpenWeather API (Optional)
1. Visit [OpenWeather](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key and paste it in `.env` as `OPENWEATHER_API_KEY`

**Note:** If you don't provide OpenWeather API key, the system will use mock weather data.

## 🎯 Usage

### Running the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Interface

1. **Enter Trip Details** (in sidebar):
   - Destination city (e.g., "Paris", "Tokyo", "New York")
   - Origin city (where you're traveling from)
   - Number of days (1-30)
   - Travel month (select from dropdown)

2. **Generate Plan**:
   - Click "🚀 Generate Travel Plan"
   - Wait for the AI agent to process (typically 10-30 seconds)

3. **Explore Results**:
   - Review cultural context
   - Check weather forecasts
   - Browse flight options
   - Compare hotels
   - View day-wise itinerary

4. **Export**:
   - Download your plan as Markdown file
   - Share or save for future reference

## 🛠️ Technical Details

### Technologies Used
- **Frontend**: Streamlit 1.31.0
- **Agent Framework**: LangChain 0.1.4
- **LLM**: Google Gemini Pro (via langchain-google-genai)
- **APIs**: OpenWeather API (with mock fallback)
- **Data Processing**: Pandas, NumPy
- **Environment Management**: python-dotenv

### MCP Tool Implementation
Each tool follows the Model Context Protocol pattern:
- **WeatherTool**: Fetches real-time weather via OpenWeather API
- **FlightTool**: Mock flight search (can be replaced with real API)
- **HotelTool**: Mock hotel search (can be replaced with real API)
- **PlacesTool**: Mock attractions database (can be replaced with Google Places API)

### Agent Architecture
The `TravelPlanningAgent` uses LangChain to:
1. Accept user inputs (destination, days, month)
2. Orchestrate multiple tool calls
3. Generate cultural context via LLM
4. Compile structured travel plan
5. Format output for user display

## 🔧 Configuration

### Using Real APIs vs Mock Data
Set `USE_MOCK_DATA=False` in `.env` to use real APIs for all tools (requires API keys).

### Switching LLMs
The project uses Gemini by default. To use LLaMA-3:
1. Uncomment LLaMA dependencies in `requirements.txt`
2. Add `HUGGINGFACE_API_TOKEN` to `.env`
3. Modify `_initialize_llm()` in `agents/travel_agent.py`

### Customizing Temperature
Adjust `LLM_TEMPERATURE` in `config/settings.py` (default: 0.7)
- Lower (0.3-0.5): More focused, deterministic outputs
- Higher (0.8-1.0): More creative, varied outputs

## 📊 Sample Output

A complete travel plan includes:

```markdown
# 🌍 Travel Plan: Paris
Duration: 7 days in June

## 📚 Cultural & Historical Significance
[AI-generated paragraph about Paris]

## 🌤️ Weather Information
Current: 22°C, Partly Cloudy
Forecast: [5-day forecast]

## 📅 Suggested Travel Dates
- Early Month: June 1-7, 2024
- Mid Month: June 11-17, 2024
- Late Month: June 24-30, 2024

## ✈️ Flight Options
[3 best flight options with pricing]

## 🏨 Hotel Options
[5 top hotels with ratings and amenities]

## 🗓️ Day-wise Itinerary
Day 1: Historical Exploration
- Eiffel Tower (4.8/5.0)
- Louvre Museum (4.9/5.0)
[... more attractions]
```

## 🤝 Contributing

This is a lab project, but suggestions are welcome:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Submit pull request

## 📝 Future Enhancements

- [ ] Integration with real flight APIs (Skyscanner, Amadeus)
- [ ] Integration with real hotel APIs (Booking.com, Hotels.com)
- [ ] Google Places API for real attraction data
- [ ] User authentication and saved trips
- [ ] Budget optimization features
- [ ] Multi-city trip planning
- [ ] Interactive map visualization
- [ ] Restaurant and dining recommendations
- [ ] Transportation suggestions within city

## ⚠️ Limitations

- Flight and hotel data is currently mocked (can be replaced with real APIs)
- Some destinations may not have specific landmarks in the mock database
- Weather forecasts limited to 5 days (OpenWeather free tier)
- Cultural context quality depends on LLM availability and performance

## 📄 License

This project is created for educational purposes as part of FGAI Lab coursework.

## 🆘 Troubleshooting

### "No API key found" error
- Ensure `.env` file exists in project root
- Verify `GOOGLE_API_KEY` is set correctly
- Restart the application

### "Error fetching weather"
- If you have `OPENWEATHER_API_KEY` set, verify it's valid
- Otherwise, set `USE_MOCK_DATA=True` to use mock weather data

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version is 3.8+

### Streamlit not opening
- Check if port 8501 is available
- Try running with custom port: `streamlit run app.py --server.port 8502`

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review configuration in `.env` file
3. Verify all dependencies are installed
4. Check API key validity

---

**Built with ❤️ using LangChain, Streamlit, and Gemini AI**
