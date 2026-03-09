#!/bin/bash
LOG="/root/clawd/memory/pending-checks.log"
TS=$(date '+%Y-%m-%d %H:%M:%S')
GEMINI=$(curl -s -m 10 "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"text":"Hi"}]}]}' 2>/dev/null | python3 -c "import json,sys;r=json.load(sys.stdin);print('OK' if 'candidates' in r else 'FAIL')" 2>/dev/null)
DOGADO=$(python3 -c "import socket;s=socket.socket();s.settimeout(3);s.connect(('web314.dogado.net',22));print('OK');s.close()" 2>/dev/null || echo "FAIL")
echo "$TS | Gemini: $GEMINI | dogado: $DOGADO" >> "$LOG"
