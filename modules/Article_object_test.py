import os
from io import BytesIO
import tarfile
# from tempfile import TemporaryDirectory
# from mock import patch

# import pytestcd


import Article_object as Article_object


article_test = Article_object.Article_object()



class Test_Article_object_methods(object):                  # What's the meaning of (object) here?
  def test_get_pmc_and_journal_from_pmid():
    article_test.pmid = "11250748"
    article_test.get_pmc_and_journal_from_pmid()            # The method is not running, but it does not fail the assertion!!!! I don't get it.
    print(article_test.pmid, article_test.pmc)
    print(article_test.describe())
    assert article_test.journal == "Breast Cancer Res"
    assert article_test.pmc == "PMC13902"
