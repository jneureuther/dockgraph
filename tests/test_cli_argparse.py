# -*- coding: utf-8 -*-

"""Test the argparse parsers in cli"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from bin import docktree_cli as cli


class TestCliArgParse(unittest.TestCase):
    """Test the argparse parsers in cli"""

    def test_intermediate(self):
        """test if intermediate switch is parsed correctly"""
        args = cli.parse_args([])
        self.assertEqual(False, args.print_intermediate)
        args = cli.parse_args('-i'.split(' '))
        self.assertEqual(True, args.print_intermediate)
        args = cli.parse_args('--inter'.split(' '))
        self.assertEqual(True, args.print_intermediate)
        args = cli.parse_args('--intermediate'.split(' '))
        self.assertEqual(True, args.print_intermediate)

    def test_format(self):
        """test if all formats are parsed correctly"""
        args = cli.parse_args([])
        self.assertEqual('ascii', args.output_format)
        args = cli.parse_args('-f ascii'.split(' '))
        self.assertEqual('ascii', args.output_format)
        args = cli.parse_args('--fo ascii'.split(' '))
        self.assertEqual('ascii', args.output_format)
        args = cli.parse_args('--format ascii'.split(' '))
        self.assertEqual('ascii', args.output_format)
        args = cli.parse_args('-f json'.split(' '))
        self.assertEqual('json', args.output_format)
        args = cli.parse_args('--for json'.split(' '))
        self.assertEqual('json', args.output_format)
        args = cli.parse_args('--format json'.split(' '))
        self.assertEqual('json', args.output_format)