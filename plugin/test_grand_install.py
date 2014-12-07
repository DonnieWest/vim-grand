#! /usr/bin/env python

import unittest
import sys
import os
from mock import patch
from mock import MagicMock

# We don't actually use this mock, but otherwise python can't find the vim
# module at all because it is only available when run from vim
sys.modules['vim'] = MagicMock() 

from grand_install import GrandInstall

class TestGrandInstall (unittest.TestCase):

    @patch('grand_install.vim')
    def testVimGrandCtagsFile(self, mock_vim):

        GrandInstall().executeCommand();

        mock_vim.eval.assert_any_call("exists(':Dispatch')")
        mock_vim.command.assert_any_call('Dispatch gradle installDebug -q')

    @patch('grand_install.vim')
    def testHasDispatchInstalld(self, mock_vim):

        GrandInstall().hasDispatchInstalled();

        mock_vim.eval.assert_called_with("exists(':Dispatch')")


    @patch('grand_install.vim')
    def testInstallUsingDispatch(self, mock_vim):

        GrandInstall().installUsingDispatch();

        mock_vim.command.assert_called_with('Dispatch gradle installDebug -q')


    @patch('grand_install.vim')
    def testInstallUsingVanillaShell(self, mock_vim):

        GrandInstall().installUsingVanillaBang()

        mock_vim.command.assert_called_with('! gradle installDebug -q')
