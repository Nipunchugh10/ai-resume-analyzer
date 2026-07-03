import React from 'react';

function JobMatches({ matches }) {
  return (
    <div className="jobs-list">
      {matches.map((job, i) => (
        <div className="job-card" key={job.id}>
          <div className="job-card-top">
            <div>
              <div className="job-title">{job.title}</div>
              <div className="job-company">{job.company} — {job.location}</div>
            </div>
            <div className="job-sim">
              {job.similarity}%<br/>
              <small>TF-IDF match</small>
            </div>
          </div>
          <div className="job-desc">{job.description}</div>
          {job.matched_skills.length > 0 && (
            <div className="job-skills-section">
              <div className="job-skills-label">Your matching skills</div>
              <div className="job-skills-tags">
                {job.matched_skills.map((s, j) => (
                  <span className="skill-tag matched" key={j}>{s}</span>
                ))}
              </div>
            </div>
          )}
          {job.missing_skills.length > 0 && (
            <div className="job-skills-section">
              <div className="job-skills-label">Skills to learn</div>
              <div className="job-skills-tags">
                {job.missing_skills.map((s, j) => (
                  <span className="skill-tag missing" key={j}>{s}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default JobMatches;
