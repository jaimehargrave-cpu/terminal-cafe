# Download and run TerminalCafe

TerminalCafe is currently a source-code prototype. There are no packaged installers or official binary downloads yet.

## Requirements
- Python 3
- A terminal emulator
- No third-party Python packages

## Get the source
Download or clone the repository from GitHub:

```bash
git clone https://github.com/jaimehargrave-cpu/terminal-cafe.git
cd terminal-cafe
```

To try the current screensaver prototype on the development branch:

```bash
git checkout copilot/terminalcafe-scaffold
python3 terminalcafe.py
```

On Windows, run `python terminalcafe.py` from PowerShell or Command Prompt if `python3` is not available.

## Controls
- Up/Down or W/S: move through the menu
- Enter: start the selected scene
- Ctrl+C: return from an animation to the menu
- q: quit from the menu

## Availability notes
The project aims to run in terminal environments across macOS, Windows, and Linux, but packaged releases and platform-specific testing are not yet available. ANSI color and Unicode rendering vary by terminal. This is a terminal animation prototype, not yet a native OS screensaver installer.

Only download and run source you trust. The built-in scenes are intended as visual simulations and do not execute the displayed code or mock build steps.
