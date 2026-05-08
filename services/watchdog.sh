#!/bin/bash

LOG="/home/haakon/pi/logs/watchdog.log"
MARKER="/tmp/tunnel_down_since"

if curl -s --max-time 10 https://tischbein.dev/health > /dev/null 2>&1; then
    rm -f "$MARKER"
    exit 0
fi

NOW=$(date +%s)

if [ ! -f "$MARKER" ]; then
    echo "$NOW" > "$MARKER"
    echo "$(date): Tunnel down, starting timer" >> "$LOG"
    exit 0
fi

DOWN_SINCE=$(cat "$MARKER")
ELAPSED=$((NOW - DOWN_SINCE))

echo "$(date): Tunnel still down, ${ELAPSED}s elapsed" >> "$LOG"

if [ "$ELAPSED" -gt 600 ]; then
    echo "$(date): Rebooting after ${ELAPSED}s downtime" >> "$LOG"
    rm -f "$MARKER"
    sudo reboot
fi
