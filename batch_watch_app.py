import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

# ✅ Modern LangChain imports
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# -------------------------------
# ENV & CONFIG
# -------------------------------
load_dotenv()
st.set_page_config(page_title="BatchWatch Agent", layout="wide")

AUTOSYS_CSV = os.getenv("AUTOSYS_CSV", "autosys.csv")
st.write("AUTOSYS_CSV:", AUTOSYS_CSV)

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_autosys_csv():
    """Load Autosys CSV and compute runtime in minutes."""
    if not os.path.exists(AUTOSYS_CSV):
        st.error(f"CSV file not found: {AUTOSYS_CSV}")
        return pd.DataFrame()
    df = pd.read_csv(AUTOSYS_CSV, parse_dates=["start_time", "end_time"])
    df["runtime"] = (df["end_time"] - df["start_time"]).dt.total_seconds() / 60.0
    return df

# -------------------------------
# ANALYSIS FUNCTIONS
# -------------------------------
def detect_long_running(df, threshold=2.0):
    """Detect jobs whose last run was significantly longer than historical average."""
    long_runners = []
    for job, g in df.groupby("job_name"):
        avg_runtime = g["runtime"].mean()
        last_run = g.sort_values("end_time").iloc[-1]
        if last_run["runtime"] > threshold * avg_runtime:
            long_runners.append({
                "job": job,
                "last_runtime": last_run["runtime"],
                "avg_runtime": avg_runtime,
                "ratio": last_run["runtime"] / avg_runtime
            })
    return pd.DataFrame(long_runners)

def failure_aggregates(df):
    """Aggregate failures by day, week, and month."""
    fails = df[df["status"] == "FAILURE"].copy()
    if fails.empty:
        return {}, {}, {}
    fails["date"] = fails["start_time"].dt.date
    daily = fails.groupby("date").size().to_dict()
    weekly = fails.groupby(fails["start_time"].dt.isocalendar().week).size().to_dict()
    monthly = fails.groupby(fails["start_time"].dt.month).size().to_dict()
    return daily, weekly, monthly

# -------------------------------
# AI AGENT (FAISS + RunnableWithMessageHistory)
# -------------------------------
@st.cache_resource
def init_agent():
    # ✅ Pull models first: `ollama pull mxbai-embed-large` & `ollama pull gemma3:1b` in terminal
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vs = FAISS.from_texts(["BatchWatch memory initialized."], embedding=embeddings)
    retriever = vs.as_retriever(search_kwargs=dict(k=5))

    llm = ChatOllama(model="gemma3:1b")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are BatchWatch, an AI agent monitoring Autosys batch jobs. Focus on job runtimes, failures, and SLA patterns."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    # ✅ Persistent session history
    if "history_store" not in st.session_state:
        st.session_state.history_store = {}

    def get_session_history(session_id: str):
        if session_id not in st.session_state.history_store:
            st.session_state.history_store[session_id] = InMemoryChatMessageHistory()
        return st.session_state.history_store[session_id]

    chain = prompt | llm
    runnable = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    return runnable, retriever

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.title("🤖 BatchWatch Agent (POC - Modern LangChain)")

df = load_autosys_csv()
if df.empty:
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Job Overview", "⚠️ Long Runners", "❌ Failures", "🧠 AI Agent"
])

# --- Tab 1: Job Overview ---
with tab1:
    st.subheader("Autosys Job Data")
    st.dataframe(df.head(20))

# --- Tab 2: Long Running Jobs ---
with tab2:
    st.subheader("Long Running Jobs vs Historical Averages")
    long_df = detect_long_running(df)
    if long_df.empty:
        st.success("No abnormal long-running jobs detected ✅")
    else:
        st.warning("Detected long-running jobs:")
        st.dataframe(long_df)

# --- Tab 3: Failure Aggregates ---
with tab3:
    st.subheader("Failure Aggregates")
    daily, weekly, monthly = failure_aggregates(df)
    st.write("**Daily Failures:**", daily)
    st.write("**Weekly Failures:**", weekly)
    st.write("**Monthly Failures:**", monthly)

# --- Tab 4: AI Agent ---
with tab4:
    st.subheader("AI Remediation & Focus Visualization")
    st.caption("💬 The agent uses FAISS memory + Ollama embeddings to focus on relevant job segments.")

    runnable, retriever = init_agent()
    user_input = st.text_area("Ask BatchWatch something about jobs, failures, or SLAs:")

    if st.button("Ask AI"):
        if user_input.strip():
            with st.spinner("🤖 BatchWatch is analyzing job patterns..."):
                # Show what retriever focuses on
                docs = retriever.get_relevant_documents(user_input)
                if docs:
                    st.info("📌 **Data segments AI is focusing on:**")
                    for d in docs:
                        st.write("-", d.page_content)

                # Run AI and display output
                response = runnable.invoke(
                    {"input": user_input},
                    config={"configurable": {"session_id": "streamlit-session"}}
                )
                st.write("🤖 **BatchWatch:**", response)
