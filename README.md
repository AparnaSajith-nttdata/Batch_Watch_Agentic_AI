# 🤖 BatchWatch Agent (Proof of Concept)

BatchWatch is an **agentic AI job analysis bot** that autonomously monitors batch job logs and audit tables. Using predictive analytics, it identifies potential long-running or failing jobs before they breach SLAs. This proof-of-concept integrates **Streamlit**, **LangChain**, **FAISS memory**, and **Ollama LLM** for AI-assisted remediation recommendations.

---

## 🧩 Features

- Load Autosys CSV job logs (`AUTOSYS_CSV` environment variable)
- Detect **long-running jobs** compared to historical averages
- Aggregate **job failures** (daily, weekly, monthly)
- AI-powered **remediation insights** using Ollama LLM
- FAISS vector store memory for contextual recall
- Streamlit interface for **interactive monitoring**

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/batch-watch-agent.git
cd batch-watch-agent

## 2. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt

## 3. Pull Ollama Models

Ensure the Ollama models are available locally:

```bash
ollama pull mxbai-embed-large
ollama pull gemma3:1b
## 4. Set CSV Path
Create a .env file in the root of the project:

env
Copy code
AUTOSYS_CSV=/full/path/to/autosys.csv
Or export the environment variable:

```bash
Copy code
export AUTOSYS_CSV=/full/path/to/autosys.csv

##5. Run the Streamlit App
```bash
Copy code
streamlit run batch_watch_app.py

##📊 Streamlit UI
The app is organized into four tabs:

Job Overview – View raw Autosys job data

Long Runners – Detect jobs with unusually long runtimes

Failures – Aggregate failed jobs by day, week, and month

AI Agent – Ask BatchWatch questions about job performance, SLA, and failures. The AI shows the data segments it focuses on and gives recommendations.

##🧠 AI & Memory
Uses Ollama LLM (gemma3:1b) for natural language analysis

FAISS vector store stores key job info for contextual recall

Retrieval highlights which parts of the data the AI is focusing on

Uses RunnableWithMessageHistory to track conversation history in st.session_state

##🔧 Configuration
AUTOSYS_CSV – Path to Autosys CSV file with at least these columns:

job_name

start_time

end_time

status

LLM & embeddings can be swapped in code:

```python
Copy code
llm = ChatOllama(model="gemma3:1b")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

##📝 Notes
This is a POC, not production-ready

FAISS memory is in-memory; persistence after app restart is not implemented yet

Ensure the CSV has correct datetime formats for start_time and end_time

##🚀 Future Enhancements
Persist FAISS memory between sessions

Add alerting via Slack/email/webhook for SLA breaches

Add visual charts for job runtimes and failure trends

Integrate multiple schedulers (not just Autosys)

Structured LLM reasoning trace for transparency

##🛠 Tech Stack
Python

Streamlit for UI

Pandas / NumPy for data processing

LangChain for AI orchestration

Ollama LLM for natural language analysis

FAISS for vector memory
