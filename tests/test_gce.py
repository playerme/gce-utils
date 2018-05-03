from unittest import mock
from gce import MetaDataServer


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

    if args[0] == 'http://metadata.google.internal/computeMetadata/v1/project/project-id':
        return MockResponse('budega', 200)
    else:
        return MockResponse(None, 404)


@mock.patch('gce.core.requests.get', side_effect=mocked_requests_get)
def test_get_info(*args, **kwargs):
    metadata = MetaDataServer()
    assert metadata.get_info('project/project-id') == "budega"
