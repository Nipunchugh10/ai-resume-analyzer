import React from 'react';

function ScoreCard({ score }) {
  const { total, grade, verdict } = score;
  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (total / 100) * circumference;

  const ringColor =
    total >= 80 ? '#22c55e' :
    total >= 60 ? '#3b82f6' :
    total >= 40 ? '#eab308' :
    total >= 20 ? '#f97316' : '#ef4444';

  return (
    <div className="score-card">
      <div className="score-ring">
        <svg width="120" height="120" viewBox="0 0 120 120">
          <circle className="track" cx="60" cy="60" r={radius} />
          <circle
            className="fill-ring"
            cx="60" cy="60" r={radius}
            stroke={ringColor}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
          />
        </svg>
        <div className="score-text">{total}</div>
      </div>
      <div className={`score-grade grade-${grade}`}>Grade {grade}</div>
      <p className="score-verdict">{verdict}</p>
    </div>
  );
}

export default ScoreCard;
