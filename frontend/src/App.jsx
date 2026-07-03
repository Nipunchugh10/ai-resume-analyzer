import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ScoreCard from './components/ScoreCard';
import SkillsPanel from './components/SkillsPanel';
import JobMatches from './components/JobMatches';
import Suggestions from './components/Suggestions';
import SectionsDetected from './components/SectionsDetected';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');
  const fileInputRef = useRef(null);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const handleFile = (f) => {
    if (f && f.type === 'application/pdf') {
      setFile(f);
      setError(null);
    } else {
      setError('Please upload a PDF file.');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('resume', file);

    try {
      const res = await axios.post(`${API_URL}/upload_resume`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
    } catch (err) {
      const msg = err.response?.data?.error || 'Upload failed. Is the backend running?';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setError(null);
    setActiveTab('overview');
  };

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'skills', label: 'Skills' },
    { id: 'jobs', label: 'Job Matches' },
    { id: 'suggestions', label: 'Suggestions' },
  ];

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo" onClick={handleReset} style={{ cursor: 'pointer' }} title="Go to Home/Upload">
            <div className="logo-icon">R</div>
            <span>AI Resume Analyzer</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {result && (
              <button className="reset-btn" onClick={handleReset}>
                Upload New Resume
              </button>
            )}
            <button
              className="theme-toggle-btn"
              onClick={toggleTheme}
              title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
              aria-label="Toggle Theme"
            >
              {theme === 'dark' ? (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="5"></circle>
                  <line x1="12" y1="1" x2="12" y2="3"></line>
                  <line x1="12" y1="21" x2="12" y2="23"></line>
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                  <line x1="1" y1="12" x2="3" y2="12"></line>
                  <line x1="21" y1="12" x2="23" y2="12"></line>
                  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
              )}
            </button>
          </div>
        </div>
      </header>

      {!result ? (
        <main className="upload-page">
          <div className="upload-hero">
            <h1>AI-Powered Resume Analysis</h1>
            <p>Upload your resume and get instant AI feedback — skills extraction, scoring, job matching, and improvement suggestions.</p>
          </div>

          <div
            className={`drop-zone ${dragActive ? 'drag-active' : ''} ${file ? 'has-file' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
            onDragLeave={() => setDragActive(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={(e) => handleFile(e.target.files[0])}
              hidden
            />
            {file ? (
              <div className="file-selected">
                <div className="file-icon">PDF</div>
                <div>
                  <p className="file-name">{file.name}</p>
                  <p className="file-size">{(file.size / 1024).toFixed(1)} KB</p>
                </div>
              </div>
            ) : (
              <div className="drop-content">
                <div className="upload-icon">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
                  </svg>
                </div>
                <p className="drop-text">Drop your resume PDF here</p>
                <p className="drop-sub">or click to browse</p>
              </div>
            )}
          </div>

          {error && <div className="error-msg">{error}</div>}

          <button
            className="analyze-btn"
            onClick={handleUpload}
            disabled={!file || loading}
          >
            {loading ? (
              <span className="spinner-wrap">
                <span className="spinner"></span>
                Analyzing...
              </span>
            ) : (
              'Analyze Resume'
            )}
          </button>

          <div className="features-grid">
            {[
              { icon: '🎯', title: 'Skill Extraction', desc: 'AI identifies your technical and soft skills automatically' },
              { icon: '📊', title: 'Resume Scoring', desc: 'Get a detailed score breakdown across 5 categories' },
              { icon: '🤝', title: 'Job Matching', desc: 'TF-IDF powered matching against real job descriptions' },
              { icon: '💡', title: 'Smart Suggestions', desc: 'Personalized tips to improve your resume' },
            ].map((f, i) => (
              <div className="feature-card" key={i}>
                <span className="feature-icon">{f.icon}</span>
                <h3>{f.title}</h3>
                <p>{f.desc}</p>
              </div>
            ))}
          </div>
        </main>
      ) : (
        <div className="dashboard">
          {/* Sidebar summary */}
          <aside className="sidebar">
            <div className="sidebar-card">
              <div className="file-badge">PDF</div>
              <h3>{result.filename}</h3>
              <p className="meta">{result.word_count} words</p>
            </div>

            <ScoreCard score={result.score} />
            <SectionsDetected sections={result.sections_detected} />
          </aside>

          {/* Main content */}
          <main className="main-content">
            <nav className="tab-nav">
              {tabs.map((t) => (
                <button
                  key={t.id}
                  className={`tab-btn ${activeTab === t.id ? 'active' : ''}`}
                  onClick={() => setActiveTab(t.id)}
                >
                  {t.label}
                </button>
              ))}
            </nav>

            <div className="tab-content">
              {activeTab === 'overview' && (
                <div className="overview-grid">
                  <div className="ov-section">
                    <h2>Score Breakdown</h2>
                    <div className="breakdown-bars">
                      {Object.entries(result.score.breakdown).map(([key, val]) => (
                        <div className="bar-row" key={key}>
                          <div className="bar-label">
                            <span className="bar-name">{key.replace(/_/g, ' ')}</span>
                            <span className="bar-val">{val.score}/{val.max}</span>
                          </div>
                          <div className="bar-track">
                            <div
                              className="bar-fill"
                              style={{ width: `${(val.score / val.max) * 100}%` }}
                            />
                          </div>
                          <p className="bar-detail">{val.detail}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="ov-section">
                    <h2>Quick Stats</h2>
                    <div className="stats-grid">
                      <div className="stat-card">
                        <div className="stat-num">{result.skills.total_skills}</div>
                        <div className="stat-label">Skills Found</div>
                      </div>
                      <div className="stat-card">
                        <div className="stat-num">{Object.keys(result.skills.skills_by_category).length}</div>
                        <div className="stat-label">Skill Categories</div>
                      </div>
                      <div className="stat-card">
                        <div className="stat-num">{result.job_matches.length}</div>
                        <div className="stat-label">Job Matches</div>
                      </div>
                      <div className="stat-card">
                        <div className="stat-num">{result.suggestions.filter(s => s.type === 'critical').length}</div>
                        <div className="stat-label">Critical Issues</div>
                      </div>
                    </div>
                  </div>

                  <div className="ov-section">
                    <h2>Top Job Match</h2>
                    {result.job_matches[0] && (
                      <div className="top-job-card">
                        <div className="top-job-header">
                          <h3>{result.job_matches[0].title}</h3>
                          <span className="match-badge">{result.job_matches[0].similarity}% match</span>
                        </div>
                        <p className="top-job-company">{result.job_matches[0].company} — {result.job_matches[0].location}</p>
                        <div className="top-job-skills">
                          {result.job_matches[0].matched_skills.map((s, i) => (
                            <span key={i} className="skill-tag matched">{s}</span>
                          ))}
                          {result.job_matches[0].missing_skills.map((s, i) => (
                            <span key={i} className="skill-tag missing">{s}</span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="ov-section">
                    <h2>Resume Preview</h2>
                    <div className="text-preview">{result.text_preview}</div>
                  </div>
                </div>
              )}

              {activeTab === 'skills' && (
                <SkillsPanel skills={result.skills} />
              )}

              {activeTab === 'jobs' && (
                <JobMatches matches={result.job_matches} />
              )}

              {activeTab === 'suggestions' && (
                <Suggestions suggestions={result.suggestions} />
              )}
            </div>
          </main>
        </div>
      )}
    </div>
  );
}

export default App;

