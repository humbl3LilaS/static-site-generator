from pathlib import Path
from block_markdown import markdown_to_html_node
import shutil

from util import extract_title


def copy_directory_recursive(src: Path, dst: Path) -> None:
    if not dst.exists():
        dst.mkdir()

    for f in src.iterdir():
        new_f = dst / f.name
        if f.is_dir():
            copy_directory_recursive(f, new_f)
        else:
            print(f"Copying {f} to {new_f}")
            shutil.copy(f, new_f)


def generate_page(form_path: Path, template_path: Path, dest_path):
    print(f"Generating {form_path}")
    markdown_content = form_path.read_text()
    template_content = template_path.read_text()

    html_output = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_output)

    if not dest_path.parent.exists():
        dest_path.parent.mkdir()

    dest_path.write_text(template_content)


def generate_page_recursive(source_path: Path, template_path: Path, dest_path: Path):
    if not dest_path.exists():
        dest_path.mkdir()

    for f in source_path.iterdir():
        new_f = dest_path / f.name

        if f.is_dir():
            generate_page_recursive(f, template_path, new_f)
        else:
            if f.suffix.lower() == ".md":
                generate_page(f, template_path, new_f.with_suffix(".html"))
            else:
                print(f"Ignoring {f}")
