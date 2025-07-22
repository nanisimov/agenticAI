#basic_chat3
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
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

with st.sidebar:
    st.subheader("Parameters", divider="gray")
    st.write('chatbot : `langgraph & opanai`.')
    st.write('model : `gpt-3.5-turbo`')
    st.subheader("Neo4j", divider="gray")
    st.write('database: DEMO_2025')

if "openai_model" not in st.session_state:
    print("openai_model not in st.session_state")
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    print("messages not in st.session_state")
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})