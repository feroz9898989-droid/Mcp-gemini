
import os
import uvicorn

from fastapi import FastAPI
from fastmcp import FastMCP


# =====================================================
# 1. INITIALIZE FASTMCP
# =====================================================

mcp = FastMCP("My Render MCP Server")


# =====================================================
# 2. REGISTER MCP TOOLS
# =====================================================

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def greet(name: str) -> str:
    """Generate a greeting for a user."""
    return f"Hello {name}! Your MCP server is working."


@mcp.tool()
def server_status() -> dict:
    """Return information about the MCP server."""
    return {
        "status": "online",
        "service": "FastMCP Render Server",
        "transport": "Streamable HTTP",
        "endpoint": "/mcp/"
    }


# =====================================================
# 3. CREATE MCP HTTP APPLICATION
# =====================================================

mcp_app = mcp.http_app(path="/")


# =====================================================
# 4. CREATE FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="FastMCP Render Server",
    description="FastAPI and FastMCP integrated server",
    version="1.0.0",
    lifespan=mcp_app.lifespan
)


# =====================================================
# 5. HEALTH ENDPOINTS
# =====================================================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "FastMCP Render Server",
        "mcp_endpoint": "/mcp/",
        "health_endpoint": "/health"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "fastmcp-render-app"
    }


@app.get("/info")
async def info():
    return {
        "name": "My Render MCP Server",
        "transport": "Streamable HTTP",
        "mcp_endpoint": "/mcp/",
        "available_tools": [
            "add_numbers",
            "multiply_numbers",
            "greet",
            "server_status"
        ]
    }


# =====================================================
# 6. MOUNT MCP ENDPOINT
# =====================================================

app.mount("/mcp", mcp_app)


# =====================================================
# 7. START SERVER
# =====================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
