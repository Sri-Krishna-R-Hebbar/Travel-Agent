"""
Test script to verify MCP servers are working properly
Run this before using the main app to diagnose issues
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment
load_dotenv()

print("=" * 70)
print("MCP SERVERS TEST")
print("=" * 70)
print()

# Test 1: Check API Keys
print("1️⃣  Checking API Keys...")
print("-" * 70)

google_key = os.getenv("GOOGLE_API_KEY")
accuweather_key = os.getenv("ACCUWEATHER_API_KEY")

if google_key and google_key != "your_google_api_key_here":
    print(f"✅ GOOGLE_API_KEY: Configured ({google_key[:10]}...)")
else:
    print(f"❌ GOOGLE_API_KEY: Missing or invalid")

if accuweather_key and accuweather_key != "your_accuweather_api_key_here":
    print(f"✅ ACCUWEATHER_API_KEY: Configured ({accuweather_key[:10]}...)")
else:
    print(f"❌ ACCUWEATHER_API_KEY: Missing or invalid")

print()

# Test 2: Check Node.js and MCP packages
print("2️⃣  Checking Node.js and MCP Weather Server...")
print("-" * 70)

import subprocess

try:
    node_version = subprocess.run(['node', '--version'], capture_output=True, text=True)
    if node_version.returncode == 0:
        print(f"✅ Node.js installed: {node_version.stdout.strip()}")
    else:
        print(f"❌ Node.js not found")
except Exception as e:
    print(f"❌ Node.js check failed: {e}")

try:
    npm_version = subprocess.run(['npm', '--version'], capture_output=True, text=True)
    if npm_version.returncode == 0:
        print(f"✅ npm installed: {npm_version.stdout.strip()}")
    else:
        print(f"❌ npm not found")
except Exception as e:
    print(f"❌ npm check failed: {e}")

try:
    # Check if MCP weather package is installed
    npm_list = subprocess.run(['npm', 'list', '-g', '@timlukahorstmann/mcp-weather'], 
                              capture_output=True, text=True)
    if '@timlukahorstmann/mcp-weather' in npm_list.stdout:
        print(f"✅ Weather MCP Server installed")
    else:
        print(f"❌ Weather MCP Server not installed")
        print(f"   Run: npm install -g @timlukahorstmann/mcp-weather")
except Exception as e:
    print(f"⚠️  Could not check MCP weather installation: {e}")

print()

# Test 3: Test Weather MCP Server Connection
print("3️⃣  Testing Weather MCP Server Connection...")
print("-" * 70)

async def test_weather_mcp():
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        
        # Configure MCP server
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@timlukahorstmann/mcp-weather"],
            env={"ACCUWEATHER_API_KEY": accuweather_key} if accuweather_key else {}
        )
        
        print("📡 Connecting to Weather MCP Server...")
        
        # Add timeout
        async def connect():
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize
                    await session.initialize()
                    print("✅ Connection established!")
                    
                    # List tools
                    tools = await session.list_tools()
                    print(f"✅ Available tools: {[t.name for t in tools.tools]}")
                    
                    # Try to call weather tool (note: underscore not hyphen!)
                    print("🔍 Testing weather-get_hourly for Paris...")
                    result = await session.call_tool(
                        "weather-get_hourly",  # Underscore not hyphen!
                        arguments={"location": "Paris", "units": "metric"}
                    )
                    
                    if result and hasattr(result, 'content'):
                        print(f"✅ Weather MCP responded!")
                        if result.content:
                            response_text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                            print(f"   Response preview: {response_text[:200]}...")
                            return True
                    else:
                        print(f"⚠️  No content in response")
                        return False
        
        result = await asyncio.wait_for(connect(), timeout=30.0)
        return result
        
    except asyncio.TimeoutError:
        print(f"❌ Weather MCP Server timeout (30s)")
        return False
    except Exception as e:
        print(f"❌ Weather MCP Error: {type(e).__name__}: {str(e)[:200]}")
        import traceback
        traceback.print_exc()
        return False

# Run weather test
try:
    weather_result = asyncio.run(test_weather_mcp())
except Exception as e:
    print(f"❌ Failed to run weather test: {e}")
    weather_result = False

print()

# Test 4: Test Kiwi MCP Server Connection
print("4️⃣  Testing Kiwi Travel MCP Server Connection...")
print("-" * 70)

async def test_kiwi_mcp():
    try:
        from mcp import ClientSession
        from mcp.client.sse import sse_client
        
        mcp_url = "https://mcp.kiwi.com"
        
        print(f"📡 Connecting to Kiwi MCP at {mcp_url}...")
        
        async def connect():
            async with sse_client(mcp_url) as (read, write):
                print("✅ SSE connection established")
                
                async with ClientSession(read, write) as session:
                    # Initialize
                    init_result = await session.initialize()
                    print(f"✅ Session initialized (protocol: {init_result.protocolVersion})")
                    
                    # List tools
                    tools = await session.list_tools()
                    tool_names = [t.name for t in tools.tools]
                    print(f"✅ Available tools: {tool_names}")
                    
                    # Try to search flights
                    print("🔍 Testing flight search NYC → PAR...")
                    
                    from datetime import datetime, timedelta
                    # Kiwi requires dd/mm/yyyy format!
                    departure = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
                    
                    tool_name = "search-flight"
                    
                    result = await session.call_tool(
                        tool_name,
                        arguments={
                            "departureDate": departure,
                            "flyFrom": "NYC",
                            "flyTo": "PAR"
                        }
                    )
                    
                    if result and hasattr(result, 'content'):
                        print(f"✅ Kiwi MCP responded!")
                        if result.content:
                            response_text = str(result.content[0])[:200] if result.content else "No content"
                            print(f"   Response preview: {response_text}...")
                            return True
                    else:
                        print(f"⚠️  No content in response")
                        return False
        
        result = await asyncio.wait_for(connect(), timeout=30.0)
        return result
        
    except asyncio.TimeoutError:
        print(f"❌ Kiwi MCP Server timeout (30s)")
        return False
    except Exception as e:
        print(f"❌ Kiwi MCP Error: {type(e).__name__}: {str(e)[:200]}")
        import traceback
        traceback.print_exc()
        return False

# Run Kiwi test
try:
    kiwi_result = asyncio.run(test_kiwi_mcp())
except Exception as e:
    print(f"❌ Failed to run Kiwi test: {e}")
    kiwi_result = False

print()

# Summary
print("=" * 70)
print("📊 TEST SUMMARY")
print("=" * 70)

results = {
    "API Keys": "✅" if (google_key and accuweather_key) else "⚠️",
    "Node.js & npm": "✅",
    "Weather MCP Server": "✅" if weather_result else "❌",
    "Kiwi MCP Server": "✅" if kiwi_result else "❌"
}

for test, status in results.items():
    print(f"{status} {test}")

print()

if weather_result and kiwi_result:
    print("🎉 ALL TESTS PASSED! MCP servers are working!")
    print("   Run: streamlit run app.py")
elif not accuweather_key or accuweather_key == "your_accuweather_api_key_here":
    print("⚠️  ACCUWEATHER_API_KEY not configured")
    print("   Get your free key from: https://developer.accuweather.com/")
    print("   Add to .env file: ACCUWEATHER_API_KEY=your_key_here")
else:
    print("⚠️  Some tests failed. Check errors above.")
    print()
    print("Common fixes:")
    print("1. Install Weather MCP: npm install -g @timlukahorstmann/mcp-weather")
    print("2. Check AccuWeather API key in .env")
    print("3. Check internet connection for Kiwi MCP")

print("=" * 70)
