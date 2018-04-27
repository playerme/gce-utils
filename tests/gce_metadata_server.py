import gceutils


def test_get_info():
    metadata = gceutils.MetaDataServer()
    assert metadata.get_info('project/project-id') == "budega"
