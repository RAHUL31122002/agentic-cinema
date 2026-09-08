import os
import streamlit as st # pyright: ignore[reportMissingImports]
from google import genai
from google.genai import types

# Page config
st.set_page_config(page_title="CineDirector AI", page_icon="🎬", layout="centered")

st.title("🎬 CineDirector AI Studio")
st.markdown("Your autonomous production workflow agent powered by **Gemini 3.6 Flash**.")

# Setup API Key & Client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key

if not api_key:
    st.warning("Please provide your API key to activate the studio director.")
    st.stop()

client = genai.Client(api_key=api_key)

# Define tools
def query_production_database(sql_query: str) -> str:
    """Queries studio analytics/production tracking database."""
    return f"Database Response: 124 active render nodes reporting. Query executed: {sql_query}"

def trigger_code_executor(task_description: str) -> str:
    """Dispatches code automation task to development sandbox."""
    return f"Sandbox Response: Script compiled successfully for task: {task_description}"

# User Input
user_prompt = st.text_area("Enter Production Command:", "Check our production database for Scene 4 metrics, then spin up a code sandbox task to optimize the render pipeline.")

if st.button("Execute Director Command"):
    if not user_prompt.strip():
        st.error("Please enter a command.")
    else:
        with st.spinner("🎬 Director Agent is analyzing and executing tools..."):
            try:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        tools=[query_production_database, trigger_code_executor],
                        system_instruction="You are an elite AI Studio Director for a blockbuster hackathon production crew.",
                        temperature=0.3,
                    ),
                )
                
                st.subheader("Agent Thought & Output")
                st.write(response.text if response.text else "Executed tool calls directly.")
                
                if response.function_calls:
                    st.subheader("Tool Executions")
                    for call in response.function_calls:
                        st.info(f"**Tool:** {call.name} \n\n **Args:** {call.args}")
                        if call.name == "query_production_database":
                            res = query_production_database(**call.args)
                            st.success(res)
                        elif call.name == "trigger_code_executor":
                            res = trigger_code_executor(**call.args)
                            st.success(res)
                            
            except Exception as e:
                st.error(f"Error: {e}")