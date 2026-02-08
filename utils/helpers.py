"""
Helper utility functions for the Travel Planning Agent
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any
import calendar


def get_month_date_range(year: int, month: int) -> tuple:
    """
    Get the first and last day of a given month
    
    Args:
        year: Year (e.g., 2024)
        month: Month (1-12)
    
    Returns:
        Tuple of (first_day, last_day)
    """
    first_day = datetime(year, month, 1)
    last_day_num = calendar.monthrange(year, month)[1]
    last_day = datetime(year, month, last_day_num)
    return first_day, last_day


def format_date(date_obj: datetime, format_str: str = "%Y-%m-%d") -> str:
    """Format datetime object to string"""
    return date_obj.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> datetime:
    """Parse date string to datetime object"""
    return datetime.strptime(date_str, format_str)


def generate_date_suggestions(month: int, year: int, num_days: int) -> List[Dict[str, str]]:
    """
    Generate suggested travel dates for a given month
    
    Args:
        month: Travel month (1-12)
        year: Travel year
        num_days: Number of days for the trip
    
    Returns:
        List of date range suggestions
    """
    first_day, last_day = get_month_date_range(year, month)
    suggestions = []
    
    # Generate 3 suggestions: beginning, middle, and end of month
    # Beginning of month
    start_date = first_day
    end_date = start_date + timedelta(days=num_days - 1)
    if end_date <= last_day:
        suggestions.append({
            "period": "Early Month",
            "start_date": format_date(start_date, "%B %d, %Y"),
            "end_date": format_date(end_date, "%B %d, %Y")
        })
    
    # Middle of month
    start_date = first_day + timedelta(days=10)
    end_date = start_date + timedelta(days=num_days - 1)
    if end_date <= last_day:
        suggestions.append({
            "period": "Mid Month",
            "start_date": format_date(start_date, "%B %d, %Y"),
            "end_date": format_date(end_date, "%B %d, %Y")
        })
    
    # End of month
    end_date = last_day
    start_date = end_date - timedelta(days=num_days - 1)
    if start_date >= first_day:
        suggestions.append({
            "period": "Late Month",
            "start_date": format_date(start_date, "%B %d, %Y"),
            "end_date": format_date(end_date, "%B %d, %Y")
        })
    
    return suggestions


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert temperature from Kelvin to Celsius"""
    return kelvin - 273.15


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert temperature from Kelvin to Fahrenheit"""
    return (kelvin - 273.15) * 9/5 + 32


def format_weather_description(weather_data: Dict[str, Any]) -> str:
    """Format weather data into a readable description"""
    if not weather_data:
        return "Weather data unavailable"
    
    temp_c = weather_data.get('temperature_celsius', 'N/A')
    temp_f = weather_data.get('temperature_fahrenheit', 'N/A')
    description = weather_data.get('description', 'N/A')
    humidity = weather_data.get('humidity', 'N/A')
    
    return (f"{description.capitalize()} with temperatures around "
            f"{temp_c:.1f}°C ({temp_f:.1f}°F), humidity {humidity}%")


def format_price(price: float, currency: str = "USD") -> str:
    """Format price with currency symbol"""
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "INR": "₹"
    }
    symbol = symbols.get(currency, currency)
    return f"{symbol}{price:.2f}"


def get_month_name(month: int) -> str:
    """Get month name from month number"""
    return calendar.month_name[month]


def validate_inputs(destination: str, num_days: int, month: int) -> tuple:
    """
    Validate user inputs
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not destination or len(destination.strip()) < 2:
        return False, "Please enter a valid destination"
    
    if num_days < 1 or num_days > 30:
        return False, "Number of days must be between 1 and 30"
    
    if month < 1 or month > 12:
        return False, "Month must be between 1 and 12"
    
    return True, ""
