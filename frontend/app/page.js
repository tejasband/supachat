"use client";

import { useState, useRef, useEffect } from 'react';
import ChatMessage from '../components/ChatMessage';
import { Send, Loader2 } from 'lucide-react';

export default function Home() {
  const [messages, setMessages] = useState([
    {
      role: 'system',
      type: 'text',
      content: 'Welcome to SupaChat Analytic! Ask me anything about your blog data, e.g., "Show top trending topics in last 30 days" or "Compare article engagement by topic".',
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
      });
      
      const data = await res.json();
      
      setMessages((prev) => [
        ...prev,
        {
          role: 'ai',
          type: data.type || 'text',
          content: data.content,
          data: data.data,
          xAxis: data.xAxis,
          yAxis: data.yAxis
        }
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'ai',
          type: 'text',
          content: 'Sorry, I could not connect to the backend. Please make sure the FastAPI server is running on localhost:8000.',
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="header">
        <h1 className="gradient-text">SupaChat</h1>
        <p>AI-Powered Blog Analytics</p>
      </div>

      <div className="chat-container glass">
        <div className="messages">
          {messages.map((msg, idx) => (
            <ChatMessage key={idx} message={msg} />
          ))}
          {loading && (
            <div className="message-row ai">
              <div className="message-bubble glass" style={{ opacity: 0.7 }}>
                <Loader2 className="animate-spin" size={24} color="#60a5fa" />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <form className="input-form" onSubmit={handleSend}>
            <input 
              type="text" 
              placeholder="Ask about your metrics..." 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
            />
            <button type="submit" disabled={loading || !input.trim()}>
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
