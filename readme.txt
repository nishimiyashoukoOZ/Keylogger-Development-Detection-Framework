Keylogger Development & Detection Framework
Python | Windows API | Memory Forensics

Overview
This project is a dual-purpose cybersecurity research framework designed to understand the offensive techniques behind kernel-level keystroke interception and to develop robust detection mechanisms against such threats. It consists of two integrated components:

Offensive Module – A stealthy, low-level keylogger built in Python using native Windows API hooks.

Defensive Module – A forensic analysis toolkit that detects Indicators of Compromise (IoCs) left by keyloggers in Event Logs, process memory, and system behaviour.

The goal was not to create malware, but to simulate realistic attack patterns in a controlled lab environment and then build and validate detection logic that could be used by blue teams.

1. Keylogger Development (Offensive)
Architecture
Language: Python 3.10+ with ctypes and pywin32 for direct Windows API access.

Core Technique: SetWindowsHookEx with WH_KEYBOARD_LL – a low-level keyboard hook that captures keystrokes before they reach the target application.

Stealth Enhancements:

Registration of the hook inside a hidden message-only window to avoid console visibility.

Thread-level hooking, avoiding system-wide DLL injection while still capturing all keystrokes.

Exfiltration via periodic HTTP POST requests to a dummy C2 server; data is encrypted using a rotating XOR key before transmission.

Process name masquerading and auto-start persistence via a Run registry key.

Implementation Details
Keystroke Interception:
The hook procedure, written in pure Python, converts virtual key codes to human-readable strings, distinguishing between printable characters, modifier keys (Shift, Ctrl), and special keys (Enter, Tab, Backspace). State tracking handles Caps Lock and Shift to accurately reconstruct case-sensitive text.

Logging & Exfiltration Pipeline:
Captured keystrokes are cached locally in an obfuscated temp file. When the buffer exceeds a threshold or a timer elapses, the data is serialized, encrypted, and sent to a remote listener using a lightweight Python HTTP client.

Persistence:
The script drops a stager in %APPDATA% and creates a scheduled task triggered by user logon, ensuring resilience across reboots.

Safety Precautions
All offensive code was executed exclusively on an air-gapped Windows 10 virtual machine, with no connection to production networks. The local detection module was then used to analyse the generated artifacts.

2. Detection Framework (Defensive)
The defensive module analyses the very artifacts the keylogger creates, providing actionable threat-hunting capabilities.

A. Windows Event Log Analysis
A Python parser extracts and correlates suspicious patterns from Security, System, and Application logs:

Event ID 4688 (Process Creation): Searches for processes launched from unusual temporary directories (%TEMP%, %APPDATA%) with Python interpreters.

Event ID 13 (Registry Modification): Alerts on modifications to HKCU\Software\Microsoft\Windows\CurrentVersion\Run.

Event ID 4656 (Handle Request): Flags processes requesting PROCESS_VM_READ on lsass.exe or other high-value targets, often indicative of credential dumping companions.

A correlation engine scores events based on a weighted risk matrix, generating a composite “Threat Score” that reduces false positives.

B. Process Memory Forensics
Using the Volatility 3 framework (wrapped with Python automation), the toolkit performs:

Malfind and Vadwalk: Scans for injected memory regions with PAGE_EXECUTE_READWRITE permissions, a hallmark of code injection often used alongside keyloggers.

DLL List & Handles: Identifies hidden or unlinked DLLs loaded by the suspicious process.

String Extraction: Dumps the process memory and scans for entropy patterns consistent with XOR‑encrypted keylog buffers, as well as cleartext artifacts like key‑state arrays.

The Python wrapper automates memory acquisition (via WinPMem), feeds the dump to Volatility, and parses JSON output to flag anomalies against a baseline of known‑good system state.

C. Network & File System IoCs
YARA Rules: Custom YARA signatures detect the specific byte sequences of the Python keylogger’s encrypted payload header and the registry persistence string.

Network Anomaly Detection: A pcap analyser identifies periodic, small‑sized HTTPS POST requests to non‑standard user‑agent strings, correlating them with process creation timestamps.

Results & Key Findings
Detection Accuracy: The framework successfully reconstructed keystroke logs from memory dumps and identified the malicious process with a Threat Score of 92/100, based purely on Windows Event Log telemetry.

Noise Reduction: Correlation of process creation, registry change, and memory protection flags eliminated false positives from benign Python scripts.

Operational Insight: The project demonstrated that while user‑land hooks are stealthy, their side‑effects—handle requests, executable memory pages, and predictable network patterns—are detectable with the right telemetry stack.

Technologies & Skills Demonstrated
Windows API Programming (SetWindowsHookEx, GetMessage, memory management)

Python System Programming (ctypes, pywin32, subprocess automation)

Memory Forensics (Volatility 3, WinPMem)

Log Analysis & Correlation (Python pandas, Windows Event Log XML parsing)

Threat Hunting (YARA, entropy analysis, IoC scoring)

Safe Lab Practices (isolation, snapshots, ethical guidelines)