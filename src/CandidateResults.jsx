import React, { useState, useEffect } from 'react';

const CandidateResults = () => {
  const [candidateData, setCandidateData] = useState([]);

  useEffect(() => {
    // Fetch data from your API endpoint or server
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8001/retrieve'); // Replace with your API endpoint
        if (response.ok) {
          const data = await response.json();
          setCandidateData(data);
        } else {
          console.error('Failed to fetch data:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Call the fetchData function
    fetchData();
  }, []); // Empty dependency array ensures that this effect runs once when the component mounts

  const handleSelection = (candidateId, status) => {
    // Handle the selection logic (accept/reject) here
    console.log(`Candidate ${candidateId} ${status}`);
  };

  return (
    <div>
      <h1>Candidate Results</h1>
      <table border="1">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Degree</th>
            <th>Skills Satisfied</th>
            <th>Experience Satisfied</th>
            <th>Degree Satisfied</th>
            <th>Overall Result</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {candidateData.map((candidate) => (
            <tr key={candidate.candidate_id}>
              <td>{candidate.candidate_id}</td>
              <td>{candidate.name}</td>
              <td>{candidate.degree}</td>
              <td>{candidate.is_skills_satisfied}</td>
              <td>{candidate.is_experience_satisfied}</td>
              <td>{candidate.is_degree_satisfied}</td>
              <td>{candidate.comparison_result_description}</td>
              <td>
                <button
                  onClick={() => handleSelection(candidate.candidate_id, 'accepted')}
                  style={{ backgroundColor: 'green', color: 'white' }}
                >
                  Accept
                </button>
                <button
                  onClick={() => handleSelection(candidate.candidate_id, 'rejected')}
                  style={{ backgroundColor: 'red', color: 'white' }}
                >
                  Reject
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CandidateResults;
