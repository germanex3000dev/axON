from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, ListView, ListItem, Label, Button, 
    TextArea, Input, Static
)
from textual.binding import Binding
from textual.events import Key
from pathlib import Path
from datetime import datetime


notes_dir = Path("~/notes").expanduser()
notes_dir.mkdir(parents=True, exist_ok=True)


class NoteApp(App):
    CSS_PATH = "app.tcss"
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("n", "new_note", "New Note"),
        Binding("d", "delete_note", "Delete Note"),
        Binding("s", "save_note", "Save Note"),
        Binding("escape", "cancel_edit", "Cancel"),
        Binding("enter", "select_note", "Open Note"),
    ]
    
    def __init__(self):
        super().__init__()
        self.current_note_path: Path | None = None
        self.editing = False
        
    def get_notes(self) -> list[Path]:
        """Get all markdown notes sorted by modification time (newest first)."""
        notes = [
            f for f in notes_dir.iterdir()
            if f.is_file() and f.suffix.lower() == ".md"
        ]
        return sorted(notes, key=lambda f: f.stat().st_mtime, reverse=True)
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with Horizontal():
            # Left panel - Note list
            with Vertical(id="sidebar"):
                yield Static("NOTES", id="sidebar-title")
                yield ListView(*[
                    ListItem(Label(note.name), id=f"note-{note.stem}")
                    for note in self.get_notes()
                ], id="note-list")
                yield Button("New", id="new-note-btn")
                yield Button("Delete", id="delete-note-btn")
            
            # Right panel - Note editor
            with Vertical(id="editor-panel"):
                yield Static("No note selected", id="note-title")
                yield TextArea(
                    "",
                    id="note-editor",
                    read_only=True,
                    show_line_numbers=False,
                )
                yield Static("Press N for new note | S to save | D to delete | ESC to cancel", id="status-bar")
    
    def on_mount(self) -> None:
        self.title = "axON Notes"
        self.sub_title = "V0.1"
        self.query_one("#note-editor", TextArea).focus()
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle note selection from the list."""
        if event.item.id and event.item.id.startswith("note-"):
            note_name = event.item.id[5:]  # Remove "note-" prefix
            self.load_note(note_name)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "new-note-btn":
            self.action_new_note()
        elif event.button.id == "delete-note-btn":
            self.action_delete_note()
    
    def load_note(self, note_name: str) -> None:
        """Load a note into the editor."""
        note_path = notes_dir / f"{note_name}.md"
        if note_path.exists():
            self.current_note_path = note_path
            content = note_path.read_text(encoding="utf-8")
            editor = self.query_one("#note-editor", TextArea)
            editor.read_only = False
            editor.text = content
            editor.focus()
            self.query_one("#note-title", Static).update(f"{note_name}.md")
            self.editing = True
            self.update_status("Editing mode - Press S to save, ESC to cancel")
    
    def action_new_note(self) -> None:
        """Create a new note."""
        self.current_note_path = None
        editor = self.query_one("#note-editor", TextArea)
        editor.read_only = False
        editor.text = ""
        editor.focus()
        self.query_one("#note-title", Static).update("New Note (unsaved)")
        self.editing = True
        self.update_status("New note - Press S to save, ESC to cancel")
    
    def action_save_note(self) -> None:
        """Save the current note."""
        if not self.editing:
            return
            
        editor = self.query_one("#note-editor", TextArea)
        content = editor.text
        
        if not content:
            self.update_status("Cannot save empty note")
            return
        
        if self.current_note_path is None:
            # Create new note with timestamp-based name
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            # Try to use first line as title
            first_line = content.split('\n')[0].strip()
            if first_line and len(first_line) < 50:
                # Sanitize filename
                safe_title = "".join(c for c in first_line if c.isalnum() or c in " -_").strip()
                note_name = f"{timestamp}-{safe_title}"
            else:
                note_name = timestamp
            self.current_note_path = notes_dir / f"{note_name}.md"
        else:
            note_name = self.current_note_path.stem
        
        self.current_note_path.write_text(content, encoding="utf-8")
        
        # Update the list view
        note_list = self.query_one("#note-list", ListView)
        note_list.clear()
        for note in self.get_notes():
            note_list.append(ListItem(Label(note.name), id=f"note-{note.stem}"))
        
        self.query_one("#note-title", Static).update(f"{note_name}.md")
        editor.read_only = True
        self.editing = False
        self.update_status(f"Saved: {note_name}.md")
    
    def action_delete_note(self) -> None:
        """Delete the currently selected note."""
        if self.current_note_path and self.current_note_path.exists():
            note_name = self.current_note_path.name
            self.current_note_path.unlink()
            
            # Clear editor
            editor = self.query_one("#note-editor", TextArea)
            editor.text = ""
            editor.read_only = True
            self.current_note_path = None
            self.editing = False
            self.query_one("#note-title", Static).update("No note selected")
            
            # Update list
            note_list = self.query_one("#note-list", ListView)
            note_list.clear()
            for note in self.get_notes():
                note_list.append(ListItem(Label(note.name), id=f"note-{note.stem}"))
            
            self.update_status(f"Deleted: {note_name}")
        else:
            self.update_status("No note to delete")
    
    def action_cancel_edit(self) -> None:
        """Cancel editing and return to view mode."""
        if self.editing:
            editor = self.query_one("#note-editor", TextArea)
            if self.current_note_path and self.current_note_path.exists():
                content = self.current_note_path.read_text(encoding="utf-8")
                editor.text = content
            else:
                editor.text = ""
            editor.read_only = True
            self.editing = False
            self.update_status("Edit cancelled")
        else:
            self.action_quit()
    
    def action_select_note(self) -> None:
        """Open the highlighted note (for keyboard navigation)."""
        note_list = self.query_one("#note-list", ListView)
        if note_list.highlighted_child:
            self.load_note(note_list.highlighted_child.id[5:])
    
    def update_status(self, message: str) -> None:
        """Update the status bar message."""
        self.query_one("#status-bar", Static).update(message)


def main() -> None:
    """Entry point for the axon console script."""
    app = NoteApp()
    app.run()


if __name__ == "__main__":
    main()
