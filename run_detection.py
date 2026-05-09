#!/usr/bin/env python3
"""
Run all detection modules and print a report.
"""
from detection.event_log_scan import generate_threat_report
from detection.yara_rules import compile_and_scan
from detection.network_scan import find_exfil_beacons
import os

if __name__ == "__main__":
    print("[*] Starting detection framework...")
    # Event log scan
    threats = generate_threat_report()
    print(f"[+] Found {len(threats)} suspicious process creation events.")
    for evt, score in threats[:5]:   # show top 5
        print(f"    Event ID {evt.EventID}, Score: {score}")

    # YARA scan on current directory
    matches = compile_and_scan(os.getcwd())
    print(f"[+] YARA matches: {len(matches)}")
    for m in matches:
        print(f"    {m}")

    # Network beacon detection (if pcap provided)
    pcap = "lab_capture.pcap"   # replace with actual path
    if os.path.exists(pcap):
        beacons = find_exfil_beacons(pcap)
        print(f"[+] Exfiltration beacons: {len(beacons)}")
        for b in beacons:
            print(f"    {b}")
    else:
        print("[!] No pcap file found – skipping network analysis.")