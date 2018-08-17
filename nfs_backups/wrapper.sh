# Script that is actually called by cron:
# crontab -l: 0 2 * * * /home/users/sjmay/Librarian/nfs_backups/wrapper.sh
export SCRAM_ARCH=slc6_amd64_gcc630
export CMSSW_VERSION=CMSSW_9_4_0
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /cvmfs/cms.cern.ch/$SCRAM_ARCH/cms/cmssw/$CMSSW_VERSION/src
eval `scramv1 runtime -sh`
cd -

if [ ! -d logs/ ]; then
  mkdir logs
fi

python /home/users/sjmay/Librarian/nfs_backups/backup_run2_data2016_94x.py
python /home/users/sjmay/Librarian/nfs_backups/backup_run2_data2017.py

if [ ! -d ~/public_html/nfs_backup_logs/ ]; then
  mkdir ~/public_html/nfs_backup_logs
fi

cp logs/nfs_backup*.txt ~/public_html/nfs_backup_logs/
chmod 755 ~/public_html/nfs_backup_logs
chmod 755 ~/public_html/nfs_backup_logs/*.txt
