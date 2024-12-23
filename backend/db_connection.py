import pymssql



def db_connection():
    conn = pymssql.connect(
    host=r'',
    user=r'',
    password=r'' ,
    database=''
    )
    return(conn)


conn = db_connection()
cursor = conn.cursor(as_dict = true)

query = 'CREATE TABLE hackathon_job_details_table (id INT PRIMARY KEY IDENTITY(1,1), degree NVARCHAR(255), experience int, skills NVARCHAR(MAX), total_experience int, job_id NVARCHAR(20), designation NVARCHAR(255))'
try:
    cursor.execute(query)
    conn.commit()
    
except Exception as e:
        print(f"Error: {str(e)}")
finally:
    cursor.close()
    conn.close()