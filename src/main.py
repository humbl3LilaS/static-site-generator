from generators import copy_directory_recursive, generate_page_recursive
from pathlib import Path
import shutil


def main():
    project_root = Path(__file__).parent.parent

    public_dir = project_root / "public"
    static_dir = project_root / "static"

    if public_dir.exists():
        shutil.rmtree(public_dir)

    copy_directory_recursive(static_dir, public_dir)

    content_dir = project_root / "content"
    template = project_root / "template.html"

    generate_page_recursive(content_dir, template, public_dir)


main()
