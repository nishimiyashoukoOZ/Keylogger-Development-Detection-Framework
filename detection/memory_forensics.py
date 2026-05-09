"""
Wrapper around Volatility 3 to detect injected memory, suspicious DLLs, etc.
Assumes volatility3 is in PATH and memory image available.
"""
import subprocess
import json
import os

def run_volatility_plugin(memory_dump, plugin, output_json=True):
    cmd = ['vol', '-f', memory_dump, plugin]
    if output_json:
        cmd.extend(['--output', 'json'])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[!] Volatility {plugin} failed: {e.stderr}")
        return []

def detect_malicious_vad(memory_dump):
    """Look for VAD regions with PAGE_EXECUTE_READWRITE."""
    malfind = run_volatility_plugin(memory_dump, 'windows.malfind')
    alerts = []
    for item in malfind:
        if item.get('Protection') == 'PAGE_EXECUTE_READWRITE':
            alerts.append(f" Suspicious VAD in PID {item.get('PID')} at {item.get('Start VPN')}")
    return alerts

def detect_keylogger_strings(memory_dump):
    """Scan dumped process memory for known keylogger artifacts."""
    # Example: run strings via subprocess, but here just a placeholder
    # In real tool, use yara or volatility windows.strings.
    return ["[!] Manual strings analysis needed – see yara rules."]