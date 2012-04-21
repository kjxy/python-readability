import unittest

from readability_lxml.readability import Document
from readability_lxml import readability as r


class TestReadabilityDocument(unittest.TestCase):
    """Test the Document parser."""

    def test_none_input_raises_exception(self):
        """Feeding a None input to the document should blow up."""

        doc = None
        self.assertRaises(ValueError, Document, doc)


class TestFindBaseUrl(unittest.TestCase):

    def setUp(self):
        self.longMessage = True

    def _assert_url(self, url, expected_base_url, msg = None):
        actual_base_url = r.find_base_url(url)
        self.assertEqual(expected_base_url, actual_base_url, msg)

    def _run_urls(self, specs):
        """
        Asserts expected results on a sequence of specs, where each spec is a
        pair: (URL, expected base URL).
        """
        for spec in specs:
            url = spec[0]
            expected = spec[1]
            if len(spec) > 2:
                msg = spec[2]
            else:
                msg = None
            self._assert_url(url, expected, msg)

    def test_none(self):
        self._assert_url(None, None)

    def test_no_change(self):
        url = 'http://foo.com/article'
        self._assert_url(url, url)

    def test_extension_stripping(self):
        specs = [
                (
                'http://foo.com/article.html',
                'http://foo.com/article',
                'extension should be stripped'
                ),
                (
                'http://foo.com/path/to/article.html',
                'http://foo.com/path/to/article',
                'extension should be stripped'
                ),
                (
                'http://foo.com/article.123not',
                'http://foo.com/article.123not',
                '123not is not extension'
                ),
                (
                'http://foo.com/path/to/article.123not',
                'http://foo.com/path/to/article.123not',
                '123not is not extension'
                )
                ]
        self._run_urls(specs)

    def test_ewcms(self):
        self._assert_url(
                'http://www.ew.com/ew/article/0,,20313460_20369436,00.html',
                'http://www.ew.com/ew/article/0,,20313460_20369436'
                )

    def test_page_numbers(self):
        specs = [
                (
                'http://foo.com/page5.html',
                'http://foo.com',
                'page number should be stripped'
                ),
                (
                'http://foo.com/path/to/page5.html',
                'http://foo.com/path/to',
                'page number should be stripped'
                ),
                (
                'http://foo.com/article-5.html',
                'http://foo.com/article',
                'page number should be stripped'
                )
                ]
        self._run_urls(specs)

    def test_numbers(self):
        specs = [
                (
                'http://foo.com/5.html',
                'http://foo.com',
                'number should be stripped'
                ),
                (
                'http://foo.com/path/to/5.html',
                'http://foo.com/path/to',
                'number should be stripped'
                )
                ]
        self._run_urls(specs)

