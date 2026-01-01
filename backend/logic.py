import yfinance as yf
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END, START
from typing import TypedDict
from tavily import TavilyClient
import os

# Define State
class AgentState(TypedDict):
    ticker: str
    price_data: str
    news_summary: str
    technical_analysis: str
    final_recommendation: str

# --- Helper Functions ---
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        if hist.empty: return None
        current = hist['Close'].iloc[-1]
        start = hist['Close'].iloc[0]
        change = ((current - start) / start) * 100
        return f"Current Price: ${current:.2f}, 1-Month Change: {change:.2f}%"
    except: return None

def get_technical_indicators(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")
    if hist.empty: return "No data."
    
    hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
    delta = hist['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    hist['RSI'] = 100 - (100 / (1 + rs))
    latest = hist.iloc[-1]
    return f"RSI: {latest['RSI']:.2f}, SMA_50: {latest['SMA_50']:.2f}, Price: {latest['Close']:.2f}"

def get_news(ticker, api_key):
    try:
        tavily = TavilyClient(api_key=api_key)
        response = tavily.search(query=f"latest financial news for {ticker}", max_results=3)
        return "\n".join([f"- {r['content']}" for r in response['results']])
    except: return "No news found."

# --- Agent Logic ---
def run_analysis(ticker: str, groq_key: str, tavily_key: str):
    
    def researcher(state):
        return {
            "price_data": get_stock_data(state["ticker"]) or "Error",
            "news_summary": get_news(state["ticker"], tavily_key)
        }

    def analyst(state):
        llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
        prompt = ChatPromptTemplate.from_template("Analyze these technicals for {ticker}: {data}. Short bullish/bearish verdict.")
        chain = prompt | llm | StrOutputParser()
        return {"technical_analysis": chain.invoke({"ticker": state["ticker"], "data": get_technical_indicators(state["ticker"])})}

    def manager(state):
        llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
        prompt = ChatPromptTemplate.from_template("As a Portfolio Manager, give a final Buy/Sell/Hold call for {ticker} based on: \nPrice: {price}\nNews: {news}\nTechs: {tech}. Keep it concise.")
        chain = prompt | llm | StrOutputParser()
        
        # --- THE FIX IS HERE ---
        # We manually map the state variables to the prompt variables
        return {"final_recommendation": chain.invoke({
            "ticker": state["ticker"],
            "price": state["price_data"],
            "news": state["news_summary"],
            "tech": state["technical_analysis"]
        })}

    # Graph Construction
    workflow = StateGraph(AgentState)
    workflow.add_node("researcher", researcher)
    workflow.add_node("analyst", analyst)
    workflow.add_node("manager", manager)
    
    workflow.add_edge(START, "researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "manager")
    workflow.add_edge("manager", END)
    
    app = workflow.compile()
    return app.invoke({"ticker": ticker})