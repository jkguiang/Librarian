import os, sys
import glob

import numpy
import json

def last_access(dir, user):
    ls = os.popen("ls -altrh %s --time=atime" % dir).read()
    lines = ls.split("\n")
    years = []
    for line in lines:
        if user in line and not ":" in line:
            years.append(float(line.split()[-2]))
    if len(years) > 0:
        return int(numpy.max(years))
    else:
        return 0

def get_size(line, thresh_year):
    entries = line.split()
    if len(entries) == 9:
        size = float(entries[4])/(1024*1024*1024*1024)
        if size > 0:
            try:
                year = float(entries[7])
            except:
                return 0, None 
            name = entries[8]
            if year <= thresh_year:
                return size, name
            else:
                return 0, None
        else:
            return 0, None
    else:
        return 0, None


def old_files(dir, thresh_year):
    total_size = 0
    files = []
    
    ls = os.popen("ls -alR %s --time=atime | grep .*\.root" % dir).read()
    lines = ls.split("\n")
    for line in lines:
        size, name = get_size(line, thresh_year)
        if size > 0:
            total_size += size
            files.append(dir + "/" + name)

    return total_size, files



user_dirs = glob.glob("/hadoop/cms/store/user/*")
results = {}
results_short = {}

thresh_year = 2015 # find all .root files last accessed 201X or earlier

for dir in user_dirs:
    user = dir.split("/")[-1]
    total_size, files = old_files(dir, thresh_year)
    results[user] = { "size" : total_size, "files" : files }
    results_short[user] = { "size" : total_size, "files" : len(files) }
    with open("hadoop_summaries/summary_%s.txt" % user, "w") as f_out:
        f_out.write("size: %.6f, n_files: %.6f" % (total_size, len(files)))

    with open("hadoop_summaries/delete_files_%s.sh" % user, "w") as f_out:
        for file in files:
            if ".root" in file:
                f_out.write("rm %s\n" % file)

with open("hadoop_user_summary.json", "w") as f_out:
    json.dump(results, f_out, sort_keys = True, indent=4)

with open("hadoop_user_summary_short.json", "w") as f_out:
    json.dump(results_short, f_out, sort_keys = True, indent=4)
