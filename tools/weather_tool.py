"""
Weather Tool using REAL MCP Server
Uses @timlukahorstmann/mcp-weather MCP server with AccuWeather API
"""
import asyncio
from typing import Dict, Any, List
from datetime import datetime
import config.settings as config

# MCP imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class WeatherTool:
    """Tool for fetching weather information using MCP Weather Server"""
    
    def __init__(self):
        self.api_key = config.ACCUWEATHER_API_KEY
        self.use_mock = config.USE_MOCK_DATA or not self.api_key
        
        # Validate API key
        if self.api_key and self.api_key != "your_accuweather_api_key_here":
            print(f"✅ Weather MCP: Using AccuWeather API key")
            self.use_mock = False
        else:
            print(f"⚠️  Weather MCP: No valid API key, using mock data")
            self.use_mock = True
        
        # ⚡ MCP SERVER CONFIGURATION ⚡
        # This is where we configure the REAL MCP server connection
        self.mcp_server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@timlukahorstmann/mcp-weather"],
            env={
                "ACCUWEATHER_API_KEY": self.api_key if self.api_key and self.api_key != "your_accuweather_api_key_here" else ""
            }
        )
    
    async def _call_mcp_weather(self, location: str, units: str = "metric") -> Dict[str, Any]:
        """
        ⚡ THIS IS WHERE THE MCP SERVER IS ACTUALLY USED! ⚡
        
        Connects to the MCP weather server and calls the weather-get-hourly tool
        
        Args:
            location: City name or location
            units: "metric" or "imperial"
            
        Returns:
            Weather data from MCP server
        """
        try:
            print(f"🌐 Connecting to Weather MCP Server for {location}...")
            
            # Add timeout
            import asyncio
            
            async def get_weather():
                # Connect to MCP server
                async with stdio_client(self.mcp_server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        # Initialize the MCP session
                        await session.initialize()
                        
                        # List tools to verify connection
                        tools = await session.list_tools()
                        print(f"   ✅ Connected! Available tools: {[t.name for t in tools.tools]}")
                        
                        # ⚡ CALLING THE MCP TOOL: weather-get_hourly ⚡
                        # Note: Tool name uses underscore, not hyphen!
                        print(f"   🔍 Calling weather-get_hourly for {location}...")
                        result = await session.call_tool(
                            "weather-get_hourly",  # Underscore not hyphen!
                            arguments={
                                "location": location,
                                "units": units
                            }
                        )
                        
                        print(f"   ✅ Got response from Weather MCP!")
                        
                        # Process the result
                        if result and hasattr(result, 'content'):
                            # Extract weather data from MCP response
                            weather_data = self._parse_mcp_response(result.content, location, units)
                            return weather_data
                        
                        return self._get_mock_current_weather(location)
            
            # Run with timeout
            result = await asyncio.wait_for(get_weather(), timeout=30.0)
            return result
                    
        except asyncio.TimeoutError:
            print(f"⚠️  Weather MCP timeout for {location}")
            print(f"   Falling back to mock data...")
            return self._get_mock_current_weather(location)
        except Exception as e:
            print(f"❌ MCP Weather Server Error: {type(e).__name__}: {str(e)[:200]}")
            print(f"   Falling back to mock data...")
            return self._get_mock_current_weather(location)
    
    def _parse_mcp_response(self, content: Any, location: str, units: str) -> Dict[str, Any]:
        """Parse the MCP server response into our format"""
        try:
            # MCP returns a list of content items
            if isinstance(content, list) and len(content) > 0:
                # Get the text content
                weather_text = content[0].text if hasattr(content[0], 'text') else str(content[0])
                
                # Parse the weather information
                # The MCP server returns formatted text with weather details
                return {
                    'city': location,
                    'raw_data': weather_text,
                    'temperature_celsius': self._extract_temperature(weather_text, units),
                    'temperature_fahrenheit': self._extract_temperature(weather_text, 'imperial') if units == 'metric' else None,
                    'description': self._extract_description(weather_text),
                    'humidity': self._extract_humidity(weather_text),
                    'wind_speed': self._extract_wind_speed(weather_text),
                    'source': 'MCP Weather Server (AccuWeather)',
                    'units': units
                }
            
            return self._get_mock_current_weather(location)
            
        except Exception as e:
            print(f"Error parsing MCP response: {e}")
            return self._get_mock_current_weather(location)
    
    def _extract_temperature(self, text: str, units: str) -> float:
        """Extract temperature from weather text"""
        try:
            # Look for temperature patterns in the text
            import re
            if units == 'metric':
                match = re.search(r'(\d+)°C', text)
            else:
                match = re.search(r'(\d+)°F', text)
            
            if match:
                return float(match.group(1))
            
            # Default fallback
            return 20.0 if units == 'metric' else 68.0
        except:
            return 20.0 if units == 'metric' else 68.0
    
    def _extract_description(self, text: str) -> str:
        """Extract weather description from text"""
        # Common weather conditions
        conditions = ['sunny', 'cloudy', 'rainy', 'clear', 'partly cloudy', 'overcast', 'stormy']
        
        text_lower = text.lower()
        for condition in conditions:
            if condition in text_lower:
                return condition
        
        return "moderate weather"
    
    def _extract_humidity(self, text: str) -> int:
        """Extract humidity from weather text"""
        try:
            import re
            match = re.search(r'(\d+)%', text)
            if match:
                return int(match.group(1))
            return 65
        except:
            return 65
    
    def _extract_wind_speed(self, text: str) -> float:
        """Extract wind speed from weather text"""
        try:
            import re
            match = re.search(r'(\d+\.?\d*)\s*(mph|km/h|m/s)', text.lower())
            if match:
                return float(match.group(1))
            return 10.0
        except:
            return 10.0
    
    def get_current_weather(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Get current weather for a city using MCP Server
        
        Args:
            city: Name of the city
            units: "metric" or "imperial"
            
        Returns:
            Dictionary containing weather information
        """
        if self.use_mock:
            print(f"⚠️  Using mock data (AccuWeather API key not configured)")
            return self._get_mock_current_weather(city)
        
        # Run the async MCP call
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._call_mcp_weather(city, units))
            loop.close()
            return result
        except Exception as e:
            print(f"Error calling MCP weather: {e}")
            return self._get_mock_current_weather(city)
    
    def get_forecast(self, city: str, num_days: int = 5) -> List[Dict[str, Any]]:
        """
        Get weather forecast - uses current weather data
        Since MCP server provides hourly data, we simulate daily forecast
        """
        current = self.get_current_weather(city)
        
        if 'source' in current and 'MCP' in current['source']:
            # We got real MCP data, create forecast from it
            forecasts = []
            for i in range(num_days):
                date = datetime.now()
                date = date.replace(day=date.day + i) if date.day + i <= 28 else date.replace(month=date.month + 1, day=1)
                
                forecasts.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'temperature_celsius': current['temperature_celsius'] + (i % 3) - 1,
                    'temperature_fahrenheit': (current['temperature_celsius'] + (i % 3) - 1) * 9/5 + 32,
                    'description': current['description'],
                    'humidity': current['humidity'],
                    'wind_speed': current['wind_speed']
                })
            
            return forecasts
        else:
            # Fall back to mock forecast
            return self._get_mock_forecast(city, num_days)
    
    def _get_mock_current_weather(self, city: str) -> Dict[str, Any]:
        """Generate mock current weather data"""
        return {
            'city': city,
            'temperature_celsius': 24.5,
            'temperature_fahrenheit': 76.1,
            'description': 'partly cloudy',
            'humidity': 65,
            'wind_speed': 12.5,
            'feels_like_celsius': 23.8,
            'source': 'Mock Data (AccuWeather API key not configured)'
        }
    
    def _get_mock_forecast(self, city: str, num_days: int) -> List[Dict[str, Any]]:
        """Generate mock forecast data"""
        from datetime import timedelta
        forecasts = []
        base_temp = 24.0
        
        for i in range(num_days):
            date = datetime.now() + timedelta(days=i)
            temp_variation = (i % 3) * 2
            
            forecasts.append({
                'date': date.strftime('%Y-%m-%d'),
                'temperature_celsius': base_temp + temp_variation,
                'temperature_fahrenheit': (base_temp + temp_variation) * 9/5 + 32,
                'description': ['sunny', 'partly cloudy', 'cloudy'][i % 3],
                'humidity': 60 + (i % 4) * 5,
                'wind_speed': 10 + (i % 3) * 2
            })
        
        return forecasts
    
    def get_weather_summary(self, city: str, num_days: int) -> str:
        """
        Get a formatted weather summary
        
        Args:
            city: Name of the city
            num_days: Number of days to include in forecast
            
        Returns:
            Formatted string with weather information
        """
        current = self.get_current_weather(city)
        forecast = self.get_forecast(city, num_days)
        
        # Add source indicator
        source_indicator = "🌐 MCP Server" if 'MCP' in current.get('source', '') else "📝 Mock Data"
        
        summary = f"**Current Weather in {city}:** {source_indicator}\n"
        summary += f"- Temperature: {current['temperature_celsius']:.1f}°C ({current['temperature_fahrenheit']:.1f}°F)\n"
        summary += f"- Conditions: {current['description'].capitalize()}\n"
        summary += f"- Humidity: {current['humidity']}%\n"
        summary += f"- Wind Speed: {current['wind_speed']} m/s\n\n"
        
        summary += f"**{num_days}-Day Forecast:**\n"
        for day in forecast:
            summary += f"- {day['date']}: {day['description'].capitalize()}, "
            summary += f"{day['temperature_celsius']:.1f}°C ({day['temperature_fahrenheit']:.1f}°F)\n"
        
        return summary
