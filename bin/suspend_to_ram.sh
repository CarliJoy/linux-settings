#!/bin/bash
loginctl lock-session
sudo pm-suspend
restart_kwin.sh
