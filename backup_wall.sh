#!/bin/bash
# Nightly Wall of support + daily log (day-* keys) backup. Saves dated JSON to /workspace/tomas-review/wall-backup/
# and puts back any post that went missing since the last backup.
# OneDrive copy: the routine that runs this should then upload the newest
# /workspace/tomas-review/wall-backup/wall-live-*.json to OneDrive /Innovo/Tomas/wall-backup/.
set -e
OUT=/workspace/tomas-review/wall-backup
python3 /workspace/tomas-level-up/wall_tool.py backup "$OUT"
ls -t "$OUT"/wall-live-*.json | head -1
