from hh import get_jobs as hh_get_jobs #loading function from a hh.py file
from so import get_jobs as so_get_jobs #loading function from a so.py file
from save import save_to_csv #loading function from a save.py file


#assing the parsing data
hh_jobs = hh_get_jobs() 
so_jobs = so_get_jobs()

#concatenation data
jobs = hh_jobs + so_jobs

#save data to csv file
save_to_csv(jobs)