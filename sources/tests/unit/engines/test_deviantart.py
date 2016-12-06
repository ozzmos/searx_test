from collections import defaultdict
import mock
from searx.engines import deviantart
from searx.testing import SearxTestCase


class TestDeviantartEngine(SearxTestCase):

    def test_request(self):
        query = 'test_query'
        dicto = defaultdict(dict)
        dicto['pageno'] = 0
        params = deviantart.request(query, dicto)
        self.assertTrue('url' in params)
        self.assertTrue(query in params['url'])
        self.assertTrue('deviantart.com' in params['url'])

    def test_response(self):
        self.assertRaises(AttributeError, deviantart.response, None)
        self.assertRaises(AttributeError, deviantart.response, [])
        self.assertRaises(AttributeError, deviantart.response, '')
        self.assertRaises(AttributeError, deviantart.response, '[]')

        response = mock.Mock(text='<html></html>')
        self.assertEqual(deviantart.response(response), [])

        response = mock.Mock(status_code=302)
        self.assertEqual(deviantart.response(response), [])

        html = """
        <div class="tt-a tt-fh tt-boxed" collect_rid="1:149167425"
            usericon="http://a.deviantart.net/avatars/t/e/test-0.gif" userid="233301"
            username="test-0" symbol="~" category="digitalart/animation">
            <span class="tt-w" style="width: auto; max-width: 277px;">
                <span class="tt-fh-tc" style="width: 202px;">
                    <span class="tt-bb" style="width: 202px;">
                    </span>
                    <span class="shadow">
                        <a class="thumb" href="http://url.of.result/2nd.part.of.url"
                            title="Behoimi BE Animation Test by test-0, Jan 4,
                            2010 in Digital Art &gt; Animation"> <i></i>
                            <img width="200" height="200" alt="Test"
                                src="http://url.of.thumbnail" data-src="http://th08.deviantart.net/test.jpg">
                        </a>
                    </span>
                    <!-- ^TTT -->
                </span>
                <span class="details">
                    <a href="http://test-0.deviantart.com/art/Test" class="t"
                        title="Behoimi BE Animation Test by test-0, Jan 4, 2010">
                        <span class="tt-fh-oe">Title of image</span> </a>
                    <small>
                    <span class="category">
                        <span class="age">
                            5 years ago
                        </span>
                        in <a title="Behoimi BE Animation Test by test-0, Jan 4, 2010"
                            href="http://www.deviantart.com/browse/all/digitalart/animation/">Animation</a>
                    </span>
                    <div class="commentcount">
                        <a href="http://test-0.deviantart.com/art/Test#comments">
                        <span class="iconcommentsstats"></span>9 Comments</a>
                    </div>
                    <a class="mlt-link" href="http://www.deviantart.com/morelikethis/149167425">
                    <span class="mlt-icon"></span> <span class="mlt-text">More Like This</span> </a>
                </span>
                </small> <!-- TTT$ -->
            </span>
        </div>
        """
        response = mock.Mock(text=html)
        results = deviantart.response(response)
        self.assertEqual(type(results), list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Title of image')
        self.assertEqual(results[0]['url'], 'http://url.of.result/2nd.part.of.url')
        self.assertNotIn('content', results[0])
        self.assertEqual(results[0]['thumbnail_src'], 'https://url.of.thumbnail')

        html = """
        <span class="tt-fh-tc" style="width: 202px;">
            <span class="tt-bb" style="width: 202px;">
            </span>
            <span class="shadow">
                <a class="thumb" href="http://url.of.result/2nd.part.of.url"
                    title="Behoimi BE Animation Test by test-0, Jan 4,
                    2010 in Digital Art &gt; Animation"> <i></i>
                    <img width="200" height="200" alt="Test"
                        src="http://url.of.thumbnail" data-src="http://th08.deviantart.net/test.jpg">
                </a>
            </span>
            <!-- ^TTT -->
        </span>
        <span class="details">
            <a href="http://test-0.deviantart.com/art/Test" class="t"
                title="Behoimi BE Animation Test by test-0, Jan 4, 2010">
                <span class="tt-fh-oe">Title of image</span> </a>
            <small>
            <span class="category">
                <span class="age">
                    5 years ago
                </span>
                in <a title="Behoimi BE Animation Test by test-0, Jan 4, 2010"
                    href="http://www.deviantart.com/browse/all/digitalart/animation/">Animation</a>
            </span>
            <div class="commentcount">
                <a href="http://test-0.deviantart.com/art/Test#comments">
                <span class="iconcommentsstats"></span>9 Comments</a>
            </div>
            <a class="mlt-link" href="http://www.deviantart.com/morelikethis/149167425">
            <span class="mlt-icon"></span> <span class="mlt-text">More Like This</span> </a>
        </span>
        </small> <!-- TTT$ -->
        """
        response = mock.Mock(text=html)
        results = deviantart.response(response)
        self.assertEqual(type(results), list)
        self.assertEqual(len(results), 0)
