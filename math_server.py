# math_server.py
from mcp.server.fastmcp import FastMCP
print("start",__name__)

mcp = FastMCP("Math",host="127.0.0.1",port=8050)
print("start2")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def say_hello(name: str) -> str:
    """Say hello to user"""
    return f'Hello, {name}! Nice to hear from you!'


if __name__ == "__main__":
    mcp.run(transport="sse")