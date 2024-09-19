from bs4 import BeautifulSoup
from contextlib import chdir
import requests
import subprocess
import os
import re
# array of page types that will determine if file recieves c44 or cjb2
pagetypes = []
def get_page_types(full_text_id, page_num):
    # page iterator, remember to subtract 1 for array
    page = 1
    while page <= pagenum:
        response = requests.get(f"https://babel.hathitrust.org/cgi/imgsrv/image?id={full_text_id};seq={page_num};size=full")
        soup = BeautifulSoup(response, "html.parser")
        if soup.find("image/jpeg"):
            pagetypes[page - 1] = "c44"
        else:
            pagetypes[page - 1] = "cjb2"
    return None
# front end
while true:
    pagetypes = []
    one = print("enter id: ")
    two = print("enter number of pages ")
    get_page_types(full_text_id, page_num):
    print(pagetypes)
    three = print("end the machine?"[yn])
    if three == "y":
        break
    
        
