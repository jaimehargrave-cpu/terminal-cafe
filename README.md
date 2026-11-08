# TerminalCafe

TerminalCafe is a Python terminal screensaver pack: a set of continuously animated, coding-inspired scenes for a terminal window.

## Scenes
- **AI Python Session** — fictional code is typed and animated; it is never executed.
- **Code Rain** — columns of synthetic characters stream continuously.
- **Build Monitor** — a fictional pipeline cycles forever; it does not run build tools.
- **Creative Tools** — a seamless, layered kinetic scene with five independently moving illustrated objects, different orbital speeds, trails, orbit paths, shifting orientation, twinkling backdrop, and moving highlights.

Creative Tools redraws the whole composition every frame so multiple movements happen simultaneously. Its animation uses a 16-second master loop; all motion returns to its starting phase together. The scene keeps running until you leave it.

## Run

Requires Python 3 and an interactive terminal. No third-party packages are needed.

```bash
python3 terminalcafe.py
```

On Windows, use `python terminalcafe.py` if `python3` is not available. See [download.md](download.md) for source download instructions and current availability.

## Controls
- **Up/Down** or **W/S**: select a scene
- **Enter**: start the selected scene
- **q**, **Esc**, or **Ctrl+C**: leave a scene; from the menu, quit

Scenes run continuously and do not stop on a timer. The terminal returns to its previous screen and cursor state on exit. True-color ANSI rendering depends on terminal support; a modern terminal is recommended.

## Project status
This is a terminal animation prototype, not yet a native OS screensaver or packaged installer. Linux distributions are not detected or guaranteed as tested targets; the program uses Python and standard terminal interfaces.

All displayed code, logs, and build steps are visual simulations only.
