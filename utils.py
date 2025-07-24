#test
import asyncio
import streamlit as st
from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

async def main():
       await connect_to_server("http://localhost:8050")

AVAILABLE_MODELS = {
    "gpt-3.5-turbo":"gpt-3.5-turbo",
    "openai:gpt-4.1":"openai:gpt-4.1"
}

async def connect_to_server(server_url):
        async with sse_client(server_url+"/sse") as (read, write):
            async with ClientSession(read, write) as session:
                print("session=",vars(session))                
                await session.initialize()
                print("connect_to_server: Connected to MCP server via SSE and initialized session.")
                if "session" not in st.session_state:
                      st.session_state.session=session
 
                tools = await load_mcp_tools(session)
                with st.sidebar:
                       st.write("Connection to MCP server established")
                       st.subheader("🔧Tools", divider="gray")
                       st.write([tool.name for tool in tools])                       
                print("Connected to MCP server established!")
                st.session_state.connected=True
                # Create and run the agent
                agent = create_react_agent("openai:gpt-4.1", tools)
                #res=  await agent.ainvoke({"messages": user_query})
                #print("res=",res)
                #st.session_state.agent=agent
                #st.session_state.tools=tools
                return(True)
            
async def process_query(server_url,user_query):
        async with sse_client(server_url+"/sse") as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("process_query: Connected to MCP server via SSE and initialized session.")
                tools = await load_mcp_tools(session)
                with st.sidebar:
                       st.subheader("🔧Tools", divider="gray")
                       st.write([tool.name for tool in tools])                       
                #agent = create_react_agent("openai:gpt-4.1", tools)
                agent = create_react_agent("openai:gpt-3.5-turbo", tools)                
                res=  await agent.ainvoke({"messages": user_query})
                return(res)
       

def display_message(message):
        # display user message
        if isinstance(message,HumanMessage) and type(message.content) == str:
               st.chat_message("user").markdown(message.content)
        elif isinstance(message,AIMessage) and message.content != "":
               st.chat_message("assistant").markdown(message.content)
        elif isinstance(message,AIMessage) and message.content == "":
               tc_parms="{ " 
               if "name" in message.tool_calls[0]:
                     tc_parms += "tool name: "+message.tool_calls[0]["name"]
               if "query" in message.tool_calls[0]["args"]:
                     tc_parms += ", query:"+message.tool_calls[0]["args"]["query"]
               st.chat_message("assistant").markdown("Tool call= "+tc_parms+" }")   #m.tool_calls[0]["args"]["query"]
        elif isinstance(message,ToolMessage):
               st.chat_message("tool",avatar="🔧").markdown("Tool name: "+message.name)
            