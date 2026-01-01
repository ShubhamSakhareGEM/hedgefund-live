import { useState } from 'react';
import axios from 'axios';
import { LineChart, ShieldAlert, Activity } from 'lucide-react';
import './App.css';

function App() {
  const [ticker, setTicker] = useState('AAPL');
  const [keys, setKeys] = useState({ groq: '', tavily: '' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!keys.groq || !keys.tavily) return alert("Please enter both API Keys");
    setLoading(true);
    setResult(null);
    
    try {
      const response = await axios.post('https://hedgefund-api.onrender.com/analyze', {
        ticker: ticker.toUpperCase(),
        groq_api_key: keys.groq,
        tavily_api_key: keys.tavily
      });
      setResult(response.data);
    } catch (error) {
      alert("Analysis failed. Ensure Backend is running!");
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div className="dashboard-container">
      <header>
        <h1>HedgeFund<span className="brand-accent">GPT</span></h1>
        <p className="subtitle">Autonomous AI Agent Team for Stock Analysis</p>
      </header>
      
      {/* Input Section */}
      <div className="input-section">
        <div className="api-inputs">
          <div className="input-wrapper">
            <input 
              type="password" 
              placeholder="Groq API Key" 
              value={keys.groq}
              onChange={e => setKeys({...keys, groq: e.target.value})} 
            />
          </div>
          <div className="input-wrapper">
            <input 
              type="password" 
              placeholder="Tavily API Key" 
              value={keys.tavily}
              onChange={e => setKeys({...keys, tavily: e.target.value})} 
            />
          </div>
        </div>

        <div className="search-bar">
          <input 
            value={ticker} 
            onChange={e => setTicker(e.target.value)} 
            placeholder="Enter Stock Ticker (e.g. NVDA)" 
          />
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? 'Analyzing...' : 'Launch Agents'}
          </button>
        </div>
      </div>

      {/* Results Dashboard */}
      {result && (
        <div className="results-grid">
          
          {/* Top Row: Market Data & Technicals Side-by-Side */}
          <div className="top-row">
            <div className="card">
              <div className="card-header">
                <Activity size={18} /> Market Data
              </div>
              <div className="card-content">
                <strong>{result.price_data}</strong>
                <hr style={{borderColor: 'var(--border-color)', margin: '15px 0'}}/>
                <div style={{fontSize: '0.9em', color: 'var(--text-secondary)'}}>
                  {result.news_summary}
                </div>
              </div>
            </div>

            <div className="card">
              <div className="card-header">
                <LineChart size={18} /> Technical Analysis
              </div>
              <div className="card-content">
                {result.technical_analysis}
              </div>
            </div>
          </div>

          {/* Bottom Row: Recommendation (Full Width) */}
          <div className="card recommendation-card">
            <div className="card-header">
              <ShieldAlert size={18} /> Portfolio Manager Verdict
            </div>
            <div className="card-content rec-text">
              {result.final_recommendation}
            </div>
          </div>

        </div>
      )}
    </div>
  );
}

export default App;
