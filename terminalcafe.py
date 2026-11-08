#!/usr/bin/env python3
import os
import sys
import time

SCREEN_OPTIONS = [
    "AI Python Session",
    "Code Rain",
    "Build Monitor",
    "Exit",
]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_menu(selected_index):
    clear_screen()
    print("TerminalCafe")
    print("Choose a screensaver")
    print()
    for i, option in enumerate(SCREEN_OPTIONS):
        marker = ">" if i == selected_index else " "
        print(f"{marker} {option}")
    print()
    print("↑/↓ move   Enter select   q quit")


def get_key():
    if os.name == "nt":
        import msvcrt
        return msvcrt.getwch()

    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            seq = sys.stdin.read(2)
            if seq == "[A":
                return "UP"
            if seq == "[B":
                return "DOWN"
            return "ESC"
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def fake_type(text, delay=0.03, stream=sys.stdout):
    for ch in text:
        stream.write(ch)
        stream.flush()
        time.sleep(delay)


def run_fake_ai_session():
    clear_screen()
    print("TerminalCafe // AI Python Session")
    print("AI assistant typing... (no commands executed)")
    print()

    commands = [
        "import os",
        "import time",
        "class AIWriter:",
        "    def __init__(self):",
        "        self.mood = 'focused'",
        "",
        "    def craft(self):",
        "        return 'syntax_is_clean'",
        "",
        "def simulate_run():",
        "    print('booting compiler...')",
        "    print('indexing files...')",
        "    print('rendering mock output...')",
        "",
        "simulate_run()",
        "print('terminalcafe: rendering complete')",
    ]

    for cmd in commands:
        fake_type(cmd + "\n", delay=0.03)
        time.sleep(0.05)

    print()
    print("Session idle. Awaiting exit signal...")
    print("Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass


def run_code_rain():
    clear_screen()
    print("TerminalCafe // Code Rain")
    print("displaying synthetic source stream")
    print("no runtime execution")
    for _ in range(40):
        print("    " + "print('lambda') " * 3)
        time.sleep(0.05)
    print("Press Ctrl+C to quit.")
    try:
        while True:
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass


def run_build_monitor():
    clear_screen()
    print("TerminalCafe // Build Monitor")
    print("build: running")
    print("[1/6] scanning modules")
    time.sleep(0.4)
    print("[2/6] validating types")
    time.sleep(0.4)
    print("[3/6] generating diff")
    time.sleep(0.4)
    print("[4/6] packaging assets")
    time.sleep(0.4)
    print("[5/6] linting output")
    time.sleep(0.4)
    print("[6/6] finalizing session")
    time.sleep(0.4)
    print("build status: mock success")
    print("Press Ctrl+C to quit.")
    try:
        while True:
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass


def menu_loop():
    selected_index = 0
    while True:
        print_menu(selected_index)
        key = get_key()

        if key in ("q", "Q", "ESC"):
            clear_screen()
            print("TerminalCafe: goodbye")
            return

        if key in ("UP", "w", "W"):
            selected_index = (selected_index - 1) % len(SCREEN_OPTIONS)
        elif key in ("DOWN", "s", "S"):
            selected_index = (selected_index + 1) % len(SCREEN_OPTIONS)
        elif key in ("\r", "\n", "ENTER"):
            choice = SCREEN_OPTIONS[selected_index]
            if choice == "AI Python Session":
                run_fake_ai_session()
            elif choice == "Code Rain":
                run_code_rain()
            elif choice == "Build Monitor":
                run_build_monitor()
            elif choice == "Exit":
                clear_screen()
                print("TerminalCafe: goodbye")
                return


if __name__ == "__main__":
    menu_loop()
