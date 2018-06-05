import requests
import json
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from google.cloud import dns
from google.cloud.exceptions import Conflict


class MetaDataServer():
    def __init__(self):
        self.project_id = self.get_info('project/project-id')
        self.service_account = self.get_info(
                'instance/service-accounts/default/email'
                )
        self.name = self.get_info('instance/name')
        self.primary_ip = self.get_info(
                'instance/network-interfaces/0/ip')

    def get_info(self, path):
        headers = {'Metadata-Flavor': 'Google'}
        baseurl = 'http://metadata.google.internal/computeMetadata/v1'
        url = f'{baseurl}/{path}'
        req = requests.get(url, headers=headers)
        return req.text

    def get_auth_token(self):
        token = self.get_info('instance/service-accounts/default/token')
        return json.loads(token)['access_token']


class GCE():
    def __init__(self):
        self.metadata = MetaDataServer()
        engine = get_driver(Provider.GCE)
        self.driver = engine(
                '',
                '',
                project=self.metadata.project_id
                )


class DNSUpdater():
    def __init__(self, project, domain):
        self.client = dns.Client(project=project)
        if not domain.endswith('.'):
            domain = '{}.'.format(domain)
        try:
            self.zone = [
                        z for z in self.client.list_zones()
                        if z.dns_name == domain
                      ][0]
        except IndexError:
            self.zone = None

    def get_records(self):
        entries = {
                r.name: r.rrdatas
                for r in self.zone.list_resource_record_sets()
                if r.record_type == 'A'
                }
        return entries

    def insert_record(self, record):
        change = self.zone.changes()
        change.add_record_set(record)
        change.create()

    def delete_record(self, record):
        change = self.zone.changes()
        change.delete_record_set(record)
        change.create()

    def update_record(self, name, ip, ttl=300):
        record = self.zone.resource_record_set(name, 'A', ttl, [ip])
        try:
            self.insert_record(record)
        except Conflict:
            old_record = [
                    r for r in self.zone.list_resource_record_sets()
                    if r.name == name][0]
            self.delete_record(old_record)
            self.insert_record(record)



