# TerminalCafe

TerminalCafe is a Python terminal screensaver pack: a set of continuously animated, coding-inspired scenes for a terminal window.

## Scenes
- **AI Python Session** — fictional code is typed and animated; it is never executed.
- **Code Rain** — columns of synthetic characters stream continuously.
- **Build Monitor** — a fictional pipeline cycles forever; it does not run build tools.
- **Creative Tools** — a layered kinetic scene with independently moving illustrated objects, trails, orbit paths, shifting orientation, twinkling backdrop, and highlights.
- **Brew** — hot coffee pours from a small pot into an ASCII mug, rises to a full cup, settles with steam, then drains and loops.

All scenes animate continuously until you leave them. Requires Python 3 and an interactive terminal; no third-party packages are needed.

## Run

```bash
python3 terminalcafe.py
```

On Windows, use `python terminalcafe.py` if `python3` is not available. See [download.md](download.md) for source download instructions and current availability.

## Controls
- **Up/Down** or **W/S**: select a scene
- **Enter**: start the selected scene
- **q**, **Esc**, or **Ctrl+C**: leave a scene; from the menu, quit

The terminal returns to its previous screen and cursor state on exit. True-color ANSI rendering depends on terminal support; a modern terminal is recommended.

## Project status
This is a terminal animation prototype, not yet a native OS screensaver or packaged installer. All displayed code, logs, and build steps are visual simulations only.
