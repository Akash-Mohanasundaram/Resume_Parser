// App.jsx

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import DragAndDrop from './DragAndDrop';
import CandidateResults from './CandidateResults';
import UploadJobDescription from './UploadJobDescription';
import NavBar from './NavBar';
import './App.css'; // Ensure that the CSS is properly imported

const App = () => {
  return (
    <Router>
      <div>
        <NavBar /> {/* Include the navigation bar at the top level */}
        <Routes>
          <Route path="/" element={<DragAndDrop />} />
          <Route path="/CandidateResults" element={<CandidateResults />} />
          <Route path="/UploadJobDescription" element={<UploadJobDescription />} />
          <Route path="/UploadResume" element={<DragAndDrop />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
