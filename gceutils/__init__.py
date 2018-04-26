import requests
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


class MetaDataServer():
    def __init__(self):
        self.project_id = self.get_info('project/project_id')

    def get_info(self, path):
        headers = {'Metadata-Flavor': 'Google'}
        baseurl = 'http://metadata.google.internal/computeMetadata/v1'
        url = f'{baseurl}/{path}'
        req = requests.get(url, headers=headers)
        return req.text


class GCE():
    def __init__(self):
        self.metadata = MetaDataServer()
        engine = get_driver(Provider.GCE)
        self.driver = engine(
                '',
                '',
                project=self.get_project()
                )

    def get_project(self):
        pass
