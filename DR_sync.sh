#!/bin/bash

# This script will stop the Symantec AV scanner during a data sync to the Anaconda Enterprise DR cluster and restart it after the sync is complete. This file can be placed in /opt/anaconda/bin/DR_sync.sh and executed via the following cron: */30 * * * * /opt/anaconda/bin/DR_sync.sh


USER=
DRHOST=

echo "stopping Symantec scanner"

/etc/init.d/rtvscand stop

echo "starting Anaconda DR sync"

path/to/accord -a backup -s --sync-user $USER --sync-node $DRHOST

echo "stopping Symantec scanner"

/etc/init.d/rtvscand start


