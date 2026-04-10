import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Bot, User } from 'lucide-react';

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user';
  
  return (
    <div className={`message-row ${isUser ? 'user' : 'ai'}`}>
      {!isUser && (
        <div style={{ marginRight: '10px', marginTop: '5px', color: '#60a5fa' }}>
          <Bot size={24} />
        </div>
      )}
      
      <div className="message-bubble glass">
        {/* Render text content */}
        {message.content && (
           <div style={{ marginBottom: message.data ? '15px' : '0' }}>
               {message.content}
           </div>
        )}
        
        {/* Render Visualizations if data exists */}
        {message.data && message.data.length > 0 && !isUser && (
          <div className="chart-container">
            {message.type === 'table' && (
              <div className="table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      {Object.keys(message.data[0]).map((key) => (
                        <th key={key}>{key}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {message.data.map((row, i) => (
                      <tr key={i}>
                        {Object.values(row).map((val, j) => (
                          <td key={j}>{String(val)}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            
            {message.type === 'barchart' && (
              <div style={{ height: '300px', width: '100%', minWidth: '300px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={message.data}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey={message.xAxis} stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }} />
                    <Legend />
                    <Bar dataKey={message.yAxis} fill="#3b82f6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
            
            {message.type === 'linechart' && (
              <div style={{ height: '300px', width: '100%', minWidth: '300px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={message.data}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey={message.xAxis} stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }} />
                    <Legend />
                    <Line type="monotone" dataKey={message.yAxis} stroke="#c084fc" strokeWidth={3} activeDot={{ r: 8 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        )}
      </div>
      
      {isUser && (
        <div style={{ marginLeft: '10px', marginTop: '5px', color: '#c084fc' }}>
          <User size={24} />
        </div>
      )}
    </div>
  );
}
