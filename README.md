# Batch_Watch_Agentic_AI

Project Utilizes poetry dependency manager which is pretty easy to setup.

## Instructions on Poetry Setup
To setup poetry if wanted to better manage dependencies & run the following commands in a bash terminal in codespaces

```bash
pip install pipx
pipx ensurepath
pipx install poetry
poetry install
```

There it should be easy to manage and add the needed dependencies for it.
Keep in mind, don't make major changes to the poetry.lock because it is sensitive.

**Please do not mess with the file pyproject.toml.**

**It is a difficult file to work with and can be cumbersome to work with all together**

## Instructions on Running

To run any python file or streamlit interface, please use the following commands in the codespaces bash terminal:

```bash
poetry run python main.py
poetry run streamlit main.py
```

For any other poetry related issues, refer back to the following documentation.

https://python-poetry.org/

## Environment variables for local development

This POC supports a small set of environment variables for optional integrations (LLM, data path). To get started:

1. Copy `.env.example` to `.env` and fill in values you need (do not commit `.env`).

```bash
cp .env.example .env
# edit .env and add your GEMINI_API_KEY and GEMINI_API_URL if you want LLM analysis
```

The Streamlit app reads the following variables:
- GEMINI_API_KEY: API key for the Gemini/LLM provider used by the POC.
- GEMINI_API_URL: Base URL for the Gemini API endpoint (POC uses a simple JSON POST).
- AUTOSYS_CSV: Path to the generated autosys CSV file (defaults to `autosys_logs.csv`).

Security note: Never commit real API keys to source control. Use secrets management for production.
# Batch_Watch_Agentic_AI

Project Utilizes poetry dependency manager which is pretty easy to setup. 

# Instructions on Poetry Setup 
To setup poetry if wanted to better manage dependencies & run the following commands in a bash terminal in codespaces

**pip install pipx**

**pipx ensurepath**

**pipx install poetry**

**poetry install**

There it should be easy to manage and add the needed dependencies for it. 
Keep in mind, don't make major changes to the poetry.lock because it is sensitive. 

**Please do not mess with the file pyproject.toml.**

**It is a difficult file to work with and can be cumbersome to work with all together**

# Instructions on Running 

To run any python file or streamlit interface, please use the following commands in the codespaces bash terminal:

**poetry run python main.py**

**poetry run streamlit main.py**


For any other poetry related issues, refer back to the following documentation.

https://python-poetry.org/