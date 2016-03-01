# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from polklibrary.type.coursepages.testing import POLKLIBRARY_TYPE_COURSEPAGES_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that polklibrary.type.coursepages is properly installed."""

    layer = POLKLIBRARY_TYPE_COURSEPAGES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if polklibrary.type.coursepages is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('polklibrary.type.coursepages'))

    def test_browserlayer(self):
        """Test that IPolklibraryTypeCoursepagesLayer is registered."""
        from polklibrary.type.coursepages.interfaces import IPolklibraryTypeCoursepagesLayer
        from plone.browserlayer import utils
        self.assertIn(IPolklibraryTypeCoursepagesLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = POLKLIBRARY_TYPE_COURSEPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['polklibrary.type.coursepages'])

    def test_product_uninstalled(self):
        """Test if polklibrary.type.coursepages is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('polklibrary.type.coursepages'))

    def test_browserlayer_removed(self):
        """Test that IPolklibraryTypeCoursepagesLayer is removed."""
        from polklibrary.type.coursepages.interfaces import IPolklibraryTypeCoursepagesLayer
        from plone.browserlayer import utils
        self.assertNotIn(IPolklibraryTypeCoursepagesLayer, utils.registered_layers())
