#!/bin/bash
LOGFILE="/tmp/kwin.log"
export __GL_YIELD="USLEEP"
echo " ***** Restart kwin $(date)" >> $LOGFILE
kwin --replace >> $LOGFILE 2>&1  &

