#!/usr/bin/env bash

scp $(pwd)/bin/backup_sweeper ${REMOTE_USER}@${REMOTE_SERVER}:/usr/local/bin/backup_sweeper
ssh ${REMOTE_USER}@${REMOTE_SERVER} /bin/chmod +x /usr/local/bin/backup_sweeper