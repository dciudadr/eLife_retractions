import os
from io import BytesIO
import tarfile
# from tempfile import TemporaryDirectory
# from mock import patch

# import pytestcd


import Article_object as Article_object


#article_test = Article_object.Article_object()


class Test_Article_object_methods(object):                  
  
  

    
    def test_get_pmc_and_journal_from_pmid(self):
    
        article_test = Article_object.Article_object()
        article_test.pmid = "11056684"
        article_test.get_pmc_and_journal_from_pmid()           
        print(article_test.pmid, article_test.pmc)
        print(article_test.describe())
        assert article_test.journal == "Breast Cancer Res"
        assert article_test.pmc == "PMC13911"
  

        # doi = 10.1186/bcr29
        article_test = Article_object.Article_object()
        article_test.pmid = "kkk"
        article_test.get_pmc_and_journal_from_pmid()            
        print(article_test.pmid, article_test.pmc)
        print(article_test.describe())
        assert article_test.journal == ""
        assert article_test.pmc == ""
         
    
    

    def test_get_pmc_and_journal_from_doi(self):
        article_test = Article_object.Article_object()
        article_test.doi = "10.1186/bcr29"
        article_test.get_pmc_and_journal_from_doi()            
        print(article_test.doi, article_test.pmc)
        print(article_test.describe())
        assert article_test.journal == "Breast Cancer Res"
        assert article_test.pmc == "PMC13911"
    
        # doi = 10.1186/bcr29
        article_test = Article_object.Article_object()
        article_test.doi = "kkk"
        article_test.get_pmc_and_journal_from_doi()           
        print(article_test.doi, article_test.pmc)
        print(article_test.describe())
        assert article_test.journal == ""
        assert article_test.pmc == ""
        # doi = 10.1186/bcr29


    def test_get_text_from_tar_file_using_pmc(self):
        article_test = Article_object.Article_object()
        article_test.get_text_from_tar_file_using_pmc()
        assert article_test.pmc == ""
        
