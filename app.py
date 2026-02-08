"""
Travel Planning Agent - Streamlit Application
Main frontend interface for the travel planning system
"""
import streamlit as st
import sys
from datetime import datetime
import calendar

# Add project root to path
sys.path.insert(0, '.')

# Install MCP Weather Server on first run (for Streamlit Cloud)
try:
    from install_mcp import install_mcp_weather_server
    install_mcp_weather_server()
except Exception as e:
    print(f"⚠️  MCP installation check skipped: {e}")

from agents.travel_agent import TravelPlanningAgent
from utils.helpers import validate_inputs, get_month_name
import config.settings as config


# Page configuration
st.set_page_config(
    page_title="Travel Planning Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1E88E5;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #FFF3E0;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'travel_plan' not in st.session_state:
        st.session_state.travel_plan = None
    if 'agent' not in st.session_state:
        st.session_state.agent = None


def create_sidebar():
    """Create sidebar with input form"""
    with st.sidebar:
        st.markdown("### 🎯 Trip Details")
        
        # Destination input
        destination = st.text_input(
            "Destination City",
            placeholder="e.g., Paris, Tokyo, New York",
            help="Enter the city you want to visit"
        )
        
        # Origin city
        origin = st.text_input(
            "Origin City",
            value="New York",
            placeholder="e.g., London, Mumbai",
            help="Enter your departure city"
        )
        
        # Number of days
        num_days = st.slider(
            "Number of Days",
            min_value=1,
            max_value=30,
            value=7,
            help="How many days will you be traveling?"
        )
        
        # Travel month
        current_month = datetime.now().month
        month_names = [calendar.month_name[i] for i in range(1, 13)]
        
        selected_month_name = st.selectbox(
            "Travel Month",
            options=month_names,
            index=current_month - 1,
            help="Select the month you plan to travel"
        )
        travel_month = month_names.index(selected_month_name) + 1
        
        st.markdown("---")
        
        # Generate button
        generate_button = st.button(
            "🚀 Generate Travel Plan",
            type="primary",
            use_container_width=True
        )
        
        # About section
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        ⚡ **Powered by REAL MCP Servers:**
        - 🌤️ **Weather MCP**: AccuWeather API
        - ✈️ **Kiwi Travel MCP**: Real flight search
        - 🤖 **Gemini LLM**: Cultural insights
        - 🗓️ **LangChain**: Agent orchestration
        """)
        
        # MCP Status
        st.markdown("### ⚡ MCP Server Status")
        if config.ACCUWEATHER_API_KEY and config.ACCUWEATHER_API_KEY != "your_accuweather_api_key_here":
            st.success("🌤️ Weather MCP: Connected")
        else:
            st.warning("🌤️ Weather MCP: Mock Data")
        st.success("✈️ Kiwi MCP: Ready (No API key needed)")
        
        return destination, origin, num_days, travel_month, generate_button


def display_cultural_context(plan):
    """Display cultural and historical context"""
    st.markdown('<div class="section-header">📚 Cultural & Historical Significance</div>', 
                unsafe_allow_html=True)
    # Better styled box with dark text on light background
    st.markdown(f'''
    <div style="background-color: #F0F8FF; padding: 1.5rem; border-radius: 0.5rem; 
                border-left: 4px solid #1E88E5; margin-bottom: 1rem;">
        <p style="color: #1a1a1a; font-size: 1.05rem; line-height: 1.6; margin: 0;">
            {plan["cultural_context"]}
        </p>
    </div>
    ''', unsafe_allow_html=True)


def display_weather_info(plan):
    """Display weather information"""
    st.markdown('<div class="section-header">🌤️ Weather Information</div>', 
                unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Current Weather")
        current = plan['weather']['current']
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric(
                "Temperature", 
                f"{current['temperature_celsius']:.1f}°C",
                f"{current['temperature_fahrenheit']:.1f}°F"
            )
        with metric_col2:
            st.metric("Humidity", f"{current['humidity']}%")
        with metric_col3:
            st.metric("Wind", f"{current['wind_speed']} m/s")
        
        st.info(f"**Conditions:** {current['description'].capitalize()}")
    
    with col2:
        st.markdown("#### Forecast")
        for day in plan['weather']['forecast']:
            st.write(f"**{day['date']}**: {day['description'].capitalize()}, "
                    f"{day['temperature_celsius']:.1f}°C")


def display_suggested_dates(plan):
    """Display suggested travel dates"""
    st.markdown('<div class="section-header">📅 Suggested Travel Dates</div>', 
                unsafe_allow_html=True)
    
    cols = st.columns(len(plan['suggested_dates']))
    for col, suggestion in zip(cols, plan['suggested_dates']):
        with col:
            st.markdown(f"**{suggestion['period']}**")
            st.write(f"**From:** {suggestion['start_date']}")
            st.write(f"**To:** {suggestion['end_date']}")


def display_flight_options(plan):
    """Display flight options"""
    if not plan['flights'] or 'outbound_flights' not in plan['flights']:
        return
    
    st.markdown('<div class="section-header">✈️ Flight Options</div>', 
                unsafe_allow_html=True)
    
    # Show source
    source = plan['flights'].get('source', 'Unknown')
    if 'Kiwi' in source and 'Mock' not in source:
        st.success(f"🌐 **Source:** {source}")
    else:
        st.warning(f"📝 **Source:** {source}")
    
    st.markdown("#### Outbound Flights")
    
    for i, flight in enumerate(plan['flights']['outbound_flights'][:3], 1):
        # Handle both 'price' (Kiwi) and 'total_price' (mock) keys
        price = flight.get('price', flight.get('total_price', 0))
        airline = flight.get('airline', 'Unknown')
        
        with st.expander(f"Option {i}: {airline} - ${price:.2f}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Flight Details**")
                st.write(f"🛫 {flight.get('flight_number', 'N/A')}")
                if 'aircraft' in flight:
                    st.write(f"✈️ {flight['aircraft']}")
                if 'class' in flight:
                    st.write(f"💺 {flight['class']}")
            
            with col2:
                st.write("**Schedule**")
                st.write(f"📅 Departure: {flight.get('departure_date', 'N/A')}")
                st.write(f"🕐 {flight.get('departure_time', 'N/A')}")
                st.write(f"⏱️ Duration: {flight.get('duration', 'N/A')}")
                stops_text = "Non-stop" if flight.get('stops', 0) == 0 else f"{flight.get('stops', 0)} stop(s)"
                st.write(f"🔄 {stops_text}")
            
            with col3:
                st.write("**Pricing**")
                st.write(f"💵 Price: ${price:.2f}")
                st.write(f"💱 Currency: {flight.get('currency', 'USD')}")
                
                # Show booking link if available
                if 'deep_link' in flight:
                    st.link_button("🔗 Book Now", flight['deep_link'])
                
                # Show available seats if present
                if 'available_seats' in flight:
                    st.write(f"🎫 Available: {flight['available_seats']} seats")


def display_itinerary(plan):
    """Display day-wise itinerary"""
    if not plan['itinerary']:
        return
    
    st.markdown('<div class="section-header">🗓️ Day-wise Itinerary</div>', 
                unsafe_allow_html=True)
    
    for day_plan in plan['itinerary']:
        st.markdown(f"### Day {day_plan['day']}: {day_plan['theme']}")
        
        for place in day_plan['places']:
            with st.expander(f"{place['name']} - {place['rating']}/5.0 ⭐"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**{place['type']}** | {place['category'].capitalize()}")
                    st.write(place['description'])
                    st.write(f"**Activities:** {', '.join(place['activities'])}")
                
                with col2:
                    st.write(f"**Duration:** {place['estimated_visit_duration']}")
                    st.write(f"**Best Time:** {place['best_time_to_visit']}")
                    
                    if place['entry_fee']['is_free']:
                        st.success("✅ Free Entry")
                    else:
                        st.info(f"💵 ${place['entry_fee']['price']} entry fee")
        
        st.markdown("---")


def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🌍 AI Travel Planning Agent</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your intelligent companion for planning the perfect trip</div>', 
                unsafe_allow_html=True)
    
    # Sidebar with inputs
    destination, origin, num_days, travel_month, generate_button = create_sidebar()
    
    # Main content area
    if generate_button:
        # Validate inputs
        is_valid, error_message = validate_inputs(destination, num_days, travel_month)
        
        if not is_valid:
            st.error(f"❌ {error_message}")
            return
        
        # Show loading state
        with st.spinner("🤖 AI Agent is planning your perfect trip..."):
            try:
                # Initialize agent if not already done
                if st.session_state.agent is None:
                    st.session_state.agent = TravelPlanningAgent()
                
                # Generate travel plan
                travel_plan = st.session_state.agent.create_travel_plan(
                    destination=destination.strip(),
                    num_days=num_days,
                    travel_month=travel_month,
                    origin=origin.strip()
                )
                
                st.session_state.travel_plan = travel_plan
                
            except Exception as e:
                st.error(f"❌ Error generating travel plan: {str(e)}")
                st.error("Please check your API keys in the .env file and try again.")
                return
        
        st.success("✅ Travel plan generated successfully!")
    
    # Display travel plan if available
    if st.session_state.travel_plan:
        plan = st.session_state.travel_plan
        
        # Overview
        st.markdown(f"## 🎯 Trip Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Destination", plan['destination'])
        with col2:
            st.metric("Duration", plan['duration'])
        with col3:
            st.metric("Travel Month", plan['travel_month'])
        
        st.markdown("---")
        
        # Display all sections
        display_cultural_context(plan)
        display_weather_info(plan)
        display_suggested_dates(plan)
        display_flight_options(plan)
        display_itinerary(plan)
        
        # Download option
        st.markdown("---")
        st.markdown("### 💾 Export Travel Plan")
        
        # Format as markdown for download
        formatted_plan = st.session_state.agent.format_travel_plan(plan)
        
        st.download_button(
            label="📥 Download as Markdown",
            data=formatted_plan,
            file_name=f"travel_plan_{plan['destination']}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
    else:
        # Welcome message
        st.markdown("""
        ## 👋 Welcome!
        
        Get started by filling in your trip details in the sidebar:
        
        1. **Enter your destination** - Where do you want to go?
        2. **Enter your origin city** - Where will you be traveling from?
        3. **Select trip duration** - How many days?
        4. **Choose travel month** - When do you want to travel?
        5. **Click "Generate Travel Plan"** - Let the AI do the rest!
        
        ### ✨ What You'll Get (via MCP Servers):
        
        - 📚 Cultural and historical insights (Gemini LLM)
        - 🌤️ Current weather and forecast (Weather MCP Server)
        - 📅 Suggested travel dates
        - ✈️ Flight options (Kiwi Travel MCP Server)
        - 🗓️ Complete day-wise itinerary with attractions
        
        ### 🔧 Setup Instructions:
        
        1. Copy `.env.example` to `.env`
        2. Add your API keys:
           - `GOOGLE_API_KEY` for Gemini (required) - Get from: https://makersuite.google.com/app/apikey
           - `ACCUWEATHER_API_KEY` for Weather MCP (optional) - Get from: https://developer.accuweather.com/
        3. Install dependencies: `pip install -r requirements.txt`
        4. Install MCP packages: `pip install mcp httpx-sse`
        5. Run the app: `streamlit run app.py`
        
        ---
        
        ⚡ **MCP Servers Used:**
        - **Weather**: @timlukahorstmann/mcp-weather (AccuWeather)
        - **Flights**: Kiwi Travel MCP (https://mcp.kiwi.com) - No API key needed!
        
        **Note:** If you haven't configured the AccuWeather API key, weather will use mock data.
        """)


if __name__ == "__main__":
    main()
