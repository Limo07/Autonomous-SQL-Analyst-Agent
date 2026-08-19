from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import gradio as gr

# 1. Initialize the NVIDIA LLM
# Llama 3.1 70B is a powerful open-source model perfect for writing code/SQL

# $env:GOOGLE_API_KEY="123" 
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0.0  # Low temperature for consistent SQL generation
)

# 2. Connect to the local db created
db = SQLDatabase.from_uri("sqlite:///cars.db")

# 3. Create the SQL Agent   
# This gives the LLM a set of tools to read the schema, write queries, and check for errors.

agent_executer = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="tool-calling",
    verbose=True # Verbose mode lets us see the agent's internal "thought process" in the terminal
)

# 4. Create a terminal chat loop
# Gradio's ChatInterface ALWAYS expects a function that takes (message, history)

def chat_with_db(message, history):
    try:
        # Pass the user's question into the agent
        response = agent_executer.invoke({"input": message})

        # Clean up the output list if Gemini returns dictionary metadata
        output = response['output']
        if isinstance(output, list) and len(output) > 0 and isinstance(output[0], dict):
            return output[0].get("text", str(output))
        return str(output)    
           

    except Exception as e:
        print(f"\n❌Error: {str(e)}\n")

# 5. Build and launch the UI
demo = gr.ChatInterface(
    fn=chat_with_db,
    title="🚗 AutoFlex Motors - SQL Analyst",
    description="Ask questions about your vehicle inventory in plain English. The AI will autonomously write and execute SQL to find the answer.",
    examples=[
        "How many cars are currently in transit?",
        "What is the total potential profit from all currently sold vehicles?",
        "Which make has the highest average purchase price?"
    ]
)

if __name__ == "__main__":
    # Launch the server!
    demo.launch()

    
