#!/bin/bash
# Lancia generate.py completamente sganciato (sopravvive alla chiusura della sessione)
cd /mnt/c/projects/fiabe || exit 1
COQUI_TOS_AGREED=1 setsid nohup /home/deckard/tts-venv/bin/python generate.py \
  > /mnt/c/projects/fiabe/generation.log 2>&1 < /dev/null &
echo "launched pid $!"
