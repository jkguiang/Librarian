import json

with open("home_usage.txt", "r") as f_in:
    lines = f_in.readlines()

results = {}

for line in lines:
    info = line.split()
    if "T" not in info[0]:
        continue
    if "total" in info[1]:
        continue

    user = info[1].split("/")[-2]
    results[user] = float(info[0][:-1])

inv = { v : k for k,v in results.items() }

with open("home_usage_sorted.json", "w") as f_out:
    json.dump(inv, f_out, sort_keys=True, indent =4)
