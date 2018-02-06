import pandas as pd
import tarfile
import re
import string
from datetime import datetime
from bs4 import BeautifulSoup


class Article_object(object):
    
    def __init__(self):
        self.text = ""
        self.journal = ""
        self.pmc = ""
        self.pmid = ""
        self.doi = ""
        self.references_dois = ""
    
    def describe(self):
        print("pmc: \t", self.pmc, 
              "\npmid: \t", self.pmid,  
              "\ndoi: \t", self.doi,
              "\njournal: \t", self.journal,
              "\ntext: \t", self.text[:100],
              "\nreferences_dois: \t", self.references_dois
              )

    def get_pmc_and_journal_from_pmid(self):
        
        if self.pmid == "": 
            print("PMID not defined in object")
            return
        
        try:
            df_pmc_ids = pd.read_csv('/project/eLife_retractions/data/PMC_ids/PMC-ids.csv', 
                         sep=',', 
                         encoding='utf-8',
                         low_memory=False
                         )
        except FileNotFoundError:
            print("/project/eLife_retractions/data/PMC_ids/PMC-ids.csv not found")
            return
            
        df_pmc_ids.PMID = df_pmc_ids.PMID.apply(lambda x: str(x)[:-2])
                          
        mask = df_pmc_ids.PMID == self.pmid
        
        df_PMC_journal = df_pmc_ids[mask]
        print(df_PMC_journal)
        
        df_PMC_journal = df_pmc_ids[mask][["PMCID", "Journal Title"]]
        
        self.pmc = df_PMC_journal.PMCID.iloc[0]
        self.journal = df_PMC_journal["Journal Title"].iloc[0]
 
 
 ########################       
    
    def get_pmc_and_journal_from_doi(self):
        
        if self.doi == "": 
            print("DOI not defined in object")
            return
        
        try:
            df_pmc_ids = pd.read_csv('/project/eLife_retractions/data/PMC_ids/PMC-ids.csv', 
                         sep=',', 
                         encoding='utf-8',
                         low_memory=False
                         )
        except FileNotFoundError:
            print("/project/eLife_retractions/data/PMC_ids/PMC-ids.csv not found")
            return
            
        
        mask = df_pmc_ids.DOI == self.doi
        
        df_PMC_journal = df_pmc_ids[mask]
        print(df_PMC_journal)
        
        df_PMC_journal = df_pmc_ids[mask][["PMCID", "Journal Title"]]
        
        self.pmc = df_PMC_journal.PMCID.iloc[0]
        self.journal = df_PMC_journal["Journal Title"].iloc[0]    



##########################

   
    def get_text_from_tar_file_using_pmc(self):
        
        import string

        def list_tarfiles_to_check (journal):
            
            journal = journal.lower()
            initial_letter = journal[0]
            letter_index = string.ascii_lowercase.index(initial_letter)
        
            # A-B
            if letter_index <= 1:
                files_to_check = ["comm_use.A-B.xml.tar.gz", "non_comm_use.A-B.xml.tar.gz"]
            # C-H
            if (2 <= letter_index) & (letter_index <= 7):
                files_to_check = ["comm_use.C-H.xml.tar.gz", "non_comm_use.C-H.xml.tar.gz"]
        
            # I-N
            if (8 <= letter_index) & (letter_index <= 13):
                files_to_check = ["comm_use.I-N.xml.tar.gz", "non_comm_use.I-N.xml.tar.gz"]
        
            # O-Z
            if (14 <= letter_index) & (letter_index <= 25):
                files_to_check = ["comm_use.O-Z.xml.tar.gz", "non_comm_use.O-Z.xml.tar.gz"]
        
            return files_to_check
    
        
        startTime = datetime.now()
       
        list_tar_files = list_tarfiles_to_check(self.journal)
       
        for file in list_tar_files:
            file_path = '/project/data/' + file
            print("Checking: ", file_path)
    
            tar = tarfile.open(file_path, "r:gz")
              
            for filename in tar:
                if re.search(self.pmc, filename.name) != None:
                    print("Article found: ", filename.name)
                    paper = tar.extractfile(filename)
                    self.text = paper.read()
                    print("Search total time = ",  datetime.now() - startTime )
                    return
            tar.close()
            
            
            print("Search total time = ",  datetime.now() - startTime )
        
        self.text = "Article not found" 
        return 
    

    def get_list_references_dois_from_text(self):
        
        list_doi_references = []
        
        manuscript_BS = BeautifulSoup(str(self.text), "lxml") 
        
        for reference in  manuscript_BS.find_all('ref'):
            reference_doi = reference.find('pub-id').text
            list_doi_references.append(reference_doi)
            
        self.references_dois = list_doi_references
        return
        
        
