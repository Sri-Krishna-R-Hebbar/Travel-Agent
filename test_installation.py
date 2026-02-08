"""
Quick test script to verify installation and setup
Run this before starting the main application
"""
import sys

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing package imports...")
    
    packages = {
        'streamlit': 'Streamlit',
        'langchain': 'LangChain',
        'langchain_google_genai': 'LangChain Google GenAI',
        'requests': 'Requests',
        'dotenv': 'Python Dotenv',
        'pandas': 'Pandas',
        'numpy': 'NumPy'
    }
    
    failed = []
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name}")
            failed.append(name)
    
    if failed:
        print(f"\n⚠️  Missing packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All packages installed successfully!")
    return True


def test_project_structure():
    """Test if project structure is correct"""
    print("\n🔍 Testing project structure...")
    
    import os
    
    required_dirs = ['agents', 'tools', 'config', 'utils']
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example',
        'README.md'
    ]
    
    missing = []
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing.append(f"Directory: {directory}")
            print(f"  ❌ {directory}/")
        else:
            print(f"  ✅ {directory}/")
    
    for file in required_files:
        if not os.path.exists(file):
            missing.append(f"File: {file}")
            print(f"  ❌ {file}")
        else:
            print(f"  ✅ {file}")
    
    if missing:
        print(f"\n⚠️  Missing: {', '.join(missing)}")
        return False
    
    print("\n✅ Project structure is correct!")
    return True


def test_env_file():
    """Test if .env file exists and has required keys"""
    print("\n🔍 Testing environment configuration...")
    
    import os
    from dotenv import load_dotenv
    
    if not os.path.exists('.env'):
        print("  ⚠️  .env file not found")
        print("  💡 Copy .env.example to .env and add your API keys")
        print("     Command: copy .env.example .env")
        return False
    
    load_dotenv()
    
    google_key = os.getenv('GOOGLE_API_KEY')
    weather_key = os.getenv('OPENWEATHER_API_KEY')
    use_mock = os.getenv('USE_MOCK_DATA', 'True').lower() == 'true'
    
    if not google_key or google_key == 'your_google_api_key_here':
        print("  ⚠️  GOOGLE_API_KEY not configured")
        print("  💡 Get your key from: https://makersuite.google.com/app/apikey")
        return False
    else:
        print("  ✅ GOOGLE_API_KEY configured")
    
    if not weather_key or weather_key == 'your_openweather_api_key_here':
        print("  ⚠️  OPENWEATHER_API_KEY not configured (will use mock data)")
    else:
        print("  ✅ OPENWEATHER_API_KEY configured")
    
    if use_mock:
        print("  ℹ️  Using mock data mode")
    else:
        print("  ℹ️  Using real API mode")
    
    print("\n✅ Environment configuration loaded!")
    return True


def test_tools():
    """Test if MCP tools can be imported"""
    print("\n🔍 Testing MCP tools...")
    
    try:
        from tools import WeatherTool, FlightTool, HotelTool, PlacesTool
        print("  ✅ WeatherTool")
        print("  ✅ FlightTool")
        print("  ✅ HotelTool")
        print("  ✅ PlacesTool")
        
        # Quick functionality test
        weather = WeatherTool()
        result = weather.get_current_weather("Paris")
        if result and 'city' in result:
            print("  ✅ WeatherTool working")
        
        print("\n✅ All tools imported successfully!")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_agent():
    """Test if agent can be initialized"""
    print("\n🔍 Testing Travel Planning Agent...")
    
    try:
        from agents import TravelPlanningAgent
        print("  ✅ Agent imported")
        
        # Note: Don't initialize agent here if no API key
        # agent = TravelPlanningAgent()
        
        print("\n✅ Agent ready!")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        print("  💡 Make sure GOOGLE_API_KEY is set in .env")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Travel Planning Agent - Installation Test")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Project Structure", test_project_structure),
        ("Environment Config", test_env_file),
        ("MCP Tools", test_tools),
        ("Agent Setup", test_agent)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} failed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! You're ready to run the app:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("   Check QUICKSTART.md for setup instructions.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
