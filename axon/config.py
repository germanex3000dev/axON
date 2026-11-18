"""AxON configuration logic, includes user-defined colors, and a bit of the layout."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from platformdirs import user_config_path
from textual.color import Color, ColorParseError

try:
    import tomllib  # only for py 3.11 and above
except ModuleNotFoundError:
    import tomli as tomllib

DEFAULT_COLORS: dict[str, str] = {
    "background": "#000000",
    "text": "#FF0000",
    "accent": "#8B0000",
    "dim": "#4A0000",
    "highlight": "#1A1A1A",
    "gray": "#333333",
}

DEFAULT_SIDEBAR_WIDTH = 20
MIN_SIDEBAR_WIDTH = 8
MAX_SIDEBAR_WIDTH = 60

# The config key is a TCSS variable name in app.tcss
# The prefix "ax-" is needed here, since Textual's built-in theme already claims
# bare names like "$background", "$text", and "$accent", and these theme values
# take precedence over the defaults of the application, which would just disable the config, silently...

_COLOR_TO_TCSS: dict[str, str] = {
    "background": "ax-background",
    "text": "ax-text",
    "accent": "ax-accent",
    "dim": "ax-dim",
    "highlight": "ax-highlight",
    "gray": "ax-gray",
}


def config_path() -> Path:
    """Here we resolve the config file locations, since $AXON_CONFIG overrides."""
    env_path = os.environ.get("AXON_CONFIG")
    if env_path:
        return Path(env_path).expanduser()
    return user_config_path("axon") / "config.toml"


@dataclass(frozen=True)
class Config:
    """The configuration is validated, with the defaults of course filled in."""

    colors: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_COLORS))
    sidebar_width: int = DEFAULT_SIDEBAR_WIDTH
    warnings: tuple[str, ...] = ()

    def css_variables(self) -> dict[str, str]:
        """The map configuration values to the TCSS variables that are used by app.tcss."""
        variables = {
            _COLOR_TO_TCSS[key]: value for key, value in self.colors.items()
        }
        variables["ax-sidebar-width"] = str(self.sidebar_width)
        return variables


def _validate_color(key: str, value: object, warnings: list[str]) -> str | None:
    """Return a valid color string (or None), with a warning if it's not valid."""
    if not isinstance(value, str):
        warnings.append(
            f"colors.{key} must be a string, got {type(value).__name__}; "
            f"using defaults instead."
        )
        return None
    try:
        Color.parse(value)
    except ColorParseError:
        warnings.append(
            f"colors.{key} = {value!r} isn't a valid color; "
            f"using defaults instead."
        )
        return None
    return value


def _validate_sidebar_width(value: object, warnings: list[str]) -> int:
    """Return a valid sidebar width, falling back to default."""
    if isinstance(value, bool) or not isinstance(value, int):
        warnings.append(
            f"ui.sidebar_width must be an integer, got {value!r}; "
            f"using defaults instead."
        )
        return DEFAULT_SIDEBAR_WIDTH
    if not MIN_SIDEBAR_WIDTH <= value <= MAX_SIDEBAR_WIDTH:
        warnings.append(
            f"ui.sidebar_width = {value} is out of range "
            f"({MIN_SIDEBAR_WIDTH}-{MAX_SIDEBAR_WIDTH}); "
            f"using defaults instead."
        )
        return DEFAULT_SIDEBAR_WIDTH
    return value


def load_config(path: Path | str | None = None) -> Config:
    """If you know how to read python, you know that this loads the TOML configuration.
    (and it also falls back to default if a problem occurs, somehow)
    The file missing obviously isn't an error, but the default theme is still used if it is, and
    it also won't complain about it.

    Any other thing such as bad TOML or a bad value produces a stderr warning, and falls back to the default.
    """
    cfg_path = Path(path) if path is not None else config_path()

    if not cfg_path.is_file():
        return Config()

    try:
        with open(cfg_path, "rb") as config_file:
            data = tomllib.load(config_file)
    except tomllib.TOMLDecodeError as error:
        return Config(warnings=(f"{cfg_path} is invalid TOML: {error}",))
    except OSError as error:
        return Config(warnings=(f"cannot read {cfg_path}: {error}",))

    warnings: list[str] = []

    colors = dict(DEFAULT_COLORS)
    sidebar_width = DEFAULT_SIDEBAR_WIDTH

    known_sections = {"colors", "ui"}
    for section in data:
        if section not in known_sections:
            warnings.append(f"unknown section [{section}], ignoring.")

    raw_colors = data.get("colors", {})
    if not isinstance(raw_colors, dict):
        warnings.append("[colors] must be a table, using defaults instead.")
        raw_colors = {}

    for key, value in raw_colors.items():
        if key not in DEFAULT_COLORS:
            warnings.append(
                f"unknown color {key!r} "
                f"(valid: {', '.join(DEFAULT_COLORS)})"
            )
            continue
        validated = _validate_color(key, value, warnings)
        if validated is not None:
            colors[key] = validated

    raw_ui = data.get("ui", {})
    if not isinstance(raw_ui, dict):
        warnings.append("[ui] must be a table; using defaults instead.")
        raw_ui = {}

    for key, value in raw_ui.items():
        if key != "sidebar_width":
            warnings.append(f"unknown option ui.{key} ignoring.")
            continue
        sidebar_width = _validate_sidebar_width(value, warnings)

    return Config(
        colors=colors,
        sidebar_width=sidebar_width,
        warnings=tuple(warnings),
    )
