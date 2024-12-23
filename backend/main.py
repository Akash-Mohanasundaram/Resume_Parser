import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from pyresparser import ResumeParser
import pymssql

app = Flask(__name__)
CORS(app)

# Get the current working directory
current_working_directory = os.getcwd()

# Create the UPLOAD_FOLDER path within the working directory
UPLOAD_FOLDER = os.path.join(current_working_directory, "upload_folder")

# Check if the UPLOAD_FOLDER directory exists, and create it if not
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def db_connection():
    conn = pymssql.connect(
    host=r'',
    user=r'',
    password=r'' ,
    database=''
    )
    return(conn)

def retrieve_standards(job_id):
    try:
        conn = db_connection()
        cursor = conn.cursor(as_dict = True)

        # Execute a query to retrieve standards for the given job_id
        query = f"SELECT degree, experience, skills, total_experience, designation FROM hackathon_job_details_table WHERE job_id = {job_id}"
        cursor.execute(query)
        standards = cursor.fetchall()

        return standards[0]

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

    finally:
        cursor.close()
        conn.close()

def extract_degree_levels(degree_string):
    # Extract and lowercase degree levels
    degree_levels = ['bachelor' if 'bachelor' in degree.lower() else 'masters' if 'masters' in degree.lower() else degree.lower() for degree in degree_string]
    return degree_levels



def compare_data(data, job_id):
    try:
        # Retrieve standards for the given job_id
        standards = retrieve_standards(job_id)
        if standards is None:
            print("Error: Standards not found for the given job_id.")
            return jsonify("Could not find job id")

        # Compare data with standards
        comparison_result = {}

        # Initialize variables for comparison results
        is_degree_satisfied = "No"
        is_experience_satisfied = "No"
        is_skills_satisfied = "No"
        comparison_result_description = ""

        for key in data:
            if key in ["skills", "degree", "experience"]:
                if key == 'experience':
                    if data['total_experience'] >= float(standards[key]) and data['total_experience'] <= float(standards['total_experience']):
                        print(f"{data['total_experience']} years of experience meets standards.")
                        is_experience_satisfied = "qualified"
                    else:
                        if int(data['total_experience']) > int(standards[key]):
                            print(f"Overqualified based on experience. Maximum years required {standards['total_experience']}, candidate experience {data['total_experience']}")
                            comparison_result_description = "Overqualified based on experience"
                            is_experience_satisfied = "Overqualified"
                        else:
                            print(f"Underqualified based on experience. Maximum years required {standards['total_experience']}, candidate experience {data['total_experience']}")
                            comparison_result_description = "Underqualified based on experience"
                            is_experience_satisfied = "Underqualified"

                elif key == 'skills':
                    set_of_skills_of_candidate = set(map(str.lower, data[key]))
                    skill_reqd = list(map(str.lower, standards[key].split(', ')))
                    count = 0
                    reqd_count = len(skill_reqd)

                    for skill in skill_reqd:
                        skill = skill.strip()
                        if skill in set_of_skills_of_candidate:
                            count += 1
                    print(f"Skills Matched: {count}/{reqd_count}")
                    is_skills_satisfied = f"Matched {count}/{reqd_count} required skills" if count == reqd_count else f"Matched {count}/{reqd_count} required skills"
                    comparison_result_description = f"Matched {count}/{reqd_count} required skills"

                elif key == 'degree':
                    # Extract and compare degree levels
                    candidate_degree_levels = extract_degree_levels(data[key])

                    if("Bachelor's" in standards[key] and 'masters' in candidate_degree_levels):
                        print(f"Overqualified {key}: {data[key]} vs {standards[key]}")
                        is_degree_satisfied = "Overqualified"
                        comparison_result_description = "Overqualified based on degree"
                    elif("Bachelor's" in standards[key] and 'bachelor' in candidate_degree_levels):
                        print(f"Qualified {key}: {data[key]} vs {standards[key]}")
                        is_degree_satisfied = "Qualified"
                        comparison_result_description = "Qualified based on degree"
                    else:
                        print(f"Underqualified {key}: {data[key]} vs {standards[key]}")
                        comparison_result_description = "Underqualified based on degree"

        # Insert data into the Candidates table using parameterized query
        conn = db_connection()
        cursor = conn.cursor(as_dict = True)
        degree_string = ' '.join(i.replace("'", "") for i in data['degree'])
        experience_string = ' '.join(i.replace("'", "") for i in data['experience'])
        skills_string = ' '.join(i.replace("'", "") for i in data['skills'])
        if(data['total_experience']<0):
            experience=0
        else:
            experience=data['total_experience']
        insert_query = f"""
        INSERT INTO Candidates (name, degree, experience, total_experience, skills, job_id,
                                comparison_result_description, is_degree_satisfied, 
                                is_experience_satisfied, is_skills_satisfied)
        VALUES ('{data['name']}', '{degree_string}', '{experience_string}',
                '{experience}', '{skills_string}', '{job_id}',
                '{comparison_result_description}', '{is_degree_satisfied}',
                '{is_experience_satisfied}', '{is_skills_satisfied}')
        """

        cursor.execute(insert_query)

        # print(insert_query)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify("Compared data and inserted into Candidates table")

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def fetch_candidates():
    try:
        # Connect to the database
        conn = db_connection()
        cursor = conn.cursor(as_dict=True)

        # Execute the query to fetch candidates
        cursor.execute('SELECT * FROM Candidates')
        candidates = cursor.fetchall()

        # Close the database connection
        conn.close()

        return candidates

    except Exception as e:
        print(f"Error fetching candidates: {str(e)}")
        return None


@app.route('/retrieve', methods=['GET'])
def get_candidates():
    candidates = fetch_candidates()

    if candidates is not None:
        return jsonify(candidates)

    return jsonify({'error': 'Failed to fetch candidates'}), 500

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        try:
            # Use ResumeParser to extract data directly from the uploaded PDF file
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.pdf')
            file.save(pdf_path)
            data = ResumeParser(pdf_path).get_extracted_data()

            # # Access the extracted data
            # degree = data.get('degree', '')
            # skills = data.get('skills', '')
            # # You can access other keys as needed

            compare_data(data, 12345)

            # Create a JSON response
            response_data = {'success': True, 'data':data}
            return jsonify(response_data)

        except Exception as e:
            error_message = f'Error: {str(e)}'
            response_data = {'success': False, 'error': error_message}
            return jsonify(response_data)

def insert_data(degree, experience, skills, total_experience, job_id, designation):
    try:
        # Connect to the database
        conn = db_connection()
        cursor = conn.cursor()

        # Execute the dynamic INSERT query
        degree = degree.replace("'","''")
        query = f"INSERT INTO hackathon_job_details_table (degree, experience, skills, total_experience, job_id, designation) VALUES ('{degree}', '{experience}', '{skills}', '{total_experience}', '{job_id}', '{designation}')"
        cursor.execute(query)

        # Commit the transaction
        conn.commit()
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

    finally:
        # Close the connection
        cursor.close()
        conn.close()


@app.route('/input', methods=['POST'])
def get_input():
    try:
        # Get JSON data from the POST request
        input_data = request.get_json()

        # Extract parameters from JSON
        degree = input_data.get('degree', '')
        experience = input_data.get('experience', '')
        skills = input_data.get('skills', '')
        total_experience = input_data.get('total_experience', '')
        job_id = input_data.get('job_id', '')
        designation = input_data.get('designation', '')

        # Insert data into the database
        success = insert_data(degree, experience, skills, total_experience, job_id, designation)
        
        if success:
            return jsonify({'success': True, 'message': 'Data inserted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to insert data'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/test', methods=['POST'])
def check_if_working():
    if request.method == 'POST':
        result = 'Success'
    else:
        result = 'Failure: Only POST requests are accepted'

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=8001)
