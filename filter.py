from dataclasses import dataclass

@dataclass
class geo_obj:
    accession: str 
    title: str
    submission_date : str
    number_of_samples : int
    summary : str
    overall_design : str
    ftp : str
    author : str
    supplementary_information : dict
    index : int  


