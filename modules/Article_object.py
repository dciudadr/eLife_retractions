import pandas as pd
import tarfile
import re
import string

import datetime
#from datetime import datetime
from bs4 import BeautifulSoup


class Article_object(object):
    
    def __init__(self):
        self.text = ""
        self.journal = ""
        self.pmc = ""
        self.pmid = ""
        self.doi = ""
        self.references_dois = ""
        self.date = ""
    
    def describe(self):
        print("pmc: \t", self.pmc, 
              "\npmid: \t", self.pmid,  
              "\ndoi: \t", self.doi,
              "\njournal: \t", self.journal,
              "\ndate: \t", self.date,
              "\ntext: \t", self.text[:100],
              "\nreferences_dois: \t", self.references_dois
              )

    def get_pmc_and_journal_from_pmid(self):
        

        """
        DEPRECATED - USED in Retractionwatch notebook. 
        Use get_pmc_doi_and_journal_from_pmid instead.
        """
        
        if self.pmid == "": 
            print("PMID not defined in object")
            return
        
        try:
            df_pmc_ids = pd.read_csv('./data/PMC_ids/PMC-ids.csv', 
                         sep=',', 
                         encoding='utf-8',
                         low_memory=False
                         )
        except FileNotFoundError:
            print("./data/PMC_ids/PMC-ids.csv not found")
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
    
    
    def get_pmc_doi_and_journal_from_pmid(self):
    
    
        if self.pmid == "": 
            print("PMID not defined in object")
            return
    
        try:
            df_pmc_ids = pd.read_csv('./data/PMC_ids/PMC-ids.csv', 
                         sep=',', 
                         encoding='utf-8',
                         low_memory=False
                         )
        except FileNotFoundError:
            print("./data/PMC_ids/PMC-ids.csv not found")
            return
    
        df_pmc_ids.PMID = df_pmc_ids.PMID.apply(lambda x: str(x)[:-2])
    
    
    
        try:
            mask = df_pmc_ids.PMID == article.pmid
            df_PMC_journal = df_pmc_ids[mask]
            df_PMC_journal = df_pmc_ids[mask][["PMCID", "DOI", "Journal Title"]]
            article.pmc = df_PMC_journal.PMCID.iloc[0]
            article.journal = df_PMC_journal["Journal Title"].iloc[0]
            article.doi = df_PMC_journal.DOI.iloc[0]
        except IndexError:
            print("get_pmc_and_journal_from_pdmi did not find pcm and journal")
            return

 
 
 

 ########################       
    
    def get_pmc_and_journal_from_doi(self):
        
        if self.doi == "": 
            print("DOI not defined in object")
            return
        
        try:
            df_pmc_ids = pd.read_csv('./data/PMC_ids/PMC-ids.csv', 
                         sep=',', 
                         encoding='utf-8',
                         low_memory=False
                         )
        except FileNotFoundError:
            print("./data/PMC_ids/PMC-ids.csv not found")
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

        startTime = datetime.datetime.now()
        
        
        
        if (self.journal == "") or (self.journal == "Article not found"):
            print("journal not defined")
            list_tar_files = []
        else:
            list_tar_files = list_tarfiles_to_check(self.journal)
            

       
        for file in list_tar_files:
            file_path = './data/' + file
            print("Checking: ", file_path)
    
            tar = tarfile.open(file_path, "r:gz")
              
            for filename in tar:
                if re.search(self.pmc, filename.name) != None:
                    print("Article found: ", filename.name)
                    paper = tar.extractfile(filename)
                    self.text = paper.read()
                    print("Search total time = ",  datetime.datetime.now() - startTime )
                    return
            tar.close()
            
            
            print("Search total time = ",  datetime.datetime.now() - startTime )
        

        self.text = "Article not found" 

        return 
    

    def get_list_references_dois_from_text(self):
        

        """
        DEPRECATED - USED in Retractionwatch notebook. 
        Use get_list_references_dois_and_pmids_from_text instead.
        """
        
        list_doi_references = []
        
        manuscript_BS = BeautifulSoup(str(self.text), "lxml") 
        
        for reference in  manuscript_BS.find_all('ref'):
            try:
                reference_doi = reference.find('pub-id').text
                list_doi_references.append(reference_doi) 

            except AttributeError:
                pass
        
        self.references_dois = list_doi_references
        return
    
    """
    get_list_references_dois_from_text:
    
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
     
    if not pub-id type = doi and pmid it will fail. 
    
    COMPLETE CODE get_list_references_dois_and_pmids_from_text
    
                    
    """
        
    def get_list_references_dois_and_pmids_from_text(self):
        
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
        
###############################################################################               
               
    def get_date_from_text(self):
              
        manuscript_BS = BeautifulSoup(str(self.text), "lxml")
        
        try:
            
            for day in  manuscript_BS.find('day'):
                #print("day: ", day)
                day_publication = day
            for month in manuscript_BS.find('month'):
                #print("month: ", month)
                month_publication = month
            for year in manuscript_BS.find('year'):
                #print("year: ", year)
                year_publication = year
            
            self.date = datetime.date(int(year_publication), int(month_publication), int(day_publication))  #year, month, day


        except TypeError:
            print("Date not found")
        
        except ValueError:
            print("Day or month out of range!!!")
            print("day: ", str(day_publication), "month: ", str(month_publication), "year: ", str(year_publication))
            try:
                # Some articles have dates such as 31/11/2010 !!!!
                day_publication = 29
                self.date = datetime.date(int(year_publication), int(month_publication), int(day_publication))  #year, month, day
                print("Date set to: ")
                print("day: ", str(day_publication), "month: ", str(month_publication), "year: ", str(year_publication))
            except:
                pass
            



##############################################################################

    """
    Addapted from ind_section.py
    
    .doi
    	Finds DOI.
    
    """


    def get_doi_from_text(self):
        
        manuscript_BS = BeautifulSoup(str(self.text), "lxml")

        if self.doi != "":
            print("Article already has a doi asigned.")
            return
        
        for sub_heading in manuscript_BS.find_all("front"):
            doi_section = sub_heading.find_all("article-id", {"pub-id-type":"doi"})
            
    
            if doi_section != []: #is not None:
                doi_section_BS = BeautifulSoup(str(doi_section[0]), "lxml")
                doi =  doi_section_BS.text.strip()
                self.doi = doi
                return
        
            if manuscript_BS.find_all("article-id", {"pub-id-type":"doi"}) != []: #None:
                doi_section = manuscript_BS.find_all("article-id", {"pub-id-type":"doi"})
                if doi_section != []: #is not None: 
                    doi_section_BS = BeautifulSoup(str(doi_section[0]), "lxml")
                    doi = doi_section_BS.text.strip()
                    self.doi =  doi
                    return
    
        print("DOI not found")
    #else:
    #    return  doi_section_BS.text
    
    ##### The following code works in jupyter notebook, but not in the module!!!
    # manuscript_BS = BeautifulSoup(text, "lxml")
    # front_part =  manuscript_BS.front
    # doi_section = front_part.find_all("article-id", {"pub-id-type":"doi"})
    # doi_section_BS = BeautifulSoup(str(doi_section[0]), "lxml")
    # return doi_section_BS.text

    def get_pmid_from_text(self):
        
        #for reference in  manuscript_BS.find_all('ref'):
        
        manuscript_BS = BeautifulSoup(self.text, "lxml")
        
        
        pmid_section = manuscript_BS.find_all("pub-id", {"pub-id-type":"pmid"})
        #print("pmid:  ", str(pmid_section))
        if len(pmid_section) > 0:
            pmid_section_BS = BeautifulSoup(str(pmid_section[0]), "lxml")
            pmid = pmid_section_BS.text.strip()
            self.pmid =  pmid
            return
    
        print("PMID not found")
        
        
        
    












            
#=======
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
                    
                   
                                

            except AttributeError:
                pass
        
        self.references_dois = list_doi_references
        return
"""        
        

