# Keylogger Detection Framework

A comprehensive cybersecurity lab project for detecting and analyzing keylogger threats through multiple detection mechanisms.

## Project Overview

This framework demonstrates both offensive (keylogger) and defensive (detection) components for educational purposes in controlled lab environments only.

### Components

- **Keylogger Module**: Low-level keyboard monitoring, persistence mechanisms, and data exfiltration
- **Detection Module**: Event log scanning, memory forensics, YARA rule matching, and network anomaly detection

## Directory Structure

```
Keylogger_Detection_Framework/
├── keylogger/          # Offensive component (LAB ONLY)
│   ├── hook.py        # Low-level keyboard hook & logging
│   ├── persist.py     # Persistence via registry & scheduled tasks
│   └── exfil.py       # Encryption + HTTP exfiltration
├── detection/         # Defensive analysis component
│   ├── event_log_scan.py       # Windows event log analysis
│   ├── memory_forensics.py     # Process memory inspection
│   ├── yara_rules.py           # Malware pattern matching
│   └── network_scan.py         # Network traffic analysis
├── run_keylogger.py   # Offensive entry point (LAB ONLY)
└── run_detection.py   # Defensive analysis entry point
```

## Requirements

See `requirements.txt` for dependencies.

## Usage

### Detection (Defensive)
```bash
python run_detection.py
```

### Keylogger (Offensive - LAB ONLY)
```bash
python run_keylogger.py
```

## ⚠️ Legal Notice

This framework is for educational purposes in controlled lab environments only. Unauthorized access to computer systems is illegal. Use only on systems you own or have explicit permission to test.
