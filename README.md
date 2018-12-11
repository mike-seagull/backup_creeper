[![Build Status](https://travis-ci.org/mike-seagull/backup_sweeper.svg?branch=master)](https://travis-ci.org/mike-seagull/backup_sweeper)
Sweeps daily backups of [OPNsense](https://opnsense.org/) config files
<h4>It only keeps 2 weeks of daily backups, 3 monthly backups, and 1 annual backup by default</h4>
<code>python src/backup_sweeper.py --backupdir ${FULLPATH_TO_BACKUP_DIRECTORY}</code>
<h4>To compile it into a binary</h4>
<code>pyinstaller --distpath bin --onefile src/backup_sweeper.py</code>
