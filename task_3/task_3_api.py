from json import loads, dumps
from typing import Callable
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults

from task_3 import appearance


class Application:
    """
    Small WSGI application made with the help of WSGIRef library
    """

    def __call__(self, environment: dict, start_response: Callable) -> list:
        """
        Handles the POST-request to the /api/ address. Extracts the data
        from the request and then uses the "appearance" method to process
        this data. Returns the result in json format.

        :param environment: dictionary with environment variables
        :param start_response: response handler
        :return: list with bytes
        """
        setup_testing_defaults(environment)
        path = environment['PATH_INFO']
        if path == '/api/':
            data = self.get_wsgi_input_data(environment)
            result = appearance(loads(data))
            result_str = dumps(result)
            body = [result_str.encode('utf-8')]
            start_response('200 OK', [('Content-Type', 'application/json')])
            return body
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'PAGE NOT FOUND']

    @staticmethod
    def get_wsgi_input_data(environment: dict) -> str:
        """
        Retrieves the data from the wsgi.input field of a POST-request.

        :param environment: dictionary with all the data
        :return: decoded string with data
        """
        query_content_length = environment.get('CONTENT_LENGTH')
        content_length = int(
            query_content_length) if query_content_length else 0
        data = environment['wsgi.input'].read(content_length) \
            if content_length > 0 else b''
        return data.decode('utf-8')


if __name__ == '__main__':
    app = Application()

    with make_server('127.0.0.1', 7777, app) as httpd:
        print('Running test server on port 7777...')
        httpd.serve_forever()
