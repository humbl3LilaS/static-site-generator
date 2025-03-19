from functools import reduce


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        res = reduce(lambda acc, curr: acc + [f'{curr[0]}="{curr[1]}"'], self.props.items(), [])
        return " ".join(res)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value):
        super().__init__(tag, value)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        return self.value if self.tag is None else f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid Parent Node: no tag")
        if self.children is None:
            raise ValueError("invalid Parent Node: no children")

        child_html = list(map(lambda x: x.to_html(), self.children))
        return self.__tag("".join(child_html))

    def __tag(self, value):
        if self.tag is None:
            raise ValueError("invalid Parent Node: no tag")
        return f"<{self.tag}>{value}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
