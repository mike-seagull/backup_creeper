#!/usr/bin/env bash

scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no $(pwd)/bin/backup_sweeper ${REMOTE_USER}@${REMOTE_SERVER}:/usr/local/bin/backup_sweeper
ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_SERVER} /bin/chmod +x /usr/local/bin/backup_sweeper