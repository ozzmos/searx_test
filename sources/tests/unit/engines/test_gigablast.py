from collections import defaultdict
import mock
from searx.engines import gigablast
from searx.testing import SearxTestCase


class TestGigablastEngine(SearxTestCase):

    def test_request(self):
        query = 'test_query'
        dicto = defaultdict(dict)
        dicto['pageno'] = 0
        dicto['language'] = 'all'
        params = gigablast.request(query, dicto)
        self.assertTrue('url' in params)
        self.assertTrue(query in params['url'])
        self.assertTrue('gigablast.com' in params['url'])

    def test_response(self):
        self.assertRaises(AttributeError, gigablast.response, None)
        self.assertRaises(AttributeError, gigablast.response, [])
        self.assertRaises(AttributeError, gigablast.response, '')
        self.assertRaises(AttributeError, gigablast.response, '[]')

        response = mock.Mock(text='{"results": []}')
        self.assertEqual(gigablast.response(response), [])

        json = """{"results": [
    {
        "title":"South by Southwest 2016",
        "dmozEntry":{
            "dmozCatId":1041152,
            "directCatId":1,
            "dmozCatStr":"Top: Regional: North America: United States",
            "dmozTitle":"South by Southwest (SXSW)",
            "dmozSum":"Annual music, film, and interactive conference.",
            "dmozAnchor":""
        },
        "dmozEntry":{
            "dmozCatId":763945,
            "directCatId":1,
            "dmozCatStr":"Top: Regional: North America: United States",
            "dmozTitle":"South by Southwest (SXSW)",
            "dmozSum":"",
            "dmozAnchor":"www.sxsw.com"
        },
        "dmozEntry":{
            "dmozCatId":761446,
            "directCatId":1,
            "dmozCatStr":"Top: Regional: North America: United States",
            "dmozTitle":"South by Southwest (SXSW)",
            "dmozSum":"Music, film, and interactive conference and festival.",
            "dmozAnchor":""
        },
        "indirectDmozCatId":1041152,
        "indirectDmozCatId":763945,
        "indirectDmozCatId":761446,
        "contentType":"html",
        "sum":"This should be the content.",
        "url":"www.sxsw.com",
        "hopCount":0,
        "size":" 102k",
        "sizeInBytes":104306,
        "bytesUsedToComputeSummary":70000,
        "docId":269411794364,
        "docScore":586571136.000000,
        "summaryGenTimeMS":12,
        "summaryTagdbLookupTimeMS":0,
        "summaryTitleRecLoadTimeMS":1,
        "site":"www.sxsw.com",
        "spidered":1452203608,
        "firstIndexedDateUTC":1444167123,
        "contentHash32":2170650347,
        "language":"English",
        "langAbbr":"en"
    }
]}
        """
        response = mock.Mock(text=json)
        results = gigablast.response(response)
        self.assertEqual(type(results), list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'South by Southwest 2016')
        self.assertEqual(results[0]['url'], 'www.sxsw.com')
        self.assertEqual(results[0]['content'], 'This should be the content.')
