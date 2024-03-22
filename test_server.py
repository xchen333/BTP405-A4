import http
import unittest
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
import http.client
import json
import threading


class TestServerGET(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8000)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_get_method(self):
        # Connect to the server and send a GET request
        connection = http.client.HTTPConnection(*self.server_address)
        connection.request('GET', '/')
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        # check That the response as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data, {'message': 'This is a GET request response'})

    def test_post_method(self):
        # Connect to the server and send a POST request
        connection = http.client.HTTPConnection(*self.server_address)
        body = json.dumps({'message': 'This is a POST request'})
        connection.request('POST', '/', body)
        response = connection.getresponse()

        # Read and Decode the response
        response_data = response.read().decode()
        connection.close()

        # check That the response as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_json = json.loads(response_data)
        self.assertEqual(response_json, {'received': {'message': 'This is a POST request'}})


if __name__ == '__main__':
    unittest.main()
