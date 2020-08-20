import datetime
from datetime import datetime, date, timedelta

def get_cur_date():
    return date.today().strftime("%Y-%m-%d")

def get_pre_n_date(n):
    return (date.today() + timedelta(days=-n)).strftime("%Y-%m-%d")
