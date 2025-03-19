from textnode import TextNode, TextType


def main():
    new_node = TextNode("This is anchor text", TextType.LINK, "http://suepr.com")
    print(new_node)


main()
