"""
YARA rules to detect keylogger payload patterns and registry persistence.
"""
import yara

RULES = """
rule keylogger_xor_header {
    strings:
        $xor_magic = { 78 6f 72 5f 68 65 61 64 }   // "xor_head" in xored form
    condition:
        $xor_magic
}

rule registry_run_key {
    strings:
        $reg1 = "Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run"
        $reg2 = "WindowsHelper"
    condition:
        all of them
}
"""

def compile_and_scan(file_path):
    rules = yara.compile(source=RULES)
    matches = rules.match(file_path)
    return matches