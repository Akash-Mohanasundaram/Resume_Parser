import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css';

const Tabs = ['Upload Resume', 'Candidate Results', 'Upload Job Description'];

const NavBar = () => {
  return (
    <div className="navbar">
      <div className="title-tab">
        Resume Parser
      </div>
      <div className="tabs">
        {Tabs.map((tab, index) => (
          <Link key={index} to={`/${tab.replace(/\s/g, '')}`} className="tab">
            {tab}
          </Link>
        ))}
      </div>
    </div>
  );
};

export default NavBar;
