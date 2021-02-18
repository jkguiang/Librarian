import glob
import os
import json

users = glob.glob("/hadoop/cms/store/user/*/")

results = {}

for user in users:
    command = "hadoop fs -du -s -h %s" % user.replace("/hadoop", "")
    print command
    output = os.popen(command).read().split()
    tb_plus = False
    for entry in output:
        if entry == "T":
            tb_plus = True

    if not tb_plus:
        continue

    size = float(output[2])
    results[user.split("/")[-2]] = size


#inv_map = {v : k for k, v in results.iteritems()}
with open("hadoop_full_usage.json", "w") as f_out:
    json.dump(results, f_out, sort_keys=True, indent=4)
