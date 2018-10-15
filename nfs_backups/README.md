# Backup of hadoop files on NFS
`backup.py` searches for all files in directories and subdirectories of `hadoop_dir + magic_string` and attempts to back them up on NFS disk, provided the following stipulations are met:
1. The files are not already present on NFS disk (they are already backed up, so conserve energy for upcoming `cp`-ing).
2. The files are not corrupt (checks with `hdfs fsck`).
3. There will still be greater than `breathing_room` TB of free space on NFS disk after backing up these files.

The script also logs the results in a text file, noting the following:
1. The files it attempted to backup (i.e. files present in `hadoop_dir + magic_string` that are not present in `nfs_dir`).
2. If there was enough space to back all of these up.
3. The files it actually did backup (a la `cp`)
4. The files it did not backup because of corruptions
5. The files that are corrupt, but are already backed up (these should be replaced with the healthy versions on NFS!)

Lines 7-11 of `corrupt.py` can be changed to your desired hadoop directory (and magic string) and NFS destination.

`syncCMS4.sh` is the old version of `corrupt.py` that does not check for file health.
