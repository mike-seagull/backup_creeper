#!/usr/bin/env bash

scp  -o LogLevel=quiet $(pwd)/bin/backup_creeper ${REMOTE_USER}@${REMOTE_SERVER}:/usr/local/bin/backup_creeper
ssh  -o LogLevel=quiet ${REMOTE_USER}@${REMOTE_SERVER} /bin/chmod +x /usr/local/bin/backup_creeper