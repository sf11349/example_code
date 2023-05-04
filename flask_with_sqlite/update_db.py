import sqlite3 as sql
from jobslist import JobsList
from datetime import date, timedelta

DB = 'flask_with_sqlite/jobs.db'




def insert_job(job):
    conn = sql.connect('jobs.db',check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO job_list(job_no,submited_date,remittance_date,comments) VALUES (:job_no, :submited_date, :remittance_date, :comments)", 
                   {'job_no': job.job_no, 'submited_date': job.submited_date, 'remittance_date': job.remittance_date, 'comments': job.comments})
    conn.commit()
    conn.close()
    return 0

def add_submitted_job(job):
    conn = sql.connect('jobs.db')
    c = conn.cursor()
    c.execute("INSERT INTO job_list(job_no,submited_date,) VALUES (:job_no, :submited_date)", 
                   {'job_no': job.job_no, 'submited_date': job.submited_date})
    conn.commit()
    conn.close()
    return 0

def add_remittance_date(job_no, remittance_date):
    conn = sql.connect('jobs.db')
    c = conn.cursor()
    c.execute(f"""UPDATE job_list
                 SET remittance_date = '{remittance_date}'
                 WHERE job_no = '{job_no}' """)
    
    conn.commit()
    conn.close()
    return 0

def get_all_jobs():
    conn = sql.connect('jobs.db')
    c = conn.cursor()
    c.execute('Select * from job_list order by id desc')
    a = c.fetchall() 
    conn.close()
    return a

def deactivate_job(job_no):
    conn = sql.connect('jobs.db')
    c = conn.cursor()
    c.execute(f"""
                  UPDATE job_list
                  SET active = 0
                  WHERE job_no = '{job_no}' """)   
    conn.commit()
    conn.close()
    return 0

def activate_job(job_no):
    conn = sql.connect('jobs.db')
    c = conn.cursor()
    
    sql_cmd = f"""
                  UPDATE job_list
                  SET active = 1
                  WHERE job_no = '{job_no}' """
    print(sql_cmd)
    c.execute(sql_cmd)   
    conn.commit()
    conn.close()
    return 0

def truncate_db():
    conn = sql.connect('jobs.db')
    c = conn.cursor()
    
    sql_cmd = f"""
                  DELETE FROM job_list """
    print(sql_cmd)
    c.execute(sql_cmd)   
    conn.commit()
    conn.close()
    return 0

def rebuild_db():
    conn = sql.connect(DB, check_same_thread=False)
    conn.row_factory = sql.Row
    c = conn.cursor()

    drop_tbl = 'DROP TABLE IF EXISTS job_list'
    create_jobs_tbl = """
       CREATE TABLE job_list (
         id integer primary key autoincrement,
         job_no text,
         submited_date text,
         remittance_date text,
         remittance_ref text,
         comments text,
         active int DEFAULT 1
     )
    """
    
    c.execute(drop_tbl)
    conn.commit()
    c.execute(create_jobs_tbl)
    conn.commit()
    conn.close()







job1 = JobsList('abcd'.upper(),(date.today()).strftime("%d-%m-%Y"),None,'phone')
#job2 = JobsList('4444',date.today()-timedelta(days=6),date.today(),None)

#add_submitted_job (job1)
#insert_job(job1)
#insert_job(job2)
#activate_job('2222')
#add_remittance_date('2222',date.today())

#truncate_db()
rebuild_db()

print(get_all_jobs())

