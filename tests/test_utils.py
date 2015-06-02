# coding: utf-8


from unittest import TestCase

try:
    from urllib.parse import urljoin
except ImportError:
    # noinspection PyUnresolvedReferences
    from urlparse import urljoin


from celerytestworker import get_application


identificator = None

class UtilsTestCase(TestCase):
    def test_get_application(self):
        self.assertEqual(get_application("tests.test_utils.identificator"), identificator)

    def test_fail_get_invalid_reference(self):
        with self.assertRaises(ImportError):
            get_application("tests.test_utils.unknown")
