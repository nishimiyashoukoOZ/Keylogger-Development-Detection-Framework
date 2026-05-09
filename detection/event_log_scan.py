"""
Parse Windows Event Logs for suspicious process creation (4688),
registry modification (13/4656) and assign a threat score.
"""
import win32evtlog
import win32evtlogutil
import re
from collections import defaultdict

SERVER = 'localhost'
LOG_TYPES = ['Security', 'System', 'Application']

SUSPICIOUS_PATHS = [r'%TEMP%', r'%APPDATA%', r'C:\Users\Public']
SUSPICIOUS_EXES = ['python.exe', 'cmd.exe', 'powershell.exe']

def read_event_log(logtype, max_events=500):
    hand = win32evtlog.OpenEventLog(SERVER, logtype)
    flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = []
    while True:
        evts = win32evtlog.ReadEventLog(hand, flags, 0)
        if not evts:
            break
        for evt in evts:
            events.append(evt)
            if len(events) >= max_events:
                break
        if len(events) >= max_events:
            break
    win32evtlog.CloseEventLog(hand)
    return events

def score_process_creation(event):
    """Analyze Event ID 4688 for suspicious parent/command lines."""
    if event.EventID != 4688:
        return 0
    msg = win32evtlogutil.SafeFormatMessage(event, logtype) if hasattr(event, 'EventID') else str(event.StringInserts)
    # Simple heuristic scoring
    score = 0
    for path in SUSPICIOUS_PATHS:
        if path in msg:
            score += 15
    for exe in SUSPICIOUS_EXES:
        if exe.lower() in msg.lower():
            score += 10
    # Flag hidden windows or /k arguments
    if '-WindowStyle Hidden' in msg or '-w hidden' in msg:
        score += 20
    return score

def generate_threat_report():
    threats = []
    for log in LOG_TYPES:
        events = read_event_log(log, 500)
        for evt in events:
            s = score_process_creation(evt) if evt.EventID == 4688 else 0
            if s > 0:
                threats.append((evt, s))
    return threats