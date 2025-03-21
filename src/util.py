def extract_title(markdown: str):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]

    raise Exception("markdown file need a title")

print(extract_title("""
This is a paragraph holy crap jesus

# This is the title
"""))