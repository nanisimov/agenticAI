# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
import streamlit as st
import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
#from utils.logger import logger

def input_func(prompt: str):
     return input("Enter neo-related question: ")

async def run_chat_session(agent,input_func,termination_keywords):
     print("run_chat_session started")
     while True:
          user_input=input_func("Enter your question")
          if user_input.lower() in termination_keywords:
                    break
          response = await agent.ainvoke({"messages": user_input})
          #print("response=",response)
          for m in response["messages"]:
                        print(m.content)


async def main():
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            
            # Get tools
            tools = await load_mcp_tools(session)
            for tool in tools:
                print("tool=",tool.description)

            # Create and run the agent
            agent = create_react_agent("openai:gpt-4.1", tools)
            #agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})

            await run_chat_session(agent,input_func,["q","quit"])



            while 2>3:
                user_input=input("Enter a prompt (q=quit)   ")
                if user_input=="q":
                    break
                agent_response = await agent.ainvoke({"messages": user_input})
                print("agent_response=\n",agent_response["messages"])

                for m in agent_response["messages"]:
                        print(m.content)

    



if __name__ == "__main__":
    asyncio.run(main())