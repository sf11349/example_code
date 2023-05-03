from flask import Flask, render_template,url_for,request
import sqlite3 as sql
from jobslist import JobsList
from datetime import date, timedelta

#config
DB = 'jobs.db'
WEB_SITE_URL = 'http://127.0.0.1:5000'

app = Flask(__name__)

TD = date.today().strftime("%d-%m-%Y")
REM_START = 'I3'
REM_LEN=7

AGENT = ''
TESTED_AGENTS={'iPhone':'mobile',
               'Macintosh':'mobile',
               'Windows NT':'laptop'  
}          




def get_all_jobs():
    conn = sql.connect(DB, check_same_thread=False)
    conn.row_factory = sql.Row
    c = conn.cursor()
    c.execute(f" Select * \
                from job_list \
                where active = 1 \
                 and id not in (select id from job_list  \
                                 where (submited_date IS not Null  and remittance_date is not null) \
                                 ) \
                 order by datetime(submited_date) \
                 ")
    data = c.fetchall() 
    conn.close()
    return data

def get_all_jobs_view_db():
    conn = sql.connect(DB, check_same_thread=False)
    conn.row_factory = sql.Row
    c = conn.cursor()
    c.execute(f" Select * \
                from job_list \
                ")
    data = c.fetchall() 
    conn.close()
    return data

def get_a_job(id):
    conn = sql.connect(DB, check_same_thread=False)
    conn.row_factory = sql.Row
    c = conn.cursor()
    c.execute(f"Select * \
                from job_list \
                where id = {int(id)} ")
    data = c.fetchall() 
    print(data)
    conn.close()
    return data

def get_today_jobs():
    conn = sql.connect(DB, check_same_thread=False)
    conn.row_factory = sql.Row
    c = conn.cursor()
    c.execute(f"Select * \
                from job_list \
                where submited_date = '{TD}' ")
    data = c.fetchall() 
    print(data)
    conn.close()
    return data


def update_display(id,num,comments,active):
    update_a_job(id,num,comments,active)
    return get_a_job(id)
    

def update_a_job(id,num,comments,active):
    print(f"{id} {num} {comments}")
    conn = sql.connect(DB, check_same_thread=False)
    conn.row_factory = sql.Row
    c = conn.cursor()
    
    c.execute(f"update job_list \
                set job_no = '{(num.upper())}', \
                    comments = '{comments.upper()}', \
                    active = {active} \
                    where id = {int(id)} ")
    conn.commit()
    conn.close()
    return 0


def submit_a_job(num,comments):
    print(f"{num} {comments}")
    conn = sql.connect(DB, check_same_thread=False)
    conn.row_factory = sql.Row
    c = conn.cursor()
    
    # see if the job already exists
    # if exist update date submitted and comments 
    
    c.execute (f"Select count(*) ct from job_list where job_no = '{num.upper()}'")
    ct = c.fetchall()
    item_0_in_result = [_[0] for _ in ct]
    print(item_0_in_result)
    
    if item_0_in_result[0] > 0:
        pass
        # number exists
        # update only comments
        c.execute (f" UPDATE job_list \
                      SET submited_date = '{TD}', \
                        comments = '{comments}' \
                        where job_no = '{num.upper()}'  ")
        conn.commit()           
    else:
        pass
        # insert new record
        c.execute("INSERT INTO job_list(job_no,submited_date,comments) VALUES (:job_no, :submited_date, :comments)", 
                   {'job_no': num.upper(), 'submited_date': TD, 'comments':comments.upper()})
        conn.commit()  
    
    conn.close()
    return 0



def display_today_submitted():
     return get_today_jobs()
    

def get_rem_list(txt):
    print(f'This a {AGENT}')
    split_txt = str(txt).split()
    dic_lst = {}
    if split_txt != []:
        for i in range(len(split_txt)):
            print(split_txt[i])
            if str(split_txt[i]).startswith(REM_START ) and len(str(split_txt[i])) == REM_LEN :
                dic_lst[split_txt[i]] = split_txt[i+1]
                
    print(dic_lst)
    return dic_lst

def get_rem_ref(txt):
    split_txt = str(txt).split()
    rem_ref = ''
    if split_txt != []:
        for i in range(len(split_txt)):
            print(split_txt[i])
            if str(split_txt[i]).find('Remittance') != -1:
                rem_ref= f"{split_txt[i]} - {split_txt[i+1]}"
                #exit loop
                break
            print(rem_ref)
    return rem_ref 

def update_db_with_rems (dic_list,rem_ref) :
    print(f"dictionary:{dic_list}")
    print(f"Rem Ref:{rem_ref}")
    
    for k, v in dic_list.items():
        # connect to db
        conn = sql.connect(DB, check_same_thread=False)
        conn.row_factory = sql.Row
        c = conn.cursor()
        
        # check if job number in db
        c.execute (f"Select count(*) ct from job_list where job_no = '{k.upper()}'")
        ct = c.fetchall()
        item_0_in_result = [_[0] for _ in ct]
        print(item_0_in_result)
        # if yes update rematnce date
        # if no imsert new job with remtance date
        if item_0_in_result[0] > 0:
            # number exists
            # update only rematance date
            c.execute (f"   UPDATE job_list \
                            SET remittance_date = '{v}', \
                                remittance_ref = '{rem_ref}' \
                            where job_no = '{k.upper()}'  ")
            conn.commit()           
        else:
            # insert new record
            c.execute("INSERT INTO job_list(job_no,remittance_date, remittance_ref) VALUES (:job_no, :remittance_date, :remittance_ref)", 
                   {'job_no': k.upper(), 'remittance_date': v, 'remittance_ref': rem_ref})
            conn.commit() 
        
        

def display_today_rem(rem_ref):
    conn = sql.connect(DB, check_same_thread=False)
    conn.row_factory = sql.Row
    c = conn.cursor()
    c.execute(f"Select * \
                from job_list \
                where remittance_ref = '{rem_ref}' \
                and remittance_ref  <> '' ")
    data = c.fetchall() 
    print(data)
    conn.close()
    return data

def get_rem_list_mobile(txt):
    print(f'This a {AGENT}')
    split_txt = str(txt).split()
    dic_lst_job = {}
    dic_lst_date = {}
    if split_txt != []:
        count=0
        j = 0
        for i in range(len(split_txt)):
            print(split_txt[i])
            if str(split_txt[i]).startswith(REM_START ) and len(str(split_txt[i])) == REM_LEN :
                dic_lst_job[split_txt[i]] = count
                count += 1
                j = i 
            if str(split_txt[i])== 'Job' and str(split_txt[i+1]) == 'Date' :
                break # exit loop
        j = j + 3 # move after Job No
        for i in range(count):
            dic_lst_date[i] = split_txt[j]
            j += 1
        print (dic_lst_job)
        print(dic_lst_date)
    #update dictionary
    for k,v in dic_lst_job.items():
        dic_lst_job[k] =  dic_lst_date[v]      
    print(dic_lst_job)
    return dic_lst_job




def  get_rem_ref_mobile (txt):
    print(f'This a {AGENT}')
    pass



@app.route("/")
@app.route("/home")
def home():
    global AGENT
    print(get_all_jobs())
    print(request.headers.get('User-Agent'))
    user_agent = request.headers.get('User-Agent')
    
    #debug
    #user_agent =' Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.4 Safari/605.1.15'
    #user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1'
    
    for k,v in TESTED_AGENTS.items():
        position = user_agent.find(k)
        if position > 0:
            AGENT = v
            # found the agent and exit
            break
        else:
            AGENT ='UNTESTED'
    print(AGENT)    
    return render_template('home.html', jobs=get_all_jobs(), site_url=WEB_SITE_URL)

@app.route("/edit", methods=['POST','GET'])
def edit():
    j = ''
    if request.method == 'GET':
        j = request.args.get('id')
    return render_template('edit.html',title='Edit',jobs=get_a_job(j),site_url=WEB_SITE_URL)

@app.route("/update_job", methods=['POST','GET'])
def update_job():
    id=num=comments=active=''
    for key, value in request.form.items():
        print("key: {0}, value: {1}".format(key, value))
    if request.method == 'POST':
        id = request.form.get('id')
        num = request.form.get('job_no')
        comments = request.form.get('comments')
        active = request.form.get('active')
    return render_template('update_job.html',title='update job',jobs=update_display(id,num,comments,active))

@app.route("/submit_job")
def submit_job():
    return render_template('submit.html',title='Submitted Jobs',jobs=display_today_submitted(),site_url=WEB_SITE_URL)

@app.route("/new_submit" , methods=['POST','GET'])
def new_submit():
    num=comments=''
    for key, value in request.form.items():
        print("key: {0}, value: {1}".format(key, value))
    if request.method == 'POST':
        num = request.form.get('job_no')
        comments = request.form.get('comments')
        if num != 'None':
           submit_a_job(num,comments) 
              
    return render_template('submit.html',title='Submitted Jobs',jobs=display_today_submitted(),site_url=WEB_SITE_URL)

@app.route("/new_remit" , methods=['POST','GET'])
def new_remit():
    txt=''
    rem_ref=''
    #for key, value in request.form.items():
    #    print("key: {0}, value: {1}".format(key, value))
    if request.method == 'POST':
        txt = request.form.get('rem_text')
        
        if txt != '':
            rem_list = rem_ref ='' 
            if AGENT == 'laptop':
                rem_list = get_rem_list(txt)
            elif AGENT == 'mobile':
                rem_list = get_rem_list_mobile(txt)
            else :
                print(f"{AGENT}")    
                
            rem_ref = get_rem_ref(txt)
            update_db_with_rems(rem_list,rem_ref) 
              
    return render_template('remittance.html',title='Remittance Jobs',jobs=display_today_rem(rem_ref),site_url=WEB_SITE_URL)



@app.route("/remittance_jobs")
def remittance_jobs():
    return render_template('remittance.html',title='Remittance')

@app.route("/view_db")
def view_db():
    global AGENT
    print(get_all_jobs())
    print(request.headers.get('User-Agent'))
    user_agent = request.headers.get('User-Agent')
    
    #debug
    #user_agent =' Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.4 Safari/605.1.15'
    #user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1'
    
    for k,v in TESTED_AGENTS.items():
        position = user_agent.find(k)
        if position > 0:
            AGENT = v
            # found the agent and exit
            break
        else:
            AGENT ='UNTESTED'
    print(AGENT)    
    return render_template('view_db.html', jobs=get_all_jobs_view_db(), site_url=WEB_SITE_URL)

if __name__ == '__main__':
    app.run(debug=True)