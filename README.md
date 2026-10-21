# axON - Blood Red Note Taking TUI

A terminal-based note-taking application with a **blood red on pitch black** theme, built with [Textual](https://textual.textualize.io/).

![Screenshot](screenshot.png)

## Features

- **Blood red on pitch black** color scheme - easy on the eyes in dark environments
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
nix run github:yourusername/axon

# Build locally
git clone https://github.com/yourusername/axon
cd axon
nix build .#axon
./result/bin/axon

# Enter development environment
nix develop
```

### Python (pip)

```bash
# From source
git clone https://github.com/yourusername/axon
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

## License

MIT License - see [LICENSE](LICENSE) for details.