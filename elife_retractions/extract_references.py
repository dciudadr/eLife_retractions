from io import BytesIO
import tarfile

from lxml import etree

def extract_references_from_xml_bytes(xml_bytes):
  xml_root = etree.parse(BytesIO(xml_bytes))
  refs = xml_root.xpath('.//ref/pub-id[@pub-id-type="pmid"]')
  return [ref.text for ref in refs]

def extract_references_of_archived_document(archive_filename, xml_filename):
  with tarfile.open(archive_filename) as tf:
    with tf.extractfile(xml_filename) as xml_f:
      xml_f.seek(0)
      xml_bytes = xml_f.read()
      return extract_references_from_xml_bytes(xml_bytes)
