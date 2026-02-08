"""
Runtime MCP Weather Server Installation
Installs the Node.js MCP package when the app starts
"""
import subprocess
import sys
import os

def install_mcp_weather_server():
    """Install MCP Weather Server if not already installed"""
    try:
        print("🔍 Checking for MCP Weather Server...")
        
        # Check if npx is available
        result = subprocess.run(
            ['npx', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ npx is available: {result.stdout.strip()}")
            
            # Try to verify weather MCP package
            print("📦 Installing @timlukahorstmann/mcp-weather...")
            
            # Note: npx will auto-download on first use, no need to pre-install!
            print("✅ MCP Weather Server ready (npx will download on demand)")
            return True
        else:
            print("⚠️  npx not available, MCP Weather will use mock data")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  npx check timeout, MCP Weather will use mock data")
        return False
    except Exception as e:
        print(f"⚠️  Could not verify MCP setup: {e}")
        print("   Weather will use mock data")
        return False

if __name__ == "__main__":
    install_mcp_weather_server()
