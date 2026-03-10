import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p","This is a text html node")
        node2 = HTMLNode("p","This is a text html node")
        self.assertEqual(node, node2)

    def test_neq_type(self):
        node = HTMLNode("p","This is a text html node")
        node2 = HTMLNode("p","This is also a text html node")
        self.assertNotEqual(node, node2)

    def test_convert(self):
        node = HTMLNode("a", "here", None, {"href": "https://www.google.com.au", "target": "_blank"})
        test_text = node.props_to_html()
        self.assertEqual(4,len(test_text.split()))

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", None, {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a>Click me!</a>")

    def parent_test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def parent_test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()