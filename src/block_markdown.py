from enum import Enum, auto
import re
from delimitors import text_to_textnodes
from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def markdown_to_blocks(markdown: str):
    return [block.strip() for block in markdown.split("\n\n") if block != ""]


def block_to_block_type(block: str):
    if __check_if_heading_block(block):
        return BlockType.HEADING
    elif __check_if_quote_block(block):
        return BlockType.QUOTE
    elif __check_if_code_block(block):
        return BlockType.CODE
    elif __check_if_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif __check_if_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def __check_if_heading_block(block: str) -> bool:
    return bool(re.match(r"^(#{1,6})\s+(.+)$", block))


def __check_if_code_block(block: str) -> bool:
    return block[:3] == "```" and block[-3:] == "```"


def __check_if_quote_block(block: str) -> bool:
    for line in block.split("\n"):
        if not line.startswith(">"):
            return False
    return True


def __check_if_unordered_list(block: str) -> bool:
    for line in block.split("\n"):
        if not line.startswith("-"):
            return False
    return True


def __check_if_ordered_list(block: str) -> bool:
    lines = block.split("\n")
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}."):
            return False
    return True


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    result = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                result.append(__paragraph_block_to_html(block))
            case BlockType.QUOTE:
                result.append(__quote_block_to_html(block))
            case BlockType.UNORDERED_LIST:
                result.append(__unordered_list_block_to_html(block))
            case BlockType.ORDERED_LIST:
                result.append(__ordered_list_block_to_html(block))
            case BlockType.CODE:
                result.append(__code_block_to_html(block))
            case BlockType.HEADING:
                result.append(__header_block_to_html(block))

    return ParentNode("div", result)


def __code_block_to_html(block: str):
    content = block.strip("```").lstrip("\n")
    return ParentNode("pre", [LeafNode("code", content)])


def __header_block_to_html(block: str):
    level = len(re.findall("#", block))
    content = block.lstrip(f"{level * "#"} ")
    return LeafNode(f"h{level}", content)


def __paragraph_block_to_html(block: str):
    content = " ".join(list(map(lambda line: line.strip(), block.split("\n"))))
    text_nodes = list(map(text_node_to_html_node, text_to_textnodes(content)))
    return ParentNode("p", text_nodes)


def __quote_block_to_html(block: str):
    lines = list(map(lambda line: line[1:].lstrip(), block.split("\n")))
    content = " ".join(lines)
    return LeafNode("blockquote", content)


def __unordered_list_block_to_html(block: str):
    lines = list(map(lambda line: line[2:], block.split("\n")))
    text_nodes_per_line = list(map(lambda line: text_to_textnodes(line), lines))
    html_nodes = list(
        map(
            lambda nodes:
            ParentNode("li",
                       list(map(lambda t_node: text_node_to_html_node(t_node), nodes))
                       ),
            text_nodes_per_line))
    return ParentNode("ul", html_nodes)


def __ordered_list_block_to_html(block: str):
    lines = list(map(lambda line: line[3:], block.split("\n")))

    text_nodes_per_line = list(map(text_to_textnodes, lines))
    html_nodes = list(
        map(
            lambda nodes:
            ParentNode("li", list(map(text_node_to_html_node, nodes))),
            text_nodes_per_line
        )
    )

    return ParentNode("ol", html_nodes)
