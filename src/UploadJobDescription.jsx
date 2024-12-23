import React, { useState } from 'react';

const UploadJobDescription = () => {
  const [formData, setFormData] = useState({
    degree: '',
    experience: '',
    skills: '',
    total_experience: '',
    job_id: '',
    designation: '',
  });
  const [submissionResult, setSubmissionResult] = useState(null);
  const [missingFields, setMissingFields] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check for missing fields
    const missing = Object.keys(formData).filter((key) => !formData[key].trim());
    if (missing.length > 0) {
      setMissingFields(missing);
      setSubmissionResult({ success: false, message: 'Please fill in all fields.' });
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8001/input', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Data sent successfully:', data);
        setSubmissionResult({ success: true, message: 'Data sent successfully!' });
      } else {
        console.error('Failed to send data:', response.statusText);
        setSubmissionResult({ success: false, message: 'Failed to send data.' });
      }
    } catch (error) {
      console.error('Error sending data:', error);
      setSubmissionResult({ success: false, message: 'Error sending data.' });
    }
  };

  return (
    <div>
      <h1>Upload Job Description</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Degree:
          <input type="text" name="degree" value={formData.degree} onChange={handleChange} />
        </label>
        <br />
        <label>
          Experience:
          <input type="text" name="experience" value={formData.experience} onChange={handleChange} />
        </label>
        <br />
        <label>
          Skills:
          <input type="text" name="skills" value={formData.skills} onChange={handleChange} />
        </label>
        <br />
        <label>
          Total Experience:
          <input
            type="text"
            name="total_experience"
            value={formData.total_experience}
            onChange={handleChange}
          />
        </label>
        <br />
        <label>
          Job ID:
          <input type="text" name="job_id" value={formData.job_id} onChange={handleChange} />
        </label>
        <br />
        <label>
          Designation:
          <input type="text" name="designation" value={formData.designation} onChange={handleChange} />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>

      {missingFields.length > 0 && (
        <p style={{ color: 'red' }}>Please fill in the following fields: {missingFields.join(', ')}</p>
      )}

      {submissionResult && (
        <div>
          {submissionResult.success ? (
            <p style={{ color: 'green' }}>{submissionResult.message}</p>
          ) : (
            <p style={{ color: 'red' }}>{submissionResult.message}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default UploadJobDescription;
