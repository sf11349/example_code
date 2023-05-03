class JobsList:
    """Job list class"""

    def __init__(self,job_no,submited_date,remittance_date,comments):
        self.job_no = job_no
        self.submited_date = submited_date
        self.remittance_date = remittance_date
        self.comments = comments
        
    def __repr__(self):
        return "Job_list('{}', '{}', '{}', '{}')".format(self.job_no, self.submited_date, self.remittance_date,self.comments)