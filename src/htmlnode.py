from blocks import *
from process_functions import *
import re

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Not yet implemented. Child class should override.")
    
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        formatted_text = []
        for prop in self.props:
            formatted_text.append(f'{prop}="{self.props[prop]}"')
        return " " + " ".join(formatted_text)
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        else:
            return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>{self.value}"
        if self.tag == "a":
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {super().props_to_html()})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("parent nodes require a tag")
        if self.children == None:
            raise ValueError("parent nodes require at least 1 child node")
        final_string = ""
        for child in self.children:
            final_string += child.to_html()
        return f"<{self.tag}>{final_string}</{self.tag}>"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href":text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception("Parameter was not a text node. Unable to convert to a html node.")

def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    html_children = []
    for node in text_nodes:
        html_children.append(text_node_to_html_node(node))
    return html_children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_parent_node_list = []
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            heading_type = block.count("#",0,5)
            words = block.split("#")
            heading = " ".join(words[heading_type:]).strip()
            children = text_to_children(heading)
            html_parent_node_list.append(ParentNode(f"h{heading_type}",children))
        elif block_to_block_type(block) == BlockType.QUOTE:
            lines = block.split("\n")
            final_string = ""
            for line in lines:
                line_child = line.strip("> ")
                final_string += line_child + "\n"
            html_parent_node_list.append(ParentNode(f"blockquote", text_to_children(final_string)))
        elif block_to_block_type(block) == BlockType.CODE:
            lines = block.split("\n")
            code = "\n".join(lines[1:-1])
            code += "\n"
            code_block = TextNode(code, TextType.CODE)
            html_code = text_node_to_html_node(code_block)
            html_parent_node_list.append(ParentNode("pre", [html_code]))
        elif block_to_block_type(block) == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            items = []
            for line in lines:
                line_child = text_to_children(line.strip("- "))
                items.append(ParentNode("li", line_child))
            html_parent_node_list.append(ParentNode("ul", items))
        elif block_to_block_type(block) == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            items = []
            for line in lines:
                line_child = text_to_children(line.split(". ", 1)[1])
                items.append(ParentNode("li", line_child))
            html_parent_node_list.append(ParentNode("ol", items))
        else:
            lines = block.split("\n")
            string = " ".join(lines)
            children = text_to_children(string)
            for child in children:
                if child.value == None:
                    children.remove(child)
            html_parent_node_list.append(ParentNode("p", children))
    return ParentNode("div", html_parent_node_list)