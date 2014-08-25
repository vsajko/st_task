from django.test import TestCase


class SummerViewsTestCase(TestCase):
    def test_list(self):
        resp = self.client.get('/summer/list/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('channels' in resp.context)

    def test_add_channel(self):
        resp = self.client.get('/summer/add_channel/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)

    def test_toplist(self):
        resp = self.client.get('/summer/toplist/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('words' in resp.context)

    def test_change_feed_status(self):
        resp = self.client.get('/summer/change_feed_status/')
        self.assertEqual(resp.status_code, 302)

    def test_rijec(self):
        resp = self.client.get('/summer/rijec/')
        self.assertEqual(resp.status_code, 200)


