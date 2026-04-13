import React from 'react';

function SectionsDetected({ sections }) {
  return (
    <div className="sections-card">
      <h3>Sections Detected</h3>
      {Object.entries(sections).map(([name, found]) => (
        <div className="section-row" key={name}>
          <span className="section-name">{name}</span>
          <span className={`section-check ${found ? 'yes' : 'no'}`}>
            {found ? '✓' : '✗'}
          </span>
        </div>
      ))}
    </div>
  );
}

export default SectionsDetected;
