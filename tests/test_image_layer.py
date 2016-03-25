# -*- coding: utf-8 -*-

"""Test the ImageLayer abstraction class"""

import unittest
import string
import random
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from docktree.ImageLayer import ImageLayer
from docktree.ImageLayer import _convert_size


def generate_valid_identifier():
    """:return a random but valid identifier for image layers"""
    allowed_id_chars = list(set(string.hexdigits.lower()))
    return ''.join(
        (random.choice(allowed_id_chars) for _ in range(64))
    )


def generate_tag():
    """:return a random but valid tag for image layers"""
    allowed_tag_chars = string.ascii_letters + string.digits
    return ''.join(
        (random.choice(allowed_tag_chars) for _ in range(
            random.randint(1, 100)
        ))
    )


class TestImageLayer(unittest.TestCase):
    """Test the ImageLayer abstraction class"""

    def test_init_without_id(self):
        """test if identifier is required"""
        self.assertRaises(TypeError, ImageLayer)

    def test_identifier_prop(self):
        """test the identifier property"""
        identifier = generate_valid_identifier()
        layer = ImageLayer(identifier)
        self.assertEqual(identifier, layer.identifier)
        # change identifier
        self.assertRaises(
            AttributeError, setattr,
            layer, 'identifier', generate_valid_identifier()
        )

    def test_tags_prop(self):
        """test the tags property"""
        identifier = generate_valid_identifier()
        tags = [generate_tag() for _ in range(random.randint(0, 50))]
        layer = ImageLayer(identifier, tags=tags)
        self.assertEqual(layer.tags, tags)
        newtag = generate_tag()
        tags += newtag
        layer.tags.append(tags)
        self.assertEqual(layer.tags, tags)
        tags = [generate_tag() for _ in range(2)]
        layer.tags = tags
        self.assertEqual(layer.tags, tags)

    def test_size_prop(self):
        """test the tags property"""
        identifier = generate_valid_identifier()
        size = random.randint(0, 9999999999999)
        layer = ImageLayer(identifier, size=size)
        self.assertEqual(layer.size, size)
        # change size
        self.assertRaises(
            AttributeError, setattr,
            layer, 'size', random.randint(0, 9999999999999)
        )

    def test_join_parent_child(self):
        """test the join_parent_child function to build the tree"""
        id_head = generate_valid_identifier()
        layer_head = ImageLayer(
            identifier=id_head,
            tags=['head'],
        )
        id_middle = generate_valid_identifier()
        layer_middle = ImageLayer(
            identifier=id_middle,
            tags=['middle'],
        )
        id_middle2 = generate_valid_identifier()
        layer_middle2 = ImageLayer(
            identifier=id_middle2,
            tags=['middle2'],
        )
        id_child = generate_valid_identifier()
        layer_child = ImageLayer(
            identifier=id_child,
            tags=['child'],
        )
        self.assertIsNone(layer_head.parent)
        self.assertIsNone(layer_middle.parent)
        self.assertIsNone(layer_middle2.parent)
        self.assertIsNone(layer_child.parent)
        self.assertEqual(len(layer_head.children), 0)
        self.assertEqual(len(layer_middle.children), 0)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        # join head and middle
        ImageLayer.join_parent_child(parent=layer_head, child=layer_middle)
        self.assertIsNone(layer_head.parent)
        self.assertEqual(layer_middle.parent, layer_head)
        self.assertIsNone(layer_middle2.parent)
        self.assertIsNone(layer_child.parent)
        self.assertEqual(len(layer_head.children), 1)
        self.assertEqual(len(layer_middle.children), 0)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        self.assertEqual(layer_head.children[0], layer_middle)
        # join head and middle2
        ImageLayer.join_parent_child(parent=layer_head, child=layer_middle2)
        self.assertIsNone(layer_head.parent)
        self.assertEqual(layer_middle.parent, layer_head)
        self.assertEqual(layer_middle2.parent, layer_head)
        self.assertIsNone(layer_child.parent)
        self.assertEqual(len(layer_head.children), 2)
        self.assertEqual(len(layer_middle.children), 0)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        self.assertEqual(layer_head.children[0], layer_middle)
        self.assertEqual(layer_head.children[1], layer_middle2)
        # join middle and child
        ImageLayer.join_parent_child(parent=layer_middle, child=layer_child)
        self.assertIsNone(layer_head.parent)
        self.assertEqual(layer_middle.parent, layer_head)
        self.assertEqual(layer_middle2.parent, layer_head)
        self.assertEqual(layer_child.parent, layer_middle)
        self.assertEqual(len(layer_head.children), 2)
        self.assertEqual(len(layer_middle.children), 1)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        self.assertEqual(layer_head.children[0], layer_middle)
        self.assertEqual(layer_head.children[1], layer_middle2)
        self.assertEqual(layer_middle.children[0], layer_child)

    def test_remove_from_chain(self):
        """Test the remove_from_chain function to reduce the tree"""
        id_head = generate_valid_identifier()
        layer_head = ImageLayer(
            identifier=id_head,
            tags=['head'],
        )
        id_middle = generate_valid_identifier()
        layer_middle = ImageLayer(
            identifier=id_middle,
            tags=['middle'],
        )
        id_middle2 = generate_valid_identifier()
        layer_middle2 = ImageLayer(
            identifier=id_middle2,
            tags=['middle2'],
        )
        id_child = generate_valid_identifier()
        layer_child = ImageLayer(
            identifier=id_child,
            tags=['child'],
        )
        # build tree
        ImageLayer.join_parent_child(parent=layer_head, child=layer_middle)
        ImageLayer.join_parent_child(parent=layer_head, child=layer_middle2)
        ImageLayer.join_parent_child(parent=layer_middle, child=layer_child)
        # remove middle2 from chain
        layer_middle2.remove_from_chain()
        self.assertIsNone(layer_head.parent)
        self.assertEqual(layer_middle.parent, layer_head)
        self.assertIsNone(layer_middle2.parent)
        self.assertEqual(layer_child.parent, layer_middle)
        self.assertEqual(len(layer_head.children), 1)
        self.assertEqual(len(layer_middle.children), 1)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        self.assertEqual(layer_head.children[0], layer_middle)
        self.assertEqual(layer_middle.children[0], layer_child)
        # remove middle from chain
        layer_middle.remove_from_chain()
        self.assertIsNone(layer_head.parent)
        self.assertIsNone(layer_middle.parent)
        self.assertIsNone(layer_middle2.parent)
        self.assertEqual(layer_child.parent, layer_head)
        self.assertEqual(len(layer_head.children), 1)
        self.assertEqual(len(layer_middle.children), 0)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)
        # remove head from chain
        layer_head.remove_from_chain()
        self.assertIsNone(layer_head.parent)
        self.assertIsNone(layer_middle.parent)
        self.assertIsNone(layer_middle2.parent)
        self.assertIsNone(layer_child.parent)
        self.assertEqual(len(layer_head.children), 0)
        self.assertEqual(len(layer_middle.children), 0)
        self.assertEqual(len(layer_middle2.children), 0)
        self.assertEqual(len(layer_child.children), 0)

    def test_str(self):
        """test the __str__ function"""
        identifier = generate_valid_identifier()
        tags = [generate_tag()]
        size = random.randint(0, 9999999999999)
        size_human = _convert_size(size)
        layer = ImageLayer(identifier, tags=tags, size=size)
        self.assertEqual(
            str(layer),
            "{0} Tags: {1} Size: {2}".format(identifier[:12], tags, size_human)
        )

    def test_convert_size(self):
        """test the size to human conversation"""
        self.assertEqual(_convert_size(0), '0 B')
        self.assertEqual(_convert_size(1), '1 B')
        self.assertEqual(_convert_size(1023), '1023 B')
        self.assertEqual(_convert_size(1024), '1.0 KiB')
        self.assertEqual(_convert_size(1023*1024), '1023.0 KiB')
        self.assertEqual(_convert_size(1024*1024), '1.0 MiB')
        self.assertEqual(_convert_size(1023*1024*1024), '1023.0 MiB')
        self.assertEqual(_convert_size(1024*1024*1024), '1.0 GiB')
        self.assertEqual(_convert_size(1023*1024*1024*1024), '1023.0 GiB')
        self.assertEqual(_convert_size(1024*1024*1024*1024), '1.0 TiB')
        self.assertEqual(_convert_size(1023*1024*1024*1024*1024), '1023.0 TiB')

    def test_print_tree(self):
        """test the print_tree function"""
        id_child = generate_valid_identifier()
        size_child = 42*1024*1024*1024
        layer_child = ImageLayer(
            identifier=id_child,
            tags=['child'],
            size=size_child,
        )
        id_parent = generate_valid_identifier()
        size_parent = 10*1024*1024
        layer_parent = ImageLayer(
            identifier=id_parent,
            tags=['parent'],
            size=size_parent,
        )
        ImageLayer.join_parent_child(parent=layer_parent, child=layer_child)
        self.assertEqual(
            layer_parent.print_tree(),
            "- {id_head} Tags: ['parent'] Size: {size_head}\n"
            "  |- {id_child} Tags: ['child'] Size: {size_child}\n".format(
                id_head=id_parent[:12],
                id_child=id_child[:12],
                size_head=_convert_size(size_parent),
                size_child=_convert_size(size_child),
            )
        )