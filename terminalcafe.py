#!/usr/bin/env python3
"""TerminalCafe: continuous, terminal-native screensaver scenes."""

import math
import os
import shutil
import sys
import time

SCENES = ["AI Python Session", "Code Rain", "Build Monitor", "Creative Tools", "Brew", "Exit"]
FPS = 18


def terminal_setup():
    """Enter a restorable interactive terminal mode; return a cleanup callback."""
    if os.name == "nt":
        import msvcrt  # noqa: F401
        sys.stdout.write("\x1b[?1049h\x1b[?25l")
        sys.stdout.flush()
        return lambda: (sys.stdout.write("\x1b[0m\x1b[?25h\x1b[?1049l"), sys.stdout.flush())

    import termios
    import tty
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    sys.stdout.write("\x1b[?1049h\x1b[?25l")
    sys.stdout.flush()

    def cleanup():
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write("\x1b[0m\x1b[?25h\x1b[?1049l")
        sys.stdout.flush()
    return cleanup


def poll_key():
    """Return a normalized key when available, without blocking animation."""
    if os.name == "nt":
        import msvcrt
        if not msvcrt.kbhit():
            return None
        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            return {"H": "UP", "P": "DOWN", "K": "LEFT", "M": "RIGHT"}.get(msvcrt.getwch(), "")
        return key

    import select
    fd = sys.stdin.fileno()
    if not select.select([fd], [], [], 0)[0]:
        return None
    key = sys.stdin.read(1)
    if key != "\x1b":
        return key
    if not select.select([fd], [], [], 0.015)[0]:
        return "ESC"
    tail = sys.stdin.read(1)
    if tail == "[" and select.select([fd], [], [], 0.015)[0]:
        tail += sys.stdin.read(1)
    return {"[A": "UP", "[B": "DOWN", "[C": "RIGHT", "[D": "LEFT"}.get(tail if tail.startswith("[") else "", "ESC")


def draw_text(canvas, colors, x, y, text, color):
    if 0 <= y < len(canvas):
        for offset, char in enumerate(text):
            px = x + offset
            if 0 <= px < len(canvas[y]):
                canvas[y][px] = char
                colors[(px, y)] = color


def new_canvas(width, height):
    return [[" " for _ in range(width)] for _ in range(height)], {}


def render(title, subtitle, canvas, colors, footer):
    output = ["\x1b[H\x1b[2J\x1b[1;38;2;235;238;250m", title, "\x1b[0m\n\x1b[38;2;145;157;180m", subtitle, "\x1b[0m\n"]
    active = None
    for y, row in enumerate(canvas):
        for x, char in enumerate(row):
            color = colors.get((x, y))
            if color != active:
                output.append("\x1b[0m" if color is None else f"\x1b[38;2;{color[0]};{color[1]};{color[2]}m")
                active = color
            output.append(char)
        output.extend(["\x1b[0m\n"])
        active = None
    output.extend(["\x1b[38;2;120;132;153m", footer, "\x1b[0m"])
    sys.stdout.write("".join(output))
    sys.stdout.flush()


def animate(draw_frame, fps=FPS):
    """Run a scene continuously until the user leaves it."""
    interval = 1.0 / fps
    frame, deadline = 0, time.monotonic()
    try:
        while True:
            if poll_key() in ("q", "Q", "ESC", "\x03"):
                return
            draw_frame(frame)
            frame += 1
            deadline += interval
            delay = deadline - time.monotonic()
            if delay > 0:
                time.sleep(delay)
            else:
                deadline = time.monotonic()
    except KeyboardInterrupt:
        return


def run_ai_session():
    code = ["from imagination import make", "", "class SmallIdea:", "    def __init__(self, color):", "        self.color = color", "        self.energy = 1.0", "", "    def become(self, shape):", "        return shape.with_light(self.color)", "", "while the_world_is_quiet:", "    idea = make(seed='curiosity')", "    sketch = idea.become('something_useful')", "    share(sketch)"]
    total = sum(len(line) + 1 for line in code)

    def draw(frame):
        width, rows = shutil.get_terminal_size((80, 24))
        height = max(6, rows - 3)
        canvas, colors = new_canvas(max(1, width), height)
        visible, used = int((frame % (FPS * 18)) / (FPS * 18) * total), 0
        for y, line in enumerate(code[:max(0, height - 2)], start=1):
            count = min(len(line), max(0, visible - used))
            draw_text(canvas, colors, 3, y, line[:count], (136, 218, 180))
            used += len(line) + 1
        draw_text(canvas, colors, 3, height - 1, "thinking  /  sketching  /  polishing", (137, 160, 194))
        render("TerminalCafe  /  AI PYTHON SESSION", "Fictional code animation; displayed text is never executed", canvas, colors, "Loops continuously  |  q / Esc / Ctrl+C: return to menu")
    animate(draw)


def run_code_rain():
    alphabet = "{}[]()<>/\\=+-_*#;:abcdef0123456789"
    palette = [(63, 206, 154), (47, 150, 133), (72, 119, 131), (104, 221, 175)]

    def draw(frame):
        width, rows = shutil.get_terminal_size((80, 24))
        height = max(6, rows - 3)
        canvas, colors = new_canvas(max(1, width), height)
        for col in range(0, width, 3):
            head = (frame * (1 + (col * 7) % 4) // 2 + col * 13) % (height + 8) - 4
            for tail in range(6):
                y = head - tail
                index = (col * 11 + frame * (tail + 1) + y * 5) % len(alphabet)
                color = palette[min(3, max(0, 3 - tail // 2))]
                draw_text(canvas, colors, col, y, alphabet[index], color)
        render("TerminalCafe  /  CODE RAIN", "Synthetic characters falling through a quiet terminal", canvas, colors, "Continuous animation  |  q / Esc / Ctrl+C: return to menu")
    animate(draw)


def run_build_monitor():
    stages = ["SCANNING", "PARSING", "LINKING", "OPTIMIZING", "PACKAGING", "READY"]

    def draw(frame):
        width, rows = shutil.get_terminal_size((80, 24))
        height = max(6, rows - 3)
        canvas, colors = new_canvas(max(1, width), height)
        cycle = frame % (FPS * 18)
        part = (cycle // (FPS * 3)) % len(stages)
        progress = (cycle % (FPS * 3)) / (FPS * 3)
        draw_text(canvas, colors, 3, 1, "WORKSHOP BUILD / SIMULATION", (120, 209, 250))
        draw_text(canvas, colors, 3, 3, f"stage  {stages[int(part)]}", (239, 195, 115))
        bar = min(42, max(12, width - 12))
        fill = int(progress * bar)
        draw_text(canvas, colors, 3, 5, "[" + "=" * fill + ">" + " " * max(0, bar - fill - 1) + "]", (116, 219, 167))
        draw_text(canvas, colors, 3, 6, f"{int(progress * 100):02d}%  /  cycles forever", (152, 165, 190))
        for i, line in enumerate(["assets: resolved", "layout: balanced", "colors: warmed", "render: smooth", "result: imaginary"]):
            if cycle // (FPS * 2) >= i:
                draw_text(canvas, colors, 3, 9 + i, f"[{i + 1:02d}]  {line}", (117, 184, 155))
        render("TerminalCafe  /  BUILD MONITOR", "Fictional pipeline; no build tools are run", canvas, colors, "Continuous animation  |  q / Esc / Ctrl+C: return to menu")
    animate(draw)


def run_creative_tools():
    """Layered, continuously looping motion with independently moving forms."""
    loop = FPS * 16
    tools = [("PENCIL", 0.30, 0.24, 1, .02, (255, 129, 158)), ("BRUSH", .41, .34, -1, .19, (255, 195, 104)), ("CHIP", .22, .41, 2, .39, (136, 231, 173)), ("WINDOW", .48, .27, -2, .59, (94, 210, 246)), ("PALETTE", .36, .44, 3, .79, (190, 151, 255))]
    art = {"PENCIL": ["  /| ", " / | ", "/__| "], "BRUSH": ["  |  ", " /|\\ ", " ||| "], "CHIP": ["+---+", "| * |", "+---+"], "WINDOW": ["+---+", "| _ |", "|___|"], "PALETTE": [" .-. ", "( o )", " `-' "]}

    def draw(frame):
        width, rows = shutil.get_terminal_size((80, 24))
        width, height = max(24, width), max(8, rows - 3)
        canvas, colors = new_canvas(width, height)
        cx, cy = width // 2, height // 2
        phase = 2 * math.pi * (frame % loop) / loop
        for i in range(40):
            x, y = (i * 37 + 11) % width, (i * 19 + 7) % height
            if (frame // (5 + i % 3 * 3) + i) % 7 == 0:
                draw_text(canvas, colors, x, y, ".", (48, 63, 87))
        for level, (rx, ry) in enumerate(((.23, .25), (.36, .37), (.48, .45))):
            for point in range(160):
                a = 2 * math.pi * point / 160 + phase * (2 if level == 1 else -1)
                x, y = round(cx + math.cos(a) * width * rx), round(cy + math.sin(a) * height * ry)
                draw_text(canvas, colors, x, y, ".", (54, 68, 91))
        for i, (name, rx, ry, speed, offset, color) in enumerate(tools):
            angle = phase * speed + offset * 2 * math.pi
            x = round(cx + math.cos(angle) * width * rx)
            y = round(cy + math.sin(angle) * height * ry)
            for tail in range(8, 0, -1):
                ta = angle - tail * .04 * (1 if speed > 0 else -1)
                tx, ty = round(cx + math.cos(ta) * width * rx), round(cy + math.sin(ta) * height * ry)
                draw_text(canvas, colors, tx, ty, "." if tail > 4 else "+", tuple(int(c * (9 - tail) / 9) for c in color))
            for dy, line in enumerate(art[name]):
                draw_text(canvas, colors, x - len(line) // 2, y + dy - 1, line, color)
            pulse = phase * (speed + 1) + i
            draw_text(canvas, colors, x + round(math.cos(pulse) * 3), y - 3 + round(math.sin(pulse)), "*", tuple(min(255, c + 35) for c in color))
        motif = ["*", "◇", "+", "✧"][(frame // (loop // 4)) % 4]
        draw_text(canvas, colors, cx, cy, motif, (205, 210, 255))
        render("TerminalCafe  /  CREATIVE TOOLS", "A living workshop: orbiting forms, shifting light, and layered motion", canvas, colors, "Infinite loop  |  q / Esc / Ctrl+C: return to menu")
    animate(draw)


def run_brew():
    """Continuously pour hot coffee into a mug, then let it empty and repeat."""
    cycle_seconds, pour_seconds = 18.0, 7.0
    coffee = (154, 91, 48)
    dark_coffee = (104, 57, 34)
    cream = (220, 174, 111)
    porcelain = (198, 211, 226)

    def draw(frame):
        width, rows = shutil.get_terminal_size((80, 24))
        width, height = max(32, width), max(10, rows - 3)
        canvas, colors = new_canvas(width, height)
        cx = width // 2
        seconds = (frame / FPS) % cycle_seconds
        if seconds < pour_seconds:
            fill = min(1.0, seconds / pour_seconds)
            pouring = True
        elif seconds < pour_seconds + 3.0:
            fill, pouring = 1.0, False
        else:
            fill = max(0.0, 1.0 - (seconds - pour_seconds - 3.0) / (cycle_seconds - pour_seconds - 3.0))
            pouring = False

        mug_height = min(9, max(5, height // 2))
        top = max(6, min(height - mug_height - 1, height // 2 - mug_height // 2 + 2))
        left = cx - 10
        right = cx + 9
        bottom = min(height - 1, top + mug_height)

        # A small coffee pot and its spout establish the source of the stream.
        pot_x = cx - 12
        draw_text(canvas, colors, pot_x, 1, " .--------.", cream)
        draw_text(canvas, colors, pot_x, 2, "(  BREW   )___", cream)
        draw_text(canvas, colors, pot_x, 3, " `--------'   \\", cream)
        pour_x = cx + 3
        if pouring:
            stream_top = 4
            for y in range(stream_top, top):
                phase = (frame + y * 3) % 12
                char = "o" if phase < 2 else ("." if phase < 5 else "|")
                draw_text(canvas, colors, pour_x, y, char, coffee if char != "o" else cream)
            for dx, char in [(-2, "."), (-1, "\\"), (0, "~"), (1, "/"), (2, ".")]:
                draw_text(canvas, colors, pour_x + dx, top, char, cream if dx == 0 else coffee)

        # Mug rim, body, and a thin curved handle.
        draw_text(canvas, colors, left, top, " .-----------------.", porcelain)
        draw_text(canvas, colors, left, top + 1, "|                   |", porcelain)
        for y in range(top + 2, bottom):
            draw_text(canvas, colors, left, y, "|                   |", porcelain)
        draw_text(canvas, colors, right + 1, top + 2, "\\", porcelain)
        draw_text(canvas, colors, right + 2, top + 3, ")", porcelain)
        draw_text(canvas, colors, right + 2, top + 4, ")", porcelain)
        draw_text(canvas, colors, right + 1, top + 5, "/", porcelain)
        draw_text(canvas, colors, left + 1, bottom, " '-----------------'", porcelain)

        inner_top, inner_bottom = top + 1, bottom - 1
        inside_height = max(1, inner_bottom - inner_top)
        liquid_rows = round(fill * inside_height)
        surface_y = inner_bottom - liquid_rows + 1
        for y in range(inner_bottom, inner_bottom - liquid_rows, -1):
            for x in range(left + 1, right):
                char = "~" if y == surface_y else ("#" if (x + y) % 4 else "=")
                draw_text(canvas, colors, x, y, char, cream if y == surface_y else (coffee if char == "#" else dark_coffee))
        if liquid_rows:
            for x in range(left + 2, right - 1):
                wave = "~" if (x + frame // 3) % 5 else "-"
                draw_text(canvas, colors, x, surface_y, wave, cream)

        # Steam curls drift independently above a hot, filled mug.
        if fill > .55 and not pouring:
            steam = ("  ~       ~  ", " ~ ~     ~ ~ ", "~   ~   ~   ~")
            for strand, line in enumerate(steam):
                shift = round(math.sin(frame / 8 + strand) * 2)
                draw_text(canvas, colors, cx - 7 + shift, top - 4 + strand, line, (160, 174, 190))
        draw_text(canvas, colors, max(0, cx - 8), min(height - 1, bottom + 2), "B R E W   /   F R E S H   C O F F E E", (190, 157, 121))
        render("TerminalCafe  /  BREW", "A fresh cup, poured slowly in a continuous loop", canvas, colors, "Coffee pours, settles, and refills  |  q / Esc / Ctrl+C: return to menu")

    animate(draw)


def menu():
    selected = 0
    while True:
        width, rows = shutil.get_terminal_size((80, 24))
        canvas, colors = new_canvas(max(width, 32), max(rows - 3, 8))
        draw_text(canvas, colors, 3, 1, "A terminal screensaver pack for curious minds", (144, 164, 195))
        for i, scene in enumerate(SCENES):
            draw_text(canvas, colors, 4, 4 + i * 2, ("> " if i == selected else "  ") + scene,
                      (255, 197, 112) if i == selected else (205, 213, 227))
        draw_text(canvas, colors, 4, min(len(canvas) - 1, 4 + len(SCENES) * 2), "W/S or arrows: select   Enter: start   q: quit", (130, 146, 170))
        render("TerminalCafe", "Choose a scene", canvas, colors, "Scenes loop until you leave them")
        key = poll_key()
        if key in ("q", "Q", "ESC", "\x03"):
            return
        if key in ("UP", "w", "W"):
            selected = (selected - 1) % len(SCENES)
        elif key in ("DOWN", "s", "S"):
            selected = (selected + 1) % len(SCENES)
        elif key in ("\r", "\n", "ENTER"):
            action = {"AI Python Session": run_ai_session, "Code Rain": run_code_rain,
                      "Build Monitor": run_build_monitor, "Creative Tools": run_creative_tools,
                      "Brew": run_brew}.get(SCENES[selected])
            if action:
                action()
            elif SCENES[selected] == "Exit":
                return
        time.sleep(0.04)


def main():
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("TerminalCafe needs an interactive terminal.", file=sys.stderr)
        return 2
    cleanup = terminal_setup()
    try:
        menu()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
