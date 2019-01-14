# Script to create backups on NFS of all hadoop files matching a "magic string"
import os
import glob
import datetime

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--location", help = "path to directory(s) to check for corruptions. Can include wildcards", type=str)
args = parser.parse_args()

def find_corrupt_files(paths):
  corruptions = "corruptions.txt"

  os.system("touch %s" % corruptions)
  os.system("rm %s" % corruptions)
  for path in paths:
    os.system("hdfs fsck %s >> %s" % (path.replace("/hadoop",""), corruptions))

  fnames = []
  with open(corruptions, "r") as fhin:
      for line in fhin:
          if "CORRUPT" not in line: continue
          if ".root" not in line: continue
          fname = line.split()[0].replace(":","")
          fnames.append("/hadoop"+fname)
  return fnames  

# Check if any files are corrupt
corrupt_files = find_corrupt_files(glob.glob(args.location))

# Now log the results
date = datetime.date.today().strftime("%d") + datetime.date.today().strftime("%B") + datetime.date.today().strftime("%Y")
with open("logs/run2_CMS4_corruptions_%s.txt" % date, "w") as log_file:
  log_file.write("Checking for hadoop corruptions\n")
  log_file.write("Date: %s \n" % datetime.datetime.now())
  log_file.write("\n The following files are corrupt: \n") 
  for file in corrupt_files:
    log_file.write("    %s \n" % file)
  log_file.write("\n To delete them, exexcute the following commands: \n")
  for file in corrupt_files:
    log_file.write("    rm %s \n" % file)
