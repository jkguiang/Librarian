# Script to create backups on NFS of all hadoop files matching a "magic string"
import os
import glob
import datetime

# Changeable parameters
hadoop_dir = "/hadoop/cms/store/user/namin/ProjectMetis/"
magic_string = "*CMS4_V00-00-06*/"

nfs_dir = "/home/users/snt/"
breathing_room = 10 
    
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

def find_files_in_subdirs(base_dir, magic_string):
  files = []
  dirs = glob.glob(base_dir + magic_string)
  for dir in dirs:
    for root, directory, filenames in os.walk(dir):
      for file in filenames:
	files.append(os.path.join(root, file))
  return files

# Check for files that are not backed up
hadoop_files = find_files_in_subdirs(hadoop_dir, magic_string)
nfs_files = find_files_in_subdirs(nfs_dir, magic_string)

files_need_backup = [file for file in hadoop_files if file.replace(hadoop_dir, nfs_dir) not in nfs_files]

# Check if any files are corrupt
corrupt_files = find_corrupt_files(glob.glob(hadoop_dir+magic_string))

corrupt_files_backed_up = [file for file in corrupt_files if file.replace(hadoop_dir, nfs_dir) in nfs_files]
corrupt_files_not_backed_up = [file for file in corrupt_files if file.replace(hadoop_dir, nfs_dir) not in nfs_files]

# Only back up the non-corrupt ones
files_to_backup = [file for file in files_need_backup if file not in corrupt_files]

# Check if there is enough space to backup these files
size_of_backup = 0 # size of all files that we are going to back up
for file in files_to_backup:
  size_of_backup += float(os.path.getsize(file))
size_of_backup *= 1/(1024.*1024.*1024.*1024.)

free_space = float(os.popen("df %s --block-size=1T | tail -n +3 |  awk '{ print $3 }'" % nfs_dir).read())

# Can we backup?
if free_space - size_of_backup > breathing_room: # backup these files!
  did_backup = True
  for file in files_to_backup:
    os.system("cp %s %s" % (file, file.replace(hadoop_dir, nfs_dir)))    

else:
  did_backup = False

# Now log the results
date = datetime.date.today().strftime("%d") + datetime.date.today().strftime("%B") + datetime.date.today().strftime("%Y")
with open("logs/nfs_backup_%s.txt" % date, "w") as log_file:
  log_file.write("Summary of hadoop backup on NFS disk\n")
  log_file.write("Attempting to backup all files matching %s in %s\n" % (hadoop_dir + magic_string, nfs_dir)) 
  log_file.write("Date: %s \n" % datetime.datetime.now())
  log_file.write("The following new files appeared: \n")
  for file in files_need_backup:
    log_file.write("    %s \n" % file)
  if not did_backup:
    log_file.write("But none were backed up because it would mean only %d TB of free space in NFS disk\n" % free_space - size_of_backup)
    log_file.write("And %d TB has been chosen as the amount of comfortable breathing room for NFS disk\n" % breathing_room)
  else:
    log_file.write("Of these, the following were backed up: \n")
    for file in files_to_backup:
      log_file.write("    %s \n" % file)
    log_file.write("The following files were not backed up because they are corrupt: \n")
    for file in corrupt_files_not_backed_up:
      log_file.write("    %s \n" % file)
    log_file.write("The following files are corrupt, but are already backed up on NFS (let Nick know so he can cp the healthy backups!): \n")
    for file in corrupt_files_backed_up:
      log_file.write("    %s \n" % file)
