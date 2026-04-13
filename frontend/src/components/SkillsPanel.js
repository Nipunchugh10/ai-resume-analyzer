import React from 'react';

function SkillsPanel({ skills }) {
  const { skills_by_category, total_skills, entities } = skills;

  return (
    <div className="skills-panel">
      {Object.entries(skills_by_category).map(([category, skillList]) => (
        <div className="skill-category-card" key={category}>
          <div className="skill-cat-header">
            <h3>{category}</h3>
            <span className="skill-count">{skillList.length}</span>
          </div>
          <div className="skills-list">
            {skillList.map((skill, i) => (
              <span className="skill-chip" key={i}>{skill}</span>
            ))}
          </div>
        </div>
      ))}

      {entities && (entities.organizations?.length > 0 || entities.dates?.length > 0) && (
        <div className="entities-card">
          <h3>Entities Detected (spaCy NER)</h3>
          {entities.organizations?.length > 0 && (
            <div className="entity-group">
              <div className="entity-label">Organizations</div>
              <div className="entity-items">
                {entities.organizations.map((e, i) => (
                  <span className="entity-tag" key={i}>{e}</span>
                ))}
              </div>
            </div>
          )}
          {entities.dates?.length > 0 && (
            <div className="entity-group">
              <div className="entity-label">Dates</div>
              <div className="entity-items">
                {entities.dates.map((e, i) => (
                  <span className="entity-tag" key={i}>{e}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default SkillsPanel;
