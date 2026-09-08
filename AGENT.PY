import os
from google import genai
from google.genai import types

# 1. Initialize API Client securely from environment variables
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing! Set it using $env:GEMINI_API_KEY='your_key'")

client = genai.Client(api_key=api_key)

# 2. Define Real Studio Tool Functions
def query_production_database(sql_query: str) -> str:
    """Queries the studio analytics or production tracking database (e.g., ClickHouse).
    
    Args:
        sql_query: The SQL query statement to run.
    """
    # [HACKATHON TIP]: Replace this block with your actual partner client SDK code 
    # e.g., clickhouse_connect or Replit/Grafana API calls.
    print(f"\n[PARTNER TOOL TRIGGERED] Executing query: {sql_query}")
    return "Database Response: 124 active render nodes reporting. Scene 4 status: COMPLETED."

def trigger_code_executor(task_description: str) -> str:
    """Dispatches a script generation or environment task to a development sandbox (e.g., Replit).
    
    Args:
        task_description: Description of the code automation task required.
    """
    print(f"\n[PARTNER TOOL TRIGGERED] Dispatching task to dev sandbox: {task_description}")
    return "Sandbox Response: Script compiled successfully, container deployment active."

# 3. Run Agent Execution Loop
def run_blockbuster_agent(prompt: str):
    print(f"🎬 [STUDIO DIRECTOR AGENT] Analyzing prompt: '{prompt}'")
    
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[query_production_database, trigger_code_executor],
            system_instruction=(
                "You are an elite AI Studio Director for a summer blockbuster hackathon production crew. "
                "You use your integrated technical tools to check project metrics and coordinate automated pipelines."
            ),
            temperature=0.3,
        ),
    )
    
    print("\n--- [AGENT THOUGHT & TEXT OUTPUT] ---")
    print(response.text if response.text else "Agent executed tools directly.")
    
    # Handle function execution routing if triggered by Gemini
    if response.function_calls:
        print("\n--- [EXECUTING TOOL CALLS] ---")
        for call in response.function_calls:
            print(f"Tool Name: {call.name}")
            print(f"Arguments Passed: {call.args}")
            
            if call.name == "query_production_database":
                result = query_production_database(**call.args)
                print(f"Result -> {result}")
            elif call.name == "trigger_code_executor":
                result = trigger_code_executor(**call.args)
                print(f"Result -> {result}")

if __name__ == "__main__":
    print("🎬 [CINE-DIRECTOR AI] Studio terminal active. Type your production commands below (type 'exit' to quit):\n")
    
    while True:
        try:
            user_input = input("Studio Director Prompt > ")
            if user_input.lower() in ["exit", "quit"]:
                print("Shutting down studio session. Action!")
                break
            if not user_input.strip():
                continue
            
            run_blockbuster_agent(user_input)
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\nSession interrupted. Goodbye!")
            break