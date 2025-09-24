from bs4 import BeautifulSoup
import pandas as pd
import requests


# Jobstreet Scrapper scrap data from id.jobstreet.com domain with whatever jobs you want, and how much page you want
# output of this program is a csv file formatted "Output-jobname.csv"


class js_scrapper:
    def __init__(self, jobs:str = None):
        '''
        To call js_scrapper jobs name needed.

        Parameter :
        jobs : string (e.g. "Data Analyst")

        make sure there is no space after the string
        '''
        # what type of jobs searched
        # number of page searched
        jobs = jobs.lower()
        self.jobs = jobs.replace(" ", "-")
    
    def run_program(self, n_max: int = 100):
        '''
        
        '''
        # DATA STORED
        self.df_jobs_output = pd.DataFrame()

        # n Page
        n_page = 1
        while n_max >= n_page:
            url_address = f"https://id.jobstreet.com/id/{self.jobs}-jobs?page={n_page}&sortmode=ListedDate"
            html_text = requests.get(url_address).text
            soup = BeautifulSoup(html_text, 'html.parser')

            # Break condition : end_page 
            end_page = soup.find('h3', class_ = "kabgy40 _1nqfni150 _1nqfni1ig _17crjwd0 _17crjwdh _17crjwdm _1lwlriv4 _17crjwd1t")
            if end_page != None and end_page.text == "Tidak ada hasil pencarian yang sesuai":
                break

            # DEFINE JOB CARD
            list_pekerjaan = soup.find_all('article', class_= "kabgy40 kabgy41 _1nqfni198 _1nqfni18t _1nqfni184 _1nqfni17p _1nqfni1bg _1nqfni1b1 _1nqfni1ac _1nqfni19x _1nqfni1i _1nqfni16c _1nqfni15g _12pakdta _12pakdt8 _12pakdt9 _17crjwd10 _17crjwd13 _1nqfni134 _1nqfni137")

            # DATA COLLECTING
            for i in list_pekerjaan:
                jobs = i.find('h3', class_ = "kabgy40 _1nqfni150 _17crjwd0 _17crjwd3 _17crjwd1t _17crjwd8 _1lwlriv4")
                if jobs == None:
                    jobs_name = "Unknown Job"
                else:
                    jobs_name = jobs.text

                company = i.find('a', class_ = "kabgy40 kabgy4g kabgy48 kabgy40 kabgy4g kabgy48 _89zi40 _89zi41")
                if company == None:
                    company_name = "Anonimous Advertiser"
                else:
                    company_name = company.text
                
                location = i.find('span', class_ = "kabgy40 _1nqfni150 _17crjwd0 _17crjwd1 _17crjwd1t _17crjwd6 _1lwlriv4")
                if location == None:
                    location_name = "Unknown Location"
                else:
                    location_name = location.text
                
                new_df = pd.DataFrame([{"Jobs Name": jobs_name,
                                        "Company Name" : company_name,
                                        "Location" : location_name}])
                self.df_jobs_output = pd.concat([self.df_jobs_output, new_df], ignore_index= True)

            
            # NEXT PAGE
            n_page += 1

        # Error Catcher
        if len(self.df_jobs_output) == 0:
            raise ValueError("jobs not found")
    
    def export_data(self):
        '''
        Export Data to .CSV 
        Make sure to run_program first
        '''
        self.df_jobs_output.to_csv(f"Output-{self.jobs}.csv")




