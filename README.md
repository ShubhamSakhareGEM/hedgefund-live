# HedgeFundGPT

I built this project to experiment with langgraph and see if autonomous agents can actually do decent stock analysis. it uses llama 3 via groq so its super fast, and tavily for searching real time news.

**Live Demo:** [Click here to view the App](https://hedgefund-live.vercel.app/)

<img width="1440" height="859" alt="Screenshot 2026-01-01 at 18 40 31" src="https://github.com/user-attachments/assets/6961c085-987f-4022-bc78-8d8f48431325" />

---

## Features

* **Multi-Agent Orchestration:** Uses LangGraph to manage state and workflow between distinct AI agents.
* **Real-Time Data:** Fetches live market data using `yfinance`.
* **Web Search Capability:** Utilizes the Tavily API to scour the web for the latest financial news.
* **Technical Analysis:** Automatically calculates key indicators like RSI (Relative Strength Index) and SMA (Simple Moving Average) using Python (Pandas) before passing data to the LLM.
* **High-Performance LLM:** Powered by Groq (Llama 3.3 70B) for rapid inference and reasoning.
* **Full-Stack Deployment:** Built with a fast **React/Vite** frontend and a robust **FastAPI** backend (Python).

---

## System Architecture

The application functions as a state machine where information flows through three specialized nodes:

1.  **Researcher Agent**
    * **Role:** Data Aggregation.
    * **Task:** Fetches historical price data (1-month performance) and searches for the latest news articles using Tavily.
    * **Output:** Raw price metrics and a summary of current events.

2.  **Analyst Agent**
    * **Role:** Technical Analysis.
    * **Task:** Calculates technical indicators (RSI, SMA-50, Volume). The LLM then interprets these numbers to determine if the stock is overbought, oversold, or trending.
    * **Output:** A bullish or bearish technical assessment.

3.  **Portfolio Manager Agent**
    * **Role:** Decision Making.
    * **Task:** Synthesizes the fundamental data, news sentiment, and technical analysis into a final report.
    * **Output:** A structured recommendation (Buy/Sell/Hold) with a defined risk level.

---

## Tech Stack

* **Frontend:** React, Vite, CSS Modules
* **Backend:** Python, FastAPI, Uvicorn
* **AI & Orchestration:** LangChain, LangGraph, Groq API (Llama 3.3 70B)
* **Data Sources:** yfinance, Tavily Search API
* **Hosting:** Vercel (Frontend), Render (Backend)

---

## Local Installation

To run this application locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/ShubhamSakhareGEM/hedgefund-gpt.git
cd hedgefund-live
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
The API will start at http://localhost:8000
```

### 3. Frontend Setup
Open a new terminal window:

```bash
cd frontend
npm install
npm run dev
The App will start at http://localhost:5173
```

Note: You will need to update frontend/src/App.jsx to point to http://127.0.0.1:8000 instead of the live URL when running locally.

## API Configuration

This application requires two API keys to function fully. You can enter them in the application sidebar, or configure them in your environment.

* **Groq API Key:** Required for the LLM agents to function.
* **Tavily API Key:** Required for the Researcher agent to fetch news. (If omitted, the app will run with technical and price analysis only).
