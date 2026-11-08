#!/usr/bin/env python3
"""TerminalCafe: continuous, terminal-native screensaver scenes."""

import math
import os
import shutil
import sys
import time

SCENES = ["AI Python Session", "Code Rain", "Build Monitor", "Creative Tools", "Exit"]
FPS = 18
FRAME_TIME = 1.0 / FPS


def terminal_setup():
    """Enter a restorable interactive terminal mode; return a cleanup callback."""
    if os.name == "nt":
        import msvcrt  # noqa: F401

        sys.stdout.write("\x1b[?1049h\x1b[?25l")
        sys.stdout.flush()

        def cleanup():
            sys.stdout.write("\x1b[0m\x1b[?25h\x1b[?1049l")
            sys.stdout.flush()

        return cleanup

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
    """Return one normalized key if available, without blocking the animation."""
    if os.name == "nt":
        import msvcrt

        if not msvcrt.kbhit():
            return None
        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            return {"H": "UP", "P": "DOWN", "K": "LEFT", "M": "RIGHT"}.get(
                msvcrt.getwch(), ""
            )
        return key

    import select

    fd = sys.stdin.fileno()
    ready, _, _ = select.select([fd], [], [], 0)
    if not ready:
        return None
    key = sys.stdin.read(1)
    if key != "\x1b":
        return key

    # Arrow keys arrive as short escape sequences. Wait only a few milliseconds
    # for the tail so an isolated Escape remains responsive.
    ready, _, _ = select.select([fd], [], [], 0.015)
    if not ready:
        return "ESC"
    tail = sys.stdin.read(1)
    if tail == "[":
        ready, _, _ = select.select([fd], [], [], 0.015)
        if ready:
            tail += sys.stdin.read(1)
    return {"[A": "UP", "[B": "DOWN", "[C": "RIGHT", "[D": "LEFT"}.get(
        tail if tail.startswith("[") else "", "ESC"
    )


def rgb(color):
    return f"\x1b[38;2;{color[0]};{color[1]};{color[2]}m"


def draw_text(canvas, colors, x, y, text, color):
    if not 0 <= y < len(canvas):
        return
    for offset, char in enumerate(text):
        px = x + offset
        if 0 <= px < len(canvas[y]):
            canvas[y][px] = char
            colors[(px, y)] = color


def render(title, subtitle, canvas, colors, footer):
    """Render a complete frame in-place to avoid scrolling and screen flicker."""
    output = ["\x1b[H\x1b[2J", "\x1b[1;38;2;235;238;250m", title, "\x1b[0m\n"]
    output.extend(["\x1b[38;2;145;157;180m", subtitle, "\x1b[0m\n"])
    for y, row in enumerate(canvas):
        active_color = None
        for x, char in enumerate(row):
            color = colors.get((x, y))
            if color != active_color:
                output.append("\x1b[0m" if color is None else rgb(color))
                active_color = color
            output.append(char)
        output.extend(["\x1b[0m\n"])
    output.extend(["\x1b[38;2;120;132;153m", footer, "\x1b[0m"])
    sys.stdout.write("".join(output))
    sys.stdout.flush()


def new_canvas(width, height):
    return [[" " for _ in range(width)] for _ in range(height)], {}


def animate(draw_frame, fps=FPS):
    """Run a scene until q/Escape/Ctrl+C; use deadline pacing to limit CPU use."""
    interval = 1.0 / fps
    frame = 0
    deadline = time.monotonic()
    try:
        while True:
            key = poll_key()
            if key in ("q", "Q", "ESC", "\x03"):
                return
            draw_frame(frame)
            frame += 1
            deadline += interval
            delay = deadline - time.monotonic()
            if delay > 0:
                time.sleep(delay)
            else:
                # Avoid a burst of catch-up renders if the terminal is slow.
                deadline = time.monotonic()
    except KeyboardInterrupt:
        return


def run_ai_session():
    code = [
        "from imagination import make",
        "",
        "class SmallIdea:",
        "    def __init__(self, color):",
        "        self.color = color",
        "        self.energy = 1.0",
        "",
        "    def become(self, shape):",
        "        return shape.with_light(self.color)",
        "",
        "while the_world_is_quiet:",
        "    idea = make(seed='curiosity')",
        "    sketch = idea.become('something_useful')",
        "    share(sketch)",
    ]

    def draw(frame):
        width, rows = shutil.get_terminal_size((80, 24))
        height = max(6, rows - 3)
        canvas, colors = new_canvas(max(1, width), height)
        cycle = frame % (FPS * 18)
        visible_chars = int((cycle / (FPS * 18)) * (sum(map(len, code)) + len(code) * 3))
        used = 0
        y = 1
        for line in code:
            count = min(len(line), max(0, visible_chars - used))
            draw_text(canvas, colors, 3, y, line[:count], (136, 218, 180))
            used += len(line) + 3
            y += 1
            if y >= height - 2:
                break
        cursor_y = min(height - 2, 1 + sum(1 for line in code if visible_chars >= sum(map(len, code[:code.index(line) + 1]))))
        cursor_x = min(width - 1, 3 + (frame // 2) % max(1, width - 8))
        if 0 <= cursor_y < height:
            draw_text(canvas, colors, cursor_x, cursor_y, "▌", (255, 202, 112))
        draw_text(canvas, colors, 3, height - 1, "● thinking  ·  ● sketching  ·  ● polishing", (137, 160, 194))
        render("TerminalCafe  /  AI PYTHON SESSION", "A quiet, fictional coding scene — displayed text is never executed", canvas, colors,
               "Loops continuously  |  q / Esc / Ctrl+C: return to menu")

    animate(draw)


def run_code_rain():
    alphabet = "{}[]()<>/\\=+-_*#;:abcdef0123456789"
    palette = [(63, 206, 154), (47, 150, 133), (72, 119, 131), (104, 221, 175)]

    def draw(frame):
        width, rows = shutil.get_terminal_size((80, 24))
        height = max(6, rows - 3)
        canvas, colors = new_canvas(max(1, width), height)
        for col in range(0, width, 3):
            speed = 1 + ((col * 7) % 4)
            head = (frame * speed // 2 + col * 13) % (height + 8) - 4
            for tail in range(6):
                y = head - tail
                if 0 <= y < height:
                    char_index = (col * 11 + frame * (tail + 1) + y * 5) % len(alphabet)
                    color = palette[min(3, max(0, 3 - tail // 2))]
                    draw_text(canvas, colors, col, y, alphabet[char_index], color)
        render("TerminalCafe  /  CODE RAIN", "Synthetic characters falling through a quiet terminal", canvas, colors,
               "Continuous animation  |  q / Esc / Ctrl+C: return to menu")

    animate(draw)


def run_build_monitor():
    stages = ["SCANNING", "PARSING", "LINKING", "OPTIMIZING", "PACKAGING", "READY"]

    def draw(frame):
        width, rows = shutil.get_terminal_size((80, 24))
        height = max(6, rows - 3)
        canvas, colors = new_canvas(max(1, width), height)
        cycle = frame % (FPS * 18)
        stage_length = FPS * 3
        stage_index = (cycle // stage_length) % len(stages)
        progress = (cycle % stage_length) / stage_length
        draw_text(canvas, colors, 3, 1, "WORKSHOP BUILD  /  SIMULATION", (120, 209, 250))
        draw_text(canvas, colors, 3, 3, f"stage     {stages[int(stage_index)]}", (239, 195, 115))
        bar_width = min(42, max(12, width - 12))
        fill = int(progress * bar_width)
        draw_text(canvas, colors, 3, 5, "[" + "=" * fill + ">" + " " * max(0, bar_width - fill - 1) + "]", (116, 219, 167))
        draw_text(canvas, colors, 3, 6, f"{int(progress * 100):02d}%   /   cycles forever", (152, 165, 190))
        log_lines = ["assets: resolved", "layout: balanced", "colors: warmed", "render: smooth", "result: purely imaginary"]
        visible = min(len(log_lines), 1 + cycle // (FPS * 2))
        for i, line in enumerate(log_lines[:visible]):
            draw_text(canvas, colors, 3, 9 + i, f"[{i + 1:02d}]  {line}", (117, 184, 155))
        render("TerminalCafe  /  BUILD MONITOR", "A looping fictional pipeline; no build tools are run", canvas, colors,
               "Continuous animation  |  q / Esc / Ctrl+C: return to menu")

    animate(draw)


def rotate_sprite(sprite, turns):
    result = [list(row) for row in sprite]
    for _ in range(turns % 4):
        result = [list(row) for row in zip(*result[::-1])]
    return ["".join(row) for row in result]


def draw_sprite(canvas, colors, cx, cy, sprite, color):
    top = cy - len(sprite) // 2
    for dy, row in enumerate(sprite):
        left = cx - len(row) // 2
        for dx, char in enumerate(row):
            if char != " ":
                draw_text(canvas, colors, left + dx, top + dy, char, color)


def run_creative_tools():
    """A continuously looping, multi-object animated creative-workshop scene."""
    # A 16-second master loop. All object, orbit, glint, and pulse frequencies
    # are integer multiples of the master phase, so the complete composition
    # returns to the same frame at the loop boundary.
    loop_frames = FPS * 16
    tools = [
        ("PENCIL", ["  /| ", " / | ", "/__| ", "   v "], 0.30, 0.24, 1, 0.02, (255, 129, 158)),
        ("BRUSH", ["  |  ", "  |  ", " /|\\ ", " ||| "], 0.41, 0.34, -1, 0.19, (255, 195, 104)),
        ("CHIP", ["+---+", "| * |", "+---+", " | | "], 0.22, 0.41, 2, 0.39, (136, 231, 173)),
        ("WINDOW", ["+---+", "| _ |", "|___|", "     "], 0.48, 0.27, -2, 0.59, (94, 210, 246)),
        ("PALETTE", [" .-. ", "( o )", " `-' ", "     "], 0.36, 0.44, 3, 0.79, (190, 151, 255)),
    ]
    stars = [(i * 37 + 11, i * 19 + 7, i % 3) for i in range(42)]

    def draw(frame):
        width, rows = shutil.get_terminal_size((80, 24))
        width = max(24, width)
        height = max(8, rows - 3)
        canvas, colors = new_canvas(width, height)
        cx, cy = width // 2, height // 2
        phase = 2 * math.pi * (frame % loop_frames) / loop_frames

        # Quiet, twinkling backdrop gives the moving objects visual depth.
        for sx, sy, variant in stars:
            x, y = sx % width, sy % height
            if (frame // (5 + variant * 3) + sx) % 7 == 0:
                draw_text(canvas, colors, x, y, "." if variant else "·", (48, 63, 87))

        # Three moving elliptical paths form a layered kinetic composition.
        for level, (rx, ry, direction) in enumerate(((0.23, 0.25, 1), (0.36, 0.37, -1), (0.48, 0.45, 1))):
            for point in range(180):
                a = 2 * math.pi * point / 180 + direction * phase * (1 if level != 1 else 2)
                x = round(cx + math.cos(a) * width * rx)
                y = round(cy + math.sin(a) * height * ry)
                if 0 <= x < width and 0 <= y < height:
                    shimmer = (point + frame // 3 + level * 4) % 9
                    draw_text(canvas, colors, x, y, "." if shimmer < 2 else "·", (54, 68, 91))

        # Every tool is independently animated and drawn in depth order. Its
        # path, orientation, eight-point trail, and glint all update per frame.
        moving = []
        for index, (name, art, rx, ry, cycles, offset, color) in enumerate(tools):
            angle = phase * cycles + 2 * math.pi * offset
            wobble = math.sin(phase * (2 if index % 2 == 0 else 3) + index) * 0.025
            x = cx + math.cos(angle) * width * (rx + wobble)
            y = cy + math.sin(angle + wobble) * height * ry
            depth = math.sin(angle)
            moving.append((depth, index, name, art, x, y, angle, cycles, color))

        for _, index, name, art, x, y, angle, cycles, color in sorted(moving):
            ix, iy = round(x), round(y)
            orientation = int((angle / (2 * math.pi) * 4) % 4)
            sprite = rotate_sprite(art, orientation)
            for tail in range(9, 0, -1):
                ta = angle - tail * 0.035 * (1 if cycles > 0 else -1)
                tx = round(cx + math.cos(ta) * width * tools[index][2])
                ty = round(cy + math.sin(ta) * height * tools[index][3])
                if 0 <= tx < width and 0 <= ty < height:
                    canvas[ty][tx] = "." if tail > 5 else "+"
                    fade = (10 - tail) / 10
                    colors[(tx, ty)] = tuple(int(component * fade) for component in color)

            draw_sprite(canvas, colors, ix, iy, sprite, color)
            # Moving glints travel around each form rather than remaining fixed.
            glint_angle = phase * (cycles + 1) + index * 1.3
            gx = ix + round(math.cos(glint_angle) * 2)
            gy = iy + round(math.sin(glint_angle) * 1.5) - 3
            if 0 <= gx < width and 0 <= gy < height:
                draw_text(canvas, colors, gx, gy, "*", tuple(min(255, c + 35) for c in color))

        # A luminous central maker's mark breathes and changes shape in sync.
        pulse = 0.5 + 0.5 * math.sin(phase * 2)
        motif = ["✦", "◇", "✧", "◈", "✧", "◇"][(frame // (loop_frames // 6)) % 6]
        mark_color = (int(164 + pulse * 80), int(166 + pulse * 70), 255)
        draw_text(canvas, colors, cx, cy, motif, mark_color)
        if width > 50 and height > 12:
            label = "MAKE  /  PLAY  /  REPEAT"
            draw_text(canvas, colors, cx - len(label) // 2, cy + 3, label, (118, 132, 160))

        render("TerminalCafe  /  CREATIVE TOOLS", "A living workshop: orbiting forms, shifting light, and layered motion",
               canvas, colors, "Infinite seamless loop  |  q / Esc / Ctrl+C: return to menu")

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
        draw_text(canvas, colors, 4, min(len(canvas) - 1, 4 + len(SCENES) * 2),
                  "W/S or arrows: select   Enter: start   q: quit", (130, 146, 170))
        render("TerminalCafe", "Choose a scene", canvas, colors, "Scenes loop until you leave them")

        key = poll_key()
        if key in ("q", "Q", "ESC", "\x03"):
            return
        if key in ("UP", "w", "W"):
            selected = (selected - 1) % len(SCENES)
        elif key in ("DOWN", "s", "S"):
            selected = (selected + 1) % len(SCENES)
        elif key in ("\r", "\n", "ENTER"):
            scene = SCENES[selected]
            if scene == "AI Python Session":
                run_ai_session()
            elif scene == "Code Rain":
                run_code_rain()
            elif scene == "Build Monitor":
                run_build_monitor()
            elif scene == "Creative Tools":
                run_creative_tools()
            elif scene == "Exit":
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
