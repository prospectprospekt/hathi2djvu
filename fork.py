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
    while page <= page_num:
        response = requests.get(f"https://babel.hathitrust.org/cgi/imgsrv/image?id={full_text_id};seq={page_num};size=full")
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.find("image/jpeg"):
            pagetypes.append("c44")
        else:
            pagetypes.append("cjb2")
        page += 1
    return None
# front end
while True:
    pagetypes = []
    one = input("enter id: ")
    two = int(input("enter number of pages "))
    get_page_types(one, two)
    print(pagetypes)
    three = print("end the machine?"[yn])
    if three == "y":
        break
    
        
