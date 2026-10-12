import sys
from pathlib import Path

# Direct script launches need the src directory to resolve mcpexample.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mcpexample.weather_mcp_server.weather import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")
