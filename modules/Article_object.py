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
                          
        
        
        try:
            mask = df_pmc_ids.PMID == self.pmid
            df_PMC_journal = df_pmc_ids[mask]
            df_PMC_journal = df_pmc_ids[mask][["PMCID", "Journal Title"]]
            self.pmc = df_PMC_journal.PMCID.iloc[0]
            self.journal = df_PMC_journal["Journal Title"].iloc[0]
        except IndexError:
            print("get_pmc_and_journal_from_pdmi did not find pcm and journal")
            return
        
 
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
        
        try:
            self.pmc = df_PMC_journal.PMCID.iloc[0]
            self.journal = df_PMC_journal["Journal Title"].iloc[0]    
        
        except IndexError:
            print("get_pmc_and_journal_from_doi did not find pcm and journal")
            return
        

##########################

   
    def get_text_from_tar_file_using_pmc(self):
        

        def list_tarfiles_to_check (journal):
            
            files_to_check = []
            
            try:
                    
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
               
            except IndexError:
                
                print("no journal defined")
                return files_to_check

        startTime = datetime.now()
        
        
        
        if (self.journal == "") or (self.journal == "Article not found"):
            print("journal not defined")
            list_tar_files = []
        else:
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
            try:
                reference_doi = reference.find('pub-id').text
                list_doi_references.append(reference_doi) 
                """
                Note that this is not just taking the doi, it could be anything under the pub-id tag such as pmid:
                You should do:
                
                reference_doi = reference.find('pub-id', {"pub-id-type": "doi"}).text
                list_doi_refernces.append (reference_doi)
                reference_pmid = reference.find('pub-id', {"pub-id-type": "pmid"}).text
                list_pmid_refernces.append (reference_pmid)
                
                or better save this a as list of dictionaries:
                
                reference_doi = reference.find('pub-id', {"pub-id-type": "doi"}).text
                reference_pmid = reference.find('pub-id', {"pub-id-type": "pmid"}).text
                reference_pmc = reference.find('pub-id', {"pub-id-type": "pmcid"}).text
                list_dictionary.append({"doi": reference_doi, "pmid": reference_pmid, "pmc": pmcid})
                 
                if not pub-id type = doi and pmid it will fail. COMPLETE CODE:
                
                
                %%%%%%%%%%%%%%%% HERE ####################
                def get_list_references_dois_from_text(self):
                    
                    list_dict_references_ids = []
                    list_dict_references_ids = []
                    
                    manuscript_BS = BeautifulSoup(str(self.text), "lxml") 
                
                    for reference in  manuscript_BS.find_all('ref'):
                        reference_doi = ""
                        reference_pmid = ""
                        
                        try:
                            reference_doi = reference.find('pub-id', {"pub-id-type": "doi"}).text
                        except AttributeError:
                            pass
                        
                        try:
                            reference_pmid = reference.find('pub-id', {"pub-id-type": "pmid"}).text
                        except AttributeError:
                            pass
                        
                        if reference_doi != "" or reference_pmid != "":
                            list_dict_references_ids.append({"doi": reference_doi, "pmid": reference_pmid})
                            #print(reference.find('pub-id', {"pub-id-type": "pmid"}))
                            
                    return list_dict_references_ids
                    
                   
                                
                """
            except AttributeError:
                pass
        
        self.references_dois = list_doi_references
        return
        
        
