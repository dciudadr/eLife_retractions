import modules.Article_object as Article_object


"""
article_test = Article_object.Article_object()

article_test.pmid = "11250748"

#assert article_test.journal == "Breast Cancer Res"
#assert article_test.pmc == "PMC13902"

article_test.describe()

article_test.get_pmc_and_journal_from_pmid()
print("\n After getting pmc and journal. Before get_text_from_tar_file_using_pmc")
article_test.describe()


article_test.get_text_from_tar_file_using_pmc()
print("\n After get_text_from_tar_file_using_pmc")
article_test.describe()
"""


print("-----------------------")



article_test2 = Article_object.Article_object()

print("doi of a retraction note: 10.1083/jcb.20070205310112013r")
article_test2.doi = "10.1083/jcb.20070205310112013r" #"10.1242/bio.20134671"

article_test2.describe()

article_test2.get_pmc_and_journal_from_doi()
print("\n After getting pmc and journal. Before get_text_from_tar_file_using_pmc")
article_test2.describe()


article_test2.get_text_from_tar_file_using_pmc()
print("\n After get_text_from_tar_file_using_pmc")
article_test2.describe()


article_test2.get_list_references_dois_from_text()
print("\n After get_list_references_dois_from_text")
article_test2.describe()



