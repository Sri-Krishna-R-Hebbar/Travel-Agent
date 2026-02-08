"""
Travel Planning Agent using LangChain and REAL MCP Servers
Orchestrates MCP tools to create comprehensive travel plans

⚡ MCP SERVERS USED:
1. Weather: @timlukahorstmann/mcp-weather (AccuWeather)
2. Flights: Kiwi Travel MCP (https://mcp.kiwi.com)
"""
from typing import Dict, Any, List
from datetime import datetime
import calendar

from langchain_google_genai import ChatGoogleGenerativeAI

import config.settings as config
from tools import WeatherTool, FlightTool, PlacesTool
from utils.helpers import (
    generate_date_suggestions,
    get_month_name,
    format_date
)


class TravelPlanningAgent:
    """Main agent for travel planning using LangChain and REAL MCP Servers"""
    
    def __init__(self):
        print("🚀 Initializing Travel Planning Agent with MCP Servers...")
        
        # ⚡ Initialize MCP Tools ⚡
        print("   📡 Connecting to Weather MCP Server...")
        self.weather_tool = WeatherTool()  # Uses @timlukahorstmann/mcp-weather
        
        print("   ✈️  Connecting to Kiwi Travel MCP Server...")
        self.flight_tool = FlightTool()  # Uses https://mcp.kiwi.com
        
        print("   📍 Initializing Places Tool...")
        self.places_tool = PlacesTool()  # Mock data (no MCP server available)
        
        # Initialize LLM
        print("   🤖 Initializing Gemini LLM...")
        self.llm = self._initialize_llm()
        
        print("✅ Agent Ready!")
        
    def _initialize_llm(self):
        """Initialize the language model (Gemini)"""
        try:
            if config.GOOGLE_API_KEY:
                llm = ChatGoogleGenerativeAI(
                    model=config.GEMINI_MODEL,
                    google_api_key=config.GOOGLE_API_KEY,
                    temperature=config.LLM_TEMPERATURE
                )
                return llm
            else:
                raise ValueError("No API key found. Please set GOOGLE_API_KEY in .env file")
        except Exception as e:
            raise Exception(f"Failed to initialize LLM: {e}")
    
    def create_travel_plan(
        self,
        destination: str,
        num_days: int,
        travel_month: int,
        origin: str = "NYC"
    ) -> Dict[str, Any]:
        """
        Create a comprehensive travel plan using MCP Servers
        
        Args:
            destination: Destination city
            num_days: Number of days for the trip
            travel_month: Month of travel (1-12)
            origin: Origin city code (default: NYC)
            
        Returns:
            Complete travel plan dictionary with MCP data
        """
        print(f"\n🌍 Creating travel plan: {origin} → {destination} ({num_days} days)")
        
        from datetime import timedelta
        
        # Calculate dates: Departure = Today + 2 days
        today = datetime.now()
        departure_date_obj = today + timedelta(days=2)
        return_date_obj = departure_date_obj + timedelta(days=num_days)
        
        # Format dates
        departure_date = departure_date_obj.strftime("%Y-%m-%d")
        return_date = return_date_obj.strftime("%Y-%m-%d")
        
        print(f"📅 Travel Dates: {departure_date} to {return_date}")
        
        # 1. Generate cultural/historical context using LLM
        print("📚 Generating cultural context with Gemini...")
        cultural_context = self._generate_cultural_context(destination)
        
        # 2. ⚡ Get weather information using MCP Weather Server ⚡
        print("🌤️  Fetching weather data via MCP Server...")
        weather_info = self._get_weather_info(destination, num_days)
        
        # 3. Generate travel date suggestions based on actual dates
        print("📅 Generating date suggestions...")
        date_suggestions = [
            {
                'period': 'Suggested Dates',
                'start_date': departure_date_obj.strftime("%B %d, %Y"),
                'end_date': return_date_obj.strftime("%B %d, %Y")
            },
            {
                'period': 'Alternative (+1 week)',
                'start_date': (departure_date_obj + timedelta(days=7)).strftime("%B %d, %Y"),
                'end_date': (return_date_obj + timedelta(days=7)).strftime("%B %d, %Y")
            },
            {
                'period': 'Alternative (+2 weeks)',
                'start_date': (departure_date_obj + timedelta(days=14)).strftime("%B %d, %Y"),
                'end_date': (return_date_obj + timedelta(days=14)).strftime("%B %d, %Y")
            }
        ]
        
        # 4. ⚡ Get flight options using Kiwi MCP Server ⚡
        print("✈️  Searching flights via Kiwi MCP Server...")
        flight_options = None
        
        # Get city codes (simple conversion)
        origin_code = self._get_city_code(origin)
        dest_code = self._get_city_code(destination)
        
        flight_options = self.flight_tool.get_best_flights(
            departure_date=departure_date,
            fly_from=origin_code,
            fly_to=dest_code,
            return_date=return_date,
            num_results=3
        )
        
        # 5. Create day-wise itinerary
        print("🗓️  Creating itinerary...")
        itinerary = self.places_tool.create_itinerary_suggestions(
            destination=destination,
            num_days=num_days
        )
        
        # 6. Compile everything into a structured plan
        travel_plan = {
            'destination': destination,
            'origin': origin,
            'duration': f"{num_days} days",
            'travel_month': get_month_name(travel_month),
            'cultural_context': cultural_context,
            'weather': weather_info,
            'suggested_dates': date_suggestions,
            'flights': flight_options,
            'itinerary': itinerary,
            'generated_at': datetime.now().isoformat(),
            'mcp_servers_used': {
                'weather': 'AccuWeather MCP (@timlukahorstmann/mcp-weather)',
                'flights': 'Kiwi Travel MCP (https://mcp.kiwi.com)',
                'places': 'Mock Data (No MCP server available)'
            }
        }
        
        print("✅ Travel plan created successfully!\n")
        return travel_plan
    
    def _get_city_code(self, city: str) -> str:
        """Convert city name to airport/city code"""
        # Common city codes
        city_codes = {
            'new york': 'NYC',
            'nyc': 'NYC',
            'paris': 'PAR',
            'london': 'LON',
            'tokyo': 'TYO',
            'los angeles': 'LAX',
            'chicago': 'CHI',
            'san francisco': 'SFO',
            'miami': 'MIA',
            'boston': 'BOS',
            'seattle': 'SEA',
            'rome': 'ROM',
            'barcelona': 'BCN',
            'amsterdam': 'AMS',
            'dubai': 'DXB',
            'singapore': 'SIN',
            'hong kong': 'HKG',
            'sydney': 'SYD',
            'delhi': 'DEL',
            'mumbai': 'BOM'
        }
        
        city_lower = city.lower().strip()
        return city_codes.get(city_lower, city[:3].upper())
    
    def _generate_cultural_context(self, destination: str) -> str:
        """
        Generate cultural and historical context using Gemini LLM
        
        Args:
            destination: Destination city
            
        Returns:
            Cultural/historical paragraph
        """
        prompt = f"""Write a concise, informative paragraph (4-6 sentences) about the cultural and historical significance of {destination}. 
        Include:
        - Historical importance
        - Cultural highlights
        - What makes it unique
        - Why travelers should visit
        
        Keep it engaging and informative."""
        
        try:
            response = self.llm.invoke(prompt)
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
        except Exception as e:
            print(f"⚠️  LLM Error: {e}")
            return (f"{destination} is a remarkable destination known for its rich cultural heritage "
                   f"and historical significance. The city offers a unique blend of tradition and modernity, "
                   f"making it an ideal destination for travelers seeking authentic experiences. "
                   f"Visitors can explore numerous historical sites, immerse themselves in local culture, "
                   f"and enjoy the vibrant atmosphere that {destination} has to offer.")
    
    def _get_weather_info(self, destination: str, num_days: int) -> Dict[str, Any]:
        """
        Get weather information using MCP Weather Server
        
        Args:
            destination: Destination city
            num_days: Number of days
            
        Returns:
            Dictionary with current weather and forecast
        """
        current_weather = self.weather_tool.get_current_weather(destination)
        forecast = self.weather_tool.get_forecast(destination, min(num_days, 5))
        
        return {
            'current': current_weather,
            'forecast': forecast
        }
    
    def _convert_date_format(self, date_str: str) -> str:
        """Convert date from 'Month Day, Year' to 'YYYY-MM-DD'"""
        try:
            dt = datetime.strptime(date_str, "%B %d, %Y")
            return dt.strftime("%Y-%m-%d")
        except:
            return date_str
    
    def format_travel_plan(self, plan: Dict[str, Any]) -> str:
        """
        Format travel plan as a readable string
        
        Args:
            plan: Travel plan dictionary
            
        Returns:
            Formatted markdown string
        """
        output = []
        
        # Header with MCP indicator
        output.append(f"# 🌍 Travel Plan: {plan['destination']}")
        output.append(f"**Duration:** {plan['duration']} in {plan['travel_month']}")
        output.append(f"**Origin:** {plan['origin']}")
        output.append("")
        output.append("⚡ **Powered by Real MCP Servers:**")
        for service, server in plan.get('mcp_servers_used', {}).items():
            output.append(f"- {service.capitalize()}: {server}")
        output.append("")
        
        # Cultural Context
        output.append("## 📚 Cultural & Historical Significance")
        output.append(plan['cultural_context'])
        output.append("")
        
        # Weather (with MCP indicator)
        output.append("## 🌤️ Weather Information")
        current = plan['weather']['current']
        source = current.get('source', 'Unknown')
        output.append(f"**Current Weather** ({source}):")
        output.append(f"- Temperature: {current['temperature_celsius']:.1f}°C ({current.get('temperature_fahrenheit', 0):.1f}°F)")
        output.append(f"- Conditions: {current['description'].capitalize()}")
        output.append(f"- Humidity: {current['humidity']}%")
        output.append("")
        
        output.append("**Forecast:**")
        for day in plan['weather']['forecast']:
            output.append(f"- {day['date']}: {day['description'].capitalize()}, {day['temperature_celsius']:.1f}°C")
        output.append("")
        
        # Suggested Dates
        output.append("## 📅 Suggested Travel Dates")
        for suggestion in plan['suggested_dates']:
            output.append(f"**{suggestion['period']}:** {suggestion['start_date']} to {suggestion['end_date']}")
        output.append("")
        
        # Flights (with MCP indicator)
        if plan['flights'] and 'outbound_flights' in plan['flights']:
            output.append("## ✈️ Flight Options")
            source = plan['flights'].get('source', 'Unknown')
            output.append(f"**Source:** {source}")
            output.append("")
            output.append("**Outbound Flights:**")
            for i, flight in enumerate(plan['flights']['outbound_flights'][:3], 1):
                output.append(f"\n**Option {i}:** {flight.get('airline', 'Unknown')} - {flight.get('flight_number', 'N/A')}")
                output.append(f"  - Departure: {flight.get('departure_date', 'N/A')} at {flight.get('departure_time', 'N/A')}")
                output.append(f"  - Arrival: {flight.get('arrival_date', 'N/A')} at {flight.get('arrival_time', 'N/A')}")
                output.append(f"  - Duration: {flight.get('duration', 'N/A')} ({flight.get('stops', 0)} stop(s))")
                output.append(f"  - Price: {flight.get('currency', '$')}{flight.get('price', 0):.2f}")
                if 'deep_link' in flight:
                    output.append(f"  - Book: {flight['deep_link']}")
            output.append("")
        
        # Itinerary
        if plan['itinerary']:
            output.append("## 🗓️ Day-wise Itinerary")
            for day_plan in plan['itinerary']:
                output.append(f"\n### Day {day_plan['day']}: {day_plan['theme']}")
                for place in day_plan['places'][:3]:  # Top 3 per day
                    output.append(f"\n**{place['name']}** ({place['type']})")
                    output.append(f"  - {place['description']}")
                    output.append(f"  - Rating: {place['rating']}/5.0")
                    output.append(f"  - Duration: {place['estimated_visit_duration']}")
                    fee_text = "Free" if place['entry_fee']['is_free'] else f"${place['entry_fee']['price']}"
                    output.append(f"  - Entry: {fee_text}")
                output.append("")
        
        return "\n".join(output)
