import { useState, useEffect, useRef } from "react";

function App() {
  const [messages, setMessages] = useState([
    { role: "ai", text: "AI Banking Triage Engine Ready." }
  ]);

  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [monitor, setMonitor] = useState(null);
  const [stats, setStats] = useState({
    total: 0,
    low: 0,
    high: 0,
    critical: 0,
    out: 0,
    escalations: 0
  });

  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async () => {
    if (!query.trim()) return;

    setMessages(prev => [...prev, { role: "user", text: query }]);
    setQuery("");
    setLoading(true);

    const startTime = performance.now();

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      });

      const data = await res.json();
      const endTime = performance.now();

      const latency = (endTime - startTime).toFixed(2);

      setMonitor({
        ...data,
        latency: latency
      });

      setStats(prev => {
        const updated = { ...prev };
        updated.total += 1;

        if (data.risk_level === "LOW_RISK") updated.low += 1;
        if (data.risk_level === "HIGH_RISK") updated.high += 1;
        if (data.risk_level === "CRITICAL") {
          updated.critical += 1;
          updated.escalations += 1;
        }
        if (data.risk_level === "OUT_OF_DOMAIN") updated.out += 1;

        return updated;
      });

      setMessages(prev => [
        ...prev,
        {
          role: "ai",
          text: `Intent: ${data.intent.replaceAll("_", " ")}`
        }
      ]);

    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="container">

      {/* LEFT PANEL - CHAT */}
      <div className="chat-panel">

        <div className="chat-header">Customer Chat</div>

        <div className="chat-body">
          {messages.map((m, i) => (
            <div key={i} className={`bubble ${m.role}`}>
              {m.text}
            </div>
          ))}
          {loading && <div className="typing">Analyzing...</div>}
          <div ref={endRef}></div>
        </div>

        <div className="chat-input">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter banking query..."
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          />
          <button onClick={handleSubmit}>Send</button>
        </div>

      </div>

      {/* RIGHT PANEL - MONITORING DASHBOARD */}
      <div className="monitor-panel">

        <div className="monitor-header">AI Monitoring Dashboard</div>

        {monitor && (
          <div className="monitor-content">

            <div className="metric">
              <label>Intent</label>
              <span>{monitor.intent}</span>
            </div>

            <div className="metric">
              <label>Confidence</label>
              <span>{(monitor.confidence * 100).toFixed(2)}%</span>
            </div>

            <div className="metric">
              <label>Risk Level</label>
              <span className={`risk ${monitor.risk_level}`}>
                {monitor.risk_level}
              </span>
            </div>

            <div className="metric">
              <label>Handling Stage</label>
              <span>{monitor.handling_stage}</span>
            </div>

            <div className="metric">
              <label>Latency</label>
              <span>{monitor.latency} ms</span>
            </div>

            {monitor.candidates && (
              <div className="candidates">
                <label>Top Candidates</label>
                {monitor.candidates.map((c, i) => (
                  <div key={i}>{i + 1}. {c}</div>
                ))}
              </div>
            )}

          </div>
        )}

        <div className="stats">
          <h4>System Stats</h4>
          <div>Total Queries: {stats.total}</div>
          <div>Low Risk: {stats.low}</div>
          <div>High Risk: {stats.high}</div>
          <div>Critical: {stats.critical}</div>
          <div>Escalations: {stats.escalations}</div>
        </div>

      </div>

    </div>
  );
}

export default App;