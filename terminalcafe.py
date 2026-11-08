#!/usr/bin/env python3
"""TerminalCafe: a collection of terminal-native screensaver scenes."""

import math
import os
import shutil
import sys
import time

SCREEN_OPTIONS = [
    "AI Python Session",
    "Code Rain",
    "Build Monitor",
    "Creative Tools",
    "Exit",
]


def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def print_menu(selected_index):
    clear_screen()
    print("TerminalCafe")
    print("Choose a screensaver\n")
    for i, option in enumerate(SCREEN_OPTIONS):
        print(f"{'>' if i == selected_index else ' '} {option}")
    print("\n↑/↓ move   Enter select   q quit")


def get_key():
    if os.name == "nt":
        import msvcrt
        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            return {"H": "UP", "P": "DOWN"}.get(msvcrt.getwch(), "")
        return key

    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            seq = sys.stdin.read(2)
            return {"[A": "UP", "[B": "DOWN"}.get(seq, "ESC")
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def fake_type(text, delay=0.03, stream=sys.stdout):
    for ch in text:
        stream.write(ch)
        stream.flush()
        time.sleep(delay)


def wait_for_interrupt():
    print("\nPress Ctrl+C to return to the menu.")
    try:
        while True:
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass


def run_fake_ai_session():
    clear_screen()
    print("TerminalCafe // AI Python Session")
    print("AI assistant typing... (no commands executed)\n")
    lines = [
        "import os", "import time", "class AIWriter:",
        "    def __init__(self):", "        self.mood = 'focused'", "",
        "    def craft(self):", "        return 'syntax_is_clean'", "",
        "def simulate_run():", "    print('booting compiler...')",
        "    print('indexing files...')", "    print('rendering mock output...')", "",
        "simulate_run()", "print('terminalcafe: rendering complete')",
    ]
    for line in lines:
        fake_type(line + "\n")
        time.sleep(0.05)
    print("\nSession idle.")
    wait_for_interrupt()


def run_code_rain():
    clear_screen()
    print("TerminalCafe // Code Rain")
    print("synthetic source stream; nothing is executed\n")
    for _ in range(40):
        print("    " + "print('lambda') " * 3)
        time.sleep(0.05)
    wait_for_interrupt()


def run_build_monitor():
    clear_screen()
    print("TerminalCafe // Build Monitor")
    print("build: running (simulation only)")
    stages = ["scanning modules", "validating types", "generating diff",
              "packaging assets", "linting output", "finalizing session"]
    for index, stage in enumerate(stages, start=1):
        print(f"[{index}/6] {stage}")
        time.sleep(0.4)
    print("build status: mock success")
    wait_for_interrupt()


def run_creative_tools():
    """Animate several independently moving creative-tool shapes at once."""
    fps = 24
    loop_frames = fps * 12
    # Each tuple is a different object, orbit, phase, speed, and color. Integer
    # cycle counts make the entire composition return to its start together.
    objects = [
        ("PENCIL", 0.30, 0.18, 1, 0.00, (255, 130, 155)),
        ("BRUSH", 0.43, 0.30, -1, 0.20, (255, 198, 100)),
        ("CHIP", 0.22, 0.36, 2, 0.40, (145, 235, 170)),
        ("WINDOW", 0.48, 0.24, -2, 0.60, (100, 220, 245)),
        ("CURSOR", 0.36, 0.42, 3, 0.80, (195, 155, 255)),
    ]
    # The small silhouettes change orientation as they travel, so they read as
    # objects in motion rather than labels sliding around a static diagram.
    silhouettes = {
        "PENCIL": ["--/", "/--", "\\--", "--\\"],
        "BRUSH": ["==]", "]==", "[==", "==["],
        "CHIP": ["[+]", "[x]", "[*]", "[+]"],
        "WINDOW": ["[ ]", "[=]", "[+]", "[ ]"],
        "CURSOR": ["<>", "^v", "{}", "v^"],
    }
    frame = 0

    try:
        while True:
            columns, rows = shutil.get_terminal_size((80, 24))
            width = max(24, columns - 2)
            height = max(8, rows - 5)
            cx, cy = (width - 1) / 2, (height - 1) / 2
            canvas = [[" " for _ in range(width)] for _ in range(height)]
            ink = {}
            phase = 2 * math.pi * (frame % loop_frames) / loop_frames

            # Multiple nested orbit paths establish depth and a composed frame.
            for level, (rx, ry) in enumerate(((0.23, 0.25), (0.36, 0.37), (0.49, 0.46))):
                for point in range(240):
                    a = 2 * math.pi * point / 240 + phase * (1 if level == 1 else -1)
                    x, y = round(cx + math.cos(a) * width * rx), round(cy + math.sin(a) * height * ry)
                    if 0 <= x < width and 0 <= y < height and canvas[y][x] == " ":
                        canvas[y][x] = "." if level == 0 else ":"
                        ink[(x, y)] = (43, 56, 76)

            # All objects are recalculated and drawn on every frame: their
            # positions, orientations, trails, and highlights move together.
            for index, (name, rx, ry, cycles, offset, rgb) in enumerate(objects):
                a = phase * cycles + 2 * math.pi * offset
                x = cx + math.cos(a) * width * rx
                y = cy + math.sin(a) * height * ry
                ix, iy = round(x), round(y)
                variant = int((frame * abs(cycles) / fps) % 4)
                shape = silhouettes[name][variant]

                # Tapered trails follow each object's own trajectory.
                for tail in range(8, 0, -1):
                    ta = a - tail * 0.045 * (1 if cycles > 0 else -1)
                    tx = round(cx + math.cos(ta) * width * rx)
                    ty = round(cy + math.sin(ta) * height * ry)
                    if 0 <= tx < width and 0 <= ty < height:
                        canvas[ty][tx] = "." if tail > 4 else "+"
                        factor = (9 - tail) / 9
                        ink[(tx, ty)] = tuple(round(c * factor) for c in rgb)

                for dx, char in enumerate(shape):
                    px = ix + dx - len(shape) // 2
                    if 0 <= px < width and 0 <= iy < height:
                        canvas[iy][px] = char
                        ink[(px, iy)] = rgb
                # A traveling glint and breathing halo add a second motion layer.
                pulse = 0.5 + 0.5 * math.sin(phase * 2 + index * 1.7)
                hx, hy = ix, iy - 1 - int(pulse * 2)
                if 0 <= hx < width and 0 <= hy < height:
                    canvas[hy][hx] = "*" if pulse > 0.72 else "."
                    ink[(hx, hy)] = tuple(min(255, int(c + 35 + pulse * 25)) for c in rgb)

            # Center glow breathes independently while all five objects orbit.
            core = [" ", ".", "+", "*", "+", "."]
            core_char = core[(frame // 8) % len(core)]
            canvas[round(cy)][round(cx)] = core_char
            ink[(round(cx), round(cy))] = (235, 230, 255)

            output = ["\033[2J\033[H", "\033[1mTerminalCafe  /  CREATIVE TOOLS\033[0m\n",
                      "Layered motion • orbiting tools • seamless loop  |  Ctrl+C: menu\n\n"]
            for y, line in enumerate(canvas):
                for x, char in enumerate(line):
                    rgb = ink.get((x, y))
                    output.append(char if rgb is None else
                                  f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{char}\033[0m")
                output.append("\n")
            sys.stdout.write("".join(output))
            sys.stdout.flush()
            frame = (frame + 1) % loop_frames
            time.sleep(1 / fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[0m\n")
        sys.stdout.flush()


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
            elif choice == "Creative Tools":
                run_creative_tools()
            elif choice == "Exit":
                clear_screen()
                print("TerminalCafe: goodbye")
                return


if __name__ == "__main__":
    menu_loop()
