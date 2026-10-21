# axON - Blood Red Note Taking TUI

Your thoughts. Your notes. Your terminal.

A terminal-based note-taking application with a **blood red on pitch black** theme, built with [Textual](https://textual.textualize.io/).


## Features

- **Blood red on pitch black** color scheme - easy on the eyes in dark environments(The real reason is, I like red)
- **Slim sidebar** (20 chars) for note list with scrollable notes
- **Full-screen editor** for note content with syntax highlighting ready
- **Markdown file storage** in `~/notes` - plain text, portable, version-controllable
- **Keyboard-driven interface** - no mouse needed
- **Auto-save prompts** - never lose your work

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `N` | Create new note |
| `S` | Save current note |
| `D` | Delete current note |
| `↑`/`↓` | Navigate note list |
| `Enter` | Open highlighted note |
| `ESC` | Cancel edit / Quit (from list) |
| `Q` | Quit application |

## Installation

### Nix (Recommended)

```bash
# Run directly from GitHub
nix run github:germanex3000dev/axON
```
```bash
# Build locally
git clone https://github.com/germanex3000dev/axON
cd axon
nix build .#axon
./result/bin/axon
```
You can also put the binary in your `PATH`
```bash
# Enter development environment
nix develop
```

### Python (pip)

```bash
# From source
git clone https://github.com/germanex3000dev/axon
cd axon
pip install -e .

# Run
axon
```

## Development

```bash
# Enter dev shell (includes python, textual, black, ruff, mypy)
nix develop

# Run from source
python -m axon

# Format code
black axon/

# Lint
ruff check axon/

# Type check
mypy axon/
```

## Project Structure

```
axon/
├── flake.nix          # Nix flake for build, run, dev shell
├── pyproject.toml     # Python package config
├── README.md          # This file
├── .gitignore         # Git ignore rules
├── axon/
│   ├── __init__.py    # Package init
│   ├── __main__.py    # Main application entry point
│   └── app.tcss       # Textual CSS theme (blood red on black)
```

## Notes Storage

Notes are stored as `.md` files in `~/notes/`:
- Each note is a separate markdown file
- Filenames are timestamp-based: `YYYYMMDD-HHMMSS-title.md`
- First line of content becomes the title (sanitized)
- Fully compatible with any markdown editor

## Theme Colors

| Element | Color | Hex |
|---------|-------|-----|
| Background | Pitch Black | `#000000` |
| Primary Text | Blood Red Bright | `#FF0000` |
| Borders/Dim | Blood Red Dim | `#4A0000` |
| Accent | Blood Red | `#8B0000` |
| Sidebar/Editor BG | Pitch Black | `#000000` |
| Highlights | Dark Gray | `#1A1A1A` |

## Requirements

- Python 3.10+
- Textual 0.50+
- Nix (for flake-based installation)

## Latest Changes

> This section tracks the evolution of axON — a running log of what landed and why.
> For the bigger picture, see [Roadmap](#roadmap).

### Latest(major) 21.10.2026, 14:30: Complete Nix flake environment

Added a full Nix flake with build, run, and development shell support:

- **`nix build .#axon`** — builds the package into `./result` with Python 3.14 and textual 8.2.8
- **`nix run .#axon`** — runs the app directly from the build output
- **`nix develop`** — drops into a dev shell with python3, textual, black, ruff, mypy, git
- Uses `hatchling` as the build backend (added to `nativeBuildInputs`)
- Fixed `pyproject.toml` with proper `[project.scripts]` entry point: `axon = "axon.__main__:main"`
- Added `main()` function to `__main__.py` for the console script
- Created `README.md` (required by hatchling) and `.gitignore`

### Latest(small) 21.10.2026, 12:15: Pure pitch black backgrounds

Refined the theme to use pitch black (`#000000`) everywhere with blood red only for borders and text:

- All panel backgrounds: Header, Footer, Sidebar, Editor, Buttons → `#000000`
- Borders only use blood red dim (`#4A0000`) and bright (`#FF0000`) on focus
- Buttons: transparent background with solid blood red borders
- Highlighted list item: left border indicator instead of full background
- Scrollbars: pitch black track with dim red thumb, bright on hover/focus
- Status bar: pitch black with dim red text and subtle top border

### Latest(major) 21.10.2026, 11:00: Slim sidebar layout

Restructured the UI to give the editor maximum screen real estate:

- Sidebar container (`#sidebar`) fixed at 20 characters width with right border
- Editor panel (`#editor-panel`) takes `1fr` (remaining space)
- Note list uses full sidebar width with tight padding (`0 1`)
- Short button labels: "New" / "Delete" to fit slim panel
- Sidebar title styled with centered blood red text and bottom border

### Latest(major) 20.10.2026, 18:00: Initial blood red theme + core functionality

First working version with the signature aesthetic and note operations:

- **Color palette**: Blood red (`#8B0000`/`#FF0000`/`#4A0000`) on pitch black (`#000000`)
- **Two-panel layout**: Horizontal split with ListView sidebar and TextArea editor
- **Note operations**: Create (N), Save (S), Delete (D), Open (Enter), Cancel/Quit (ESC/Q)
- **File storage**: Markdown files in `~/notes/` with timestamp-based naming
- **Auto-title extraction**: First line of content becomes filename (sanitized)
- **Keyboard bindings**: Full Textual binding system with footer hints
- **Visual feedback**: Hover states, focus borders, highlighted selection

## Roadmap

- [x] Basic TUI setup with textual
- [x] Display markdown files in a list
- [x] Navigate and select notes
- [x] Built-in Markdown editor
- [x] Save notes and handle unsaved changes
- [x] Complete Nix flake (build, run, dev shell)
- [x] Slim sidebar with editor-focused layout
- [x] Pure pitch black backgrounds with red borders
- [ ] Search notes by name and content
- [ ] Support configurable notes directories
- [ ] Add basic configuration options (theme, keybindings)
- [ ] Introduce task management and project organization
- [ ] Expand into an all-in-one terminal productivity tool

## License

MIT License - see [LICENSE](LICENSE) for details.
