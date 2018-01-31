import os
from io import BytesIO
import tarfile
from tempfile import TemporaryDirectory
from mock import patch

import pytest

import elife_retractions.extract_references as extract_references_module
from elife_retractions.extract_references import (
  extract_references_from_xml_bytes,
  extract_references_of_archived_document
)

PMID_1 = '12345'

def _add_tar_file_bytes(tf, name, data):
  tar_info = tarfile.TarInfo(name)
  tar_info.size = len(data)
  tf.addfile(tar_info, BytesIO(data))

class TestExtractReferencesFromXmlBytes(object):
  def test_should_return_empty_list_if_xml_does_not_contain_references(self):
    xml_bytes = b'<article></article>'
    assert extract_references_from_xml_bytes(xml_bytes) == []

  def test_should_return_list_with_references_from_xml_file(self):
    xml_bytes = (
      b'<article><back><ref-list>'
      b'<ref><pub-id pub-id-type="pmid">%s</pub-id></ref>'
      b'</ref-list></back></article>' %
      PMID_1.encode('utf-8')
    )
    assert extract_references_from_xml_bytes(xml_bytes) == [PMID_1]

  def test_should_not_include_pub_ids_with_type_other_than_pmid(self):
    xml_bytes = (
      b'<article><back><ref-list>'
      b'<ref><pub-id pub-id-type="other">%s</pub-id></ref>'
      b'</ref-list></back></article>' %
      PMID_1.encode('utf-8')
    )
    assert extract_references_from_xml_bytes(xml_bytes) == []

class TestExtractReferencesOfArchivedDocument(object):
  def test_should_return_raise_error_file_xml_file_does_not_exist(self):
    with TemporaryDirectory() as path:
      archive_filename = os.path.join(path, 'test.tar.gz')
      with tarfile.open(archive_filename, 'w') as tf:
        _add_tar_file_bytes(tf, 'dummy.xml', b'')
      os.sync()

      with pytest.raises(KeyError):
        extract_references_of_archived_document(
          archive_filename, 'test.xml'
        )

  def test_should_return_list_with_references_from_xml_file(self):
    xml_bytes = b'dummy'
    with patch.object(extract_references_module, 'extract_references_from_xml_bytes') as \
      extract_references_from_xml_bytes_mock:

      with TemporaryDirectory() as path:
        archive_filename = os.path.join(path, 'test.tar.gz')
        with tarfile.open(archive_filename, 'w') as tf:
          _add_tar_file_bytes(tf, 'test.xml', xml_bytes)
        os.sync()

        assert extract_references_of_archived_document(
          archive_filename, 'test.xml'
        ) == extract_references_from_xml_bytes_mock.return_value
        extract_references_from_xml_bytes_mock.assert_called_with(xml_bytes)
