[![Build Status](https://travis-ci.com/mike-seagull/backup_creeper.svg?branch=master)](https://travis-ci.com/mike-seagull/backup_creeper)  
Sweeps daily backups of [OPNsense](https://opnsense.org/) config files
<h4>It only keeps 2 weeks of daily backups, 3 monthly backups, and 1 annual backup by default. It also converts all '%Y-%m-%d_%H:%M:%S' date strings to epoch time</h4>
<code>python src/backup_creeper.py --backupdir ${FULLPATH_TO_BACKUP_DIRECTORY}</code>
<h4>To compile it into a binary</h4>
<code>pyinstaller --distpath bin --onefile src/backup_creeper.py</code>
