// DragAndDrop.jsx

import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Tabs = ['Upload Resume', 'Candidate Results', 'Upload Job Description'];

const DragAndDrop = () => {
  const [activeTab, setActiveTab] = useState(null);
  const [uploadMessage, setUploadMessage] = useState('');
  const [jobId, setJobId] = useState('');
  const [isHovered, setIsHovered] = useState(false);

  const handleDrop = async (e) => {
    e.preventDefault();

    setIsHovered(false);

    const file = e.dataTransfer.files[0];

    if (file && file.type === 'application/pdf' && jobId) {
      try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('jobId', jobId);

        const response = await fetch('http://127.0.0.1:8001/upload', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Upload successful:', data);
          setUploadMessage('File uploaded successfully!');
        } else {
          console.error('Failed to upload file:', response.statusText);
          setUploadMessage('Failed to upload file.');
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        setUploadMessage('Error uploading file.');
      }
    } else {
      console.error('Invalid file format or missing job ID.');
      setUploadMessage('Invalid file format or missing job ID.');
    }
  };

  const handleTabClick = (tabIndex) => {
    console.log(`Clicked on ${Tabs[tabIndex]}`);
    setActiveTab(tabIndex);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsHovered(true);
  };

  const handleDragLeave = () => {
    setIsHovered(false);
  };

  return (
    <div className="container">
      <div className="tabs" style={{ display: 'none' }}>
        {Tabs.map((tab, index) => (
          <Link
            to={`/${tab.replace(/\s/g, '')}`} // Generate a route based on the tab name
            key={index}
            onClick={() => handleTabClick(index)}
            className={`tab ${activeTab === index ? 'active' : ''}`}
          >
            {tab}
          </Link>
        ))}
      </div>
      <div
        className={`drop-area ${isHovered ? 'hovered' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <p>Drag and drop PDF file here</p>
        <input
          type="text"
          placeholder="Enter Job ID"
          value={jobId}
          onChange={(e) => setJobId(e.target.value)}
        />
        {uploadMessage && <p className="upload-message">{uploadMessage}</p>}
      </div>
    </div>
  );
};

export default DragAndDrop;
