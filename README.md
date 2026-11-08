# TerminalCafe

TerminalCafe is a terminal-first screensaver pack for macOS, Windows, and Linux. It brings a little motion and color to a developer's terminal with several selectable scenes.

## Screensaver scenes
- **AI Python Session** — simulated code typing; displayed text is never executed.
- **Code Rain** — a stream of synthetic source snippets.
- **Build Monitor** — a mock build pipeline animation.
- **Creative Tools** — a colorful, seamless 12-second loop with several independently moving tool-like shapes. Their orbital paths, orientations, trails, and highlights animate simultaneously.

Creative Tools is an original terminal-native kinetic animation, using layered motion and abstract ASCII forms rather than reproducing proprietary artwork.

## Run

Python 3 is required; no third-party packages are needed.

```bash
python3 terminalcafe.py
```

Use the arrow keys or W/S to navigate, then press Enter. In any scene, press **Ctrl+C** to return to the menu; press **q** from the menu to quit.

The scenes are visual simulations only. They do not execute the commands or build steps they display.
