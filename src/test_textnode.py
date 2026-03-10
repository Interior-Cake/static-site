import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is not a text node", TextType.PLAIN)
        node2 = TextNode("Also this is not a text nde", TextType.PLAIN)
        self.assertNotEqual

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK)
        if node.url == None:
            self.assertTrue
        else:
            self.assertFalse

if __name__ == "__main__":
    unittest.main()