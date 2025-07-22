#llm_langchain_app2
import os
import asyncio
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
#from langgraph.graph import START, MessagesState, StateGraph
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from utils import connect_to_server, display_message, process_query
from pprint import pprint


#openai_api_key=os.getenv("OPENAI_API_KEY")
openai_api_key=st.secrets["OPENAI_API_KEY"]
MCP_API_URL = "http://localhost:8050"
LLM_MODEL="gpt-3.5-turbo"
print(openai_api_key)

st.set_page_config(
    page_icon=":cat:",
    page_title="Neo4j MCP Client",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

 # Set logo
#st.logo("images/Neo4j.png", size="large")
#st.logo("neo4j_logo.png", size="large")

st.title("🦜🔗 Neo4j MCP client")
st.write("Based on Streamlit, LangChain/LangGraph and mcp-neo4j-cypher server")
print("🦜🔗 Quickstart App 3 started")


#openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
with st.sidebar:
    st.subheader("Parameters", divider="gray")
    st.write('chatbot : `langgraph & opanai`.')
    st.write('model : `gpt-3.5-turbo`')
    st.subheader("MCP Settings", divider="gray")
    server_url = st.text_input(
        "MCP Server URL",
        value=MCP_API_URL+"/sse",
        help="Enter the URL of your MCP server (SSE endpoint)"
    )
    if st.button("Connect to MCP Server", type="secondary"):
        print("onnect to MCP Server Button pressed")
        asyncio.run(connect_to_server(MCP_API_URL))
    st.subheader("Neo4j Settings", divider="gray")
    if st.button("DEBUG", type="secondary"):
        print("DEBUG Button pressed")
        if "tools" in st.session_state:
            print(st.session_state.tools)
        if "session" in st.session_state:
            print(st.session_state.session)
        if "messages" in st.session_state:
            print("messages=",st.session_state.messages)
        else:
            print("No messages")
    #st.write("Server API URL: ", MCP_API_URL)


def generate_response(input_text):
    print("function generate_response started with:",input_text)
    #model = ChatOpenAI(temperature=0.7, api_key=openai_api_key) # default model="gpt-3.5-turbo" 
    #model=st.session_state.model
    agent=st.session_state.agent
    agent_response =  asyncio.run(agent.ainvoke({"messages": input_text}))
    for m in agent_response["messages"]:
        print("\nmessage=",m.content)
    
    with st.chat_message("assistant"):
        st.markdown(agent_response)
    return (agent_response)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#if "model" not in st.session_state:
 #   st.session_state.model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    response = asyncio.run(process_query(MCP_API_URL,prompt))["messages"]
    for m in response:
        display_message(m)
        print("\nmessage=",m.content)
    for m in response:
        m.pretty_print()
    #with st.chat_message("assistant"):
     #   st.markdown(response)

    #response = generate_response(prompt)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    #print(st.session_state)

