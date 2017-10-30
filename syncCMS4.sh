basedir="/hadoop/cms/store/user/namin/ProjectMetis/"
dir="*CMS4_V00-00-06*/"
backupDir="/home/users/snt/"

logFile="/home/users/sjmay/Librarian/backupSummary.txt"

# Find size of CMS4 currently on hadoop (in TB)
du -ch $basedir$dir > usageHadoop.txt --block-size=1T
grep "total" usageHadoop.txt > nTBusedHadoop.txt
nTBHadoop=$(<nTBusedHadoop.txt)
# Now extract number from nTB
nTBHadoop=$(echo $nTBHadoop | sed 's/[^0-9]*//g')

# Find size of CMS4 currently backed up on NFS (in TB)
du -ch $backupDir > usageNFS.txt --block-size=1T 
grep "total" usageNFS.txt > nTBusedNFS.txt
nTBNFS=$(<nTBusedNFS.txt)
# Now extract number from nTB
nTBNFS=$(echo $nTBNFS | sed 's/[^0-9]*//g')

# Find how much free space there is on NFS disk (in TB)
df /home/users/snt/ --block-size=1T | tail -n +3 |  awk '{ print $3 }' > nTBFreeNFS.txt # this grabs the 3rd argument of the 3rd line of df's output
nTBFreeNFS=$(<nTBFreeNFS.txt)

# Calculate how much free space there will be if we back up again
echo "Date: "$(date)", attempting to backup CMS4" >> $logFile
echo "Space remaining after rsync:" >> $logFile
nTBtoTransfer=$((nTBHadoop-nTBNFS))
nTBRemaining=$((nTBFreeNFS-nTBtoTransfer))
echo $nTBRemaining >> $logFile

breathingRoom=10
if (($nTBRemaining > $breathingRoom))
then
  echo "Enough space to backup. Running rsync" >> $logFile
  rsync -a $basedir $backupDir --include $dir'***' --exclude '*' >> $logFile
else
  echo "Not enough breathing room ("$nTBRemaining" TB), did not backup" >> $logFile
fi 
