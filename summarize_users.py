import glob
import json

users = glob.glob("hadoop_summaries/*.txt")

total_size = 0.0
summary = {}

for user_file in users:
    user = user_file.replace("summary_","").replace(".txt", "")
    with open(user_file, "r") as f_in:
        lines = f_in.readlines()
        info = lines[0].split()
        size = float(info[1][:-1])
        total_size += size
        if size > 1.:
            print user, size
            summary[user] = { "size" : str(size) + " TB", "script" : "/home/users/smay/Librarian/hadoop_summaries/delete_files_%s.sh" % user }

summary["all"] = { "size" : str(total_size) + " TB", "script" : "/home/users/smay/Librarian/hadoop_summaries/delete_files_*.sh" }

with open("hadoop_deletion_summary_2019.json", "w") as f_out:
    json.dump(summary, f_out, sort_keys = True, indent = 4)
