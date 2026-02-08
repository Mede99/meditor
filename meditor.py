import sys

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TextArea


class Meditor(App):
    """A terminal-based text editor."""

    TITLE = "Meditor"

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+s", "save", "Save"),
    ]

    def __init__(self, filepath: str = None):
        super().__init__()
        self.filepath = filepath
        self.text_content = ""
        self.is_new_file = False

        # Load file if provided
        if self.filepath:
            try:
                with open(self.filepath, "r") as f:
                    self.text_content = f.read()
            except FileNotFoundError:
                # File doesn't exist, we'll create it on save
                self.text_content = ""
                self.is_new_file = True
            except Exception as e:
                self.text_content = f"Error loading file: {str(e)}"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield TextArea(self.text_content, language="python")
        yield Footer()

    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()

    def action_save(self) -> None:
        """Save the current content to file."""
        if not self.filepath:
            return

        # Get the TextArea widget
        text_area = self.query_one(TextArea)

        try:
            with open(self.filepath, "w") as f:
                f.write(text_area.text)

            if self.is_new_file:
                self.notify(
                    f"Created and saved {self.filepath}", severity="information"
                )
                self.is_new_file = False
            else:
                self.notify(f"Saved to {self.filepath}", severity="information")
        except Exception as e:
            self.notify(f"Error saving file: {str(e)}", severity="error")


def main():
    """Entry point for the application."""
    filepath = sys.argv[1] if len(sys.argv) > 1 else None

    if not filepath:
        print("Usage: python meditor.py <filename>")
        sys.exit(1)

    app = Meditor(filepath)
    app.run()


if __name__ == "__main__":
    main()
