from pathlib import Path

import markdown
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.widgets.webview import WebView


class MarkdownPage:
    def __init__(self, file_name):
        self.project_root = Path(__file__).parent
        self.resources_path = self.project_root / "resources" / "md"
        self.file_path = self.resources_path / file_name
        self.web_view = WebView(style=Pack(flex=1, width=290, height=700))

    def load_content(self):
        try:
            md_content = self.file_path.read_text()
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.5; padding: 20px; }}
                    h1, h2, h3 {{ color: #333; }}
                    p {{ margin-bottom: 15px; }}
                </style>
            </head>
            <body>
                {markdown.markdown(md_content)}
            </body>
            </html>
            """
            self.web_view.set_content("", content=html_content)
        except FileNotFoundError:
            self.web_view.set_content(
                "", content=f"<p>File not found: {self.file_path.resolve()}</p>"
            )

    def get_widget(self):
        self.load_content()
        return self.web_view

    def list_markdown_files(self):
        markdown_files = [
            file.name for file in self.resources_path.glob("*.md") if file.is_file()
        ]
        return (
            "\n".join(markdown_files) if markdown_files else "No Markdown files found."
        )

    @classmethod
    def get_available_pages(cls):
        resources_path = Path(__file__).parent / "resources" / "md"
        return [file.stem for file in resources_path.glob("*.md") if file.is_file()]


class SidebarApp(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=ROW, flex=1))
        sidebar = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=0.2))
        self.content_area = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=0.8))

        # Dynamically create buttons for each available Markdown file
        available_pages = MarkdownPage.get_available_pages()
        for page_name in sorted(available_pages):
            button = toga.Button(
                f"Page {page_name.replace("page", "")}", 
                on_press=self.show_page(page_name), 
                style=Pack(padding=5)
            )
            sidebar.add(button)

        main_box.add(sidebar)
        main_box.add(self.content_area)

        self.main_window = toga.MainWindow(
            title="Camino: Who was St James?", size=(800, 600)
        )
        self.main_window.content = main_box
        self.main_window.show()

    def show_page(self, page_name):
        def _show_page(widget):
            page = MarkdownPage(f"{page_name}.md")
            self.update_content(page)

        return _show_page

    def update_content(self, page):
        self.content_area.remove(
            *self.content_area.children
        )  # Remove all existing children
        self.content_area.add(page.get_widget())
        self.content_area.refresh()  # Force a refresh of the content area


def main():
    return SidebarApp()
