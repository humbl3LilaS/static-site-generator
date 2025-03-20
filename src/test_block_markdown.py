import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_block(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockMarkdown(unittest.TestCase):
    def test_h1(self):
        markdown_block = "# This is a h1 heading"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.HEADING

        self.assertEqual(result, expected_result)

    def test_h6(self):
        markdown_block = "###### This is a h6 heading"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.HEADING

        self.assertEqual(result, expected_result)

    def test_not_h2(self):
        markdown_block = "##This is not a h2 heading so it should be a paragraph"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.PARAGRAPH

        self.assertEqual(result, expected_result)

    def test_code(self):
        markdown_block = "``` this is a code block ```"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.CODE

        self.assertEqual(result, expected_result)

    def test_code_multiline(self):
        markdown_block = "```python\n this is a\nmultiline\n code block\n ```"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.CODE

        self.assertEqual(result, expected_result)

    def test_not_code(self):
        markdown_block = "``` this is a bad code block ``"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.PARAGRAPH

        self.assertEqual(result, expected_result)

    def test_quote(self):
        markdown_block = "> this is a quote"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.QUOTE

        self.assertEqual(result, expected_result)

    def test_quote_multi(self):
        markdown_block = "> this is a quote\n> that spans\n>multiple\n>lines."

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.QUOTE

        self.assertEqual(result, expected_result)

    def test_quote_bad(self):
        markdown_block = "> this is a quote\n> that spans multiple\nlines poorly"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.PARAGRAPH

        self.assertEqual(result, expected_result)

    def test_unordered_list(self):
        markdown_block = "- this is an\n- unordered\n- list"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.UNORDERED_LIST

        self.assertEqual(result, expected_result)

    def test_unordered_list_bad(self):
        markdown_block = "* this is an\n*unordered\n* bad\n-list"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.PARAGRAPH

        self.assertEqual(result, expected_result)

    def test_ordered_list(self):
        markdown_block = "1. this is an\n2. ordered\n3. list"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.ORDERED_LIST

        self.assertEqual(result, expected_result)

    def test_ordered_list_bad(self):
        markdown_block = "1. this is an\n1. ordered\n2. list"

        result = block_to_block_type(markdown_block)

        expected_result = BlockType.PARAGRAPH

        self.assertEqual(result, expected_result)


class TestMarkdownToHtmlNodes(unittest.TestCase):
    def test_empty_md(self):
        markdown = ""
        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div></div>"

        self.assertEqual(result, expected_result)

    def test_simple_md(self):
        markdown = "hi"
        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div><p>hi</p></div>"

        self.assertEqual(result, expected_result)

    def test_blockquote(self):
        markdown = """
> This is a
> blockquote block

this is paragraph text

"""

        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>"
        self.assertEqual(result, expected_result)

    def test_paragraphs(self):
        markdown = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(result, expected_result)

    def test_lists(self):
        markdown = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>"

        self.assertEqual(result, expected_result)

    def test_headings(self):
        markdown = """
# this is an h1

this is paragraph text

## this is an h2
"""

        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>"
        self.assertEqual(result, expected_result)
