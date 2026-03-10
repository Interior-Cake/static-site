from textnode import *
from htmlnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif delimiter not in ["**","`","_"]:
            raise Exception(f"The entered delimiter: {delimiter} , is not valid markdown.")
        else:
            split_node = node.text.split(delimiter)
            for i in range(len(split_node)):
                if i%2 == 0 or i == 0:
                    new_nodes.append(TextNode(split_node[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_node[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text is None:
            pass
        elif "!" not in node.text:
            new_nodes.append(node)
        else:
            sections = re.split(r"(!\[.*?\]\(.*?\))", node.text)
            for i in range(len(sections)):
                if (i%2== 0 or i == 0):
                    if sections[i] != "":
                        new_nodes.append(TextNode(sections[i], TextType.PLAIN))
                else:
                    if sections[i] != "":
                        image = extract_markdown_images(sections[i])
                        new_nodes.append(TextNode(image[0][0], TextType.IMAGE, image[0][1]))
    return new_nodes
        

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text is None:
            pass
        elif "[" not in node.text:
            new_nodes.append(node)
        else:
            sections = re.split(r"(\[.*?\]\(.*?\))", node.text)
            for i in range(len(sections)):
                if (i%2== 0 or i == 0):
                    if sections[i] != "":
                        new_nodes.append(TextNode(sections[i], TextType.PLAIN))
                else:
                    if sections[i] != "":
                        link = extract_markdown_links(sections[i])
                        new_nodes.append(TextNode(link[0][0], TextType.LINK, link[0][1]))               
    return new_nodes

def text_to_text_nodes(text):
    original_text = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(original_text,"**",TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"_",TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    for node in nodes:
        if node.text_type == TextType.TEXT:
            node.text_type = TextType.PLAIN
    return nodes

def extract_markdown_images(text):
    alt_texts = re.findall(r"!\[([^\[\]]*)\]", text)
    src_texts = re.findall(r"(?<=\()(.*?)(?=\))", text)
    if len(alt_texts) != len(src_texts):
        raise Exception("Error: Markdown images require alt text and src text.")
    tuples = []
    for i in range(len(alt_texts)):
        tuples.append((alt_texts[i], src_texts[i]))
    return tuples

def extract_markdown_links(text):
    anchor_texts = re.findall(r"(?<=\[)(.*?)(?=\])", text)
    links = re.findall(r"(?<=\()(.*?)(?=\))", text)
    if len(anchor_texts) != len(links):
        raise Exception("Error: Markdown links require anchor text and urls.")
    tuples = []
    for i in range(len(links)):
        tuples.append((anchor_texts[i], links[i]))
    return tuples

def extract_title(markdown):
    title = re.findall(r"(# .*)", markdown)
    if len(title) < 1:
        raise Exception("No title found in markdown document.")
    title = title[0].strip("#")
    title = title.strip()
    return title