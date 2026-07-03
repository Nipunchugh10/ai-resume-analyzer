import React from 'react';

const ICONS = {
  critical: '!',
  important: '!',
  nice: '+',
  positive: '✓',
};

function Suggestions({ suggestions }) {
  const sorted = [...suggestions].sort((a, b) => {
    const order = { critical: 0, important: 1, nice: 2, positive: 3 };
    return (order[a.type] ?? 4) - (order[b.type] ?? 4);
  });

  return (
    <div className="suggestions-list">
      {sorted.map((s, i) => (
        <div className="suggestion-card" key={i}>
          <div className={`suggestion-icon ${s.type}`}>
            {ICONS[s.type] || '?'}
          </div>
          <div className="suggestion-body">
            <div className={`suggestion-type ${s.type}`}>
              {s.type} <span className="suggestion-cat">— {s.category}</span>
            </div>
            <p className="suggestion-text">{s.text}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default Suggestions;
