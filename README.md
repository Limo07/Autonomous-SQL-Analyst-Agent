# 🚗 AutoFlex Motors: Autonomous SQL Analyst Agent

An Agentic AI web application that translates natural language questions into executable SQL queries, runs them against a database, and returns plain-English answers. 

This project bridges the gap between complex databases and non-technical business users, allowing stakeholders to query inventory data effortlessly. It was built using Python, LangChain, Google Gemini, and Gradio.

---

## 📸 Project Showcase

![Gradio Interface]([sql-agent-project\images\ui-screenshot.png](https://github.com/Limo07/Autonomous-SQL-Analyst-Agent/blob/main/images/ui-screenshot.png))

![Agentic Reasoning Trace]([sql-agent-project\images\terminal.png](https://github.com/Limo07/Autonomous-SQL-Analyst-Agent/blob/main/images/ui-screenshot.png))

---

## ✨ Features & Capabilities

* **Natural Language to SQL:** Uses advanced LLM reasoning to interpret user intent and draft accurate SQL syntax.
* **Autonomous Database Introspection:** The agent dynamically inspects the database schema and table relationships to understand the data structure before querying.
* **Self-Correction Loops:** If a generated SQL query contains an error, the agent catches it, reads the error log, and rewrites the query automatically.
* **Interactive UI:** A lightweight, responsive chat interface built with Gradio's `ChatInterface`.

---

## 🛠️ Tech Stack

* **Orchestration:** LangChain (SQLDatabase Toolkit & SQL Agent)
* **LLM:** Google Gemini 3.5 Flash (`langchain-google-genai`)
* **Database:** SQLite3 (Python built-in)
* **Frontend:** Gradio
* **Data Manipulation:** Pandas

---

## 🚀 Replicating the Project

Follow these steps to build and run the complete project from scratch.

### 1. Project Structure
Create a new folder for your project. By the end of this guide, your directory will look like this:

```text
autoflex-sql-agent/
│
├── images/                 # Screenshots for documentation
├── .venv/                  # Virtual Environment (ignored in git)
├── .gitignore              # Files for Git to ignore
├── requirements.txt        # Project dependencies
├── setup_db.py             # Script to generate the mock SQLite database
├── app.py                  # Main Agent and Gradio UI application
└── README.md               # This documentation file
```

### 2. Environment Setup
Initialize a virtual environment to keep dependencies isolated:

**For Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

**For macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Dependencies (`requirements.txt`)
Create a `requirements.txt` file and add the following:

```text
langchain
langchain-community
langchain-google-genai
sqlalchemy
pandas
gradio
```

Install them by running:
```bash
pip install -r requirements.txt
```

### 4. Setting the API Key
Set your Gemini API key in your terminal session so LangChain can authenticate:

**For Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your-gemini-api-key"
```

**For macOS/Linux:**
```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

---

## 📂 The Codebase

### Database Generator (`setup_db.py`)
This script creates a local `cars.db` SQLite database and populates it with mock inventory data for AutoFlex Motors.

```python
import sqlite3
import pandas as pd

# 1. Create mock data
data = {
    "vehicle_id": [101, 102, 103, 104, 105],
    "make": ["Toyota", "Honda", "Nissan", "Toyota", "Subaru"],
    "model": ["Supra", "Civic Type R", "Skyline GT-R", "Land Cruiser", "Impreza WRX"],
    "import_year": [2024, 2024, 2025, 2025, 2026],
    "purchase_price_usd": [45000, 38000, 75000, 60000, 25000],
    "sale_price_usd": [52000, 43000, 85000, 71000, 31000],
    "status": ["Sold", "Sold", "In Transit", "Sold", "Available"]
}

df = pd.DataFrame(data)

# 2. Connect and write to local SQLite database
conn = sqlite3.connect("cars.db")
df.to_sql("inventory", conn, if_exists="replace", index=False)

print("✅ Successfully created cars.db and loaded the 'inventory' table.")
conn.close()
```

Run it to generate the database:
```bash
python setup_db.py
```

### Main Application (`app.py`)
This script initializes the Gemini model, connects to the database, wraps it in a LangChain SQL Agent, and serves it via Gradio.

```python
import gradio as gr
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Initialize the LLM (Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0
)

# 2. Connect Database
db = SQLDatabase.from_uri("sqlite:///cars.db")

# 3. Create Agent
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="tool-calling",
    verbose=True
)

# 4. Define the Chat Wrapper Function
def chat_with_db(message, history):
    try:
        response = agent_executor.invoke({"input": message})
        output = response["output"]
        
        # Clean up output if Gemini returns dictionary metadata
        if isinstance(output, list) and len(output) > 0 and isinstance(output[0], dict):
            return output[0].get("text", str(output))
        return str(output)
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"

# 5. Build and Launch the UI
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
    demo.launch()
```

Run the application:
```bash
python app.py
```
Open `http://127.0.0.1:7860` in your browser.

