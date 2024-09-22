from bs4 import BeautifulSoup
import requests
from contextlib import chdir
import os
# import re

def get_number_of_pages(full_text_id):
    print("Retrieving number of pages in scan...")
    url = f"https://babel.hathitrust.org/cgi/pt?id={full_text_id}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Response code 200. Parsing the HTML...")
        soup = BeautifulSoup(response.content, 'html.parser')
        output_group = soup.find('div', class_='bg-dark')
        script_tag = soup.find('script')

        # Get the JavaScript code within the script tag
        js_code = script_tag.string

        # Now, extract the value of "HT.params.totalSeq" from the JavaScript code
        total_seq_value = None
        lines = js_code.splitlines()
        for line in lines:
            if 'HT.params.totalSeq' in line:
                total_seq_value = line.split('=')[-1].strip().rstrip(';')
                break

        number_of_pages = int(total_seq_value)
        print(f"Number of pages found! Number of pages in scan: {number_of_pages}")
        return number_of_pages
    print(f"Response code not 200. Was: {response.status_code}")
    return None

def get_hathitrust_images(full_text_id, folder_path=None):
    # page_source = get_full_text_page_source(url)
    if type(full_text_id) == list:
        full_text_id = "/".join(full_text_id)
    number_of_pages = get_number_of_pages(full_text_id)
    print(f"Attempting to download the {number_of_pages} HathiTrust images from {full_text_id}...")
    
    if not folder_path:
        folder_path = f"Images_from_{full_text_id}"
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder path {folder_path} as it did not exist.")
    all_djvu_pages = "" # for merging djvu files in the end
    for page_num in range(1, number_of_pages+1):
        all_djvu_pages += f" {page_num}.djvu" # add page number to djvu for final command
        print(f"Attempting to download {page_num} of {number_of_pages}...")
        page_url_for_determining_bitonality = f"https://babel.hathitrust.org/cgi/imgsrv/image?id={full_text_id};seq={page_num};size=full"
        page_url = f"https://babel.hathitrust.org/cgi/imgsrv/image?id={full_text_id};seq={page_num};size=full;format=image/"
        while 1: # make SURE the image downloads.
            response = requests.get(page_url)
            if response.status_code == 200:
                # Save the image to the specified path
                image_path = os.path.join(folder_path, f"{page_num}")
                with open(image_path, 'wb') as file:
                    file.write(response.content)
                    print(f"Image for page #{page_num} saved successfully!")
                    break

            print(f"Failed to download the image file for page #{page_num}! Trying again...")
        while 1: # make SURE it finds the bitonality. This checks if image withour the format parameter is a jpeg or png. If image is jpeg, it means that it is either colored or greyscale; if it is png then it is bitonal. 
            response = requests.get(page_url_for_determining_bitonality)
            if response.status_code == 200:
                # Save the image to the specified path
                content_type = response.headers['content-type']
                oldpwd = os.getcwd()
                if content_type == "image/jpeg":
                    print(f"Color/greyscale detected! {page_num} is for c44")
                    os.chdir(f"{oldpwd}/{folder_path}/")
                    os.system(f"c44 -dpi 600 {page_num} {page_num}.djvu") # using default dpi settings because that's what ia-upload uses and it's what's recommended
                    # os.system(f"djvm -c finished_work.djvu {page_num}.djvu")
                    # os.remove(f"{page_num}") # delete pnm file to not let it take up storage
                    os.chdir(oldpwd)
                else:
                    print(f"Bitonality detected! {page_num} is for cjb2")
                    os.chdir(f"{oldpwd}/{folder_path}/")
                    os.system(f"cjb2 -dpi 600 {page_num} {page_num}.djvu") # using dpi 600 for bitonal images because they take up less storage and hathitrust images are 600 dpi
                    # os.system(f"djvm -c finished_work.djvu {page_num}.djvu")
                    # os.remove(f"{page_num}") # delete pnm file to not let it take up storage
                    os.chdir(oldpwd)
                break 
        
            print(f"Failed to determine the bitonality for #{page_num}! Trying again...")

    print(f"All images downloaded from Hathi scan {full_text_id}, converted to individual djvu files, and subsequently deleted successfully! Now to make one big djvu file")
    oldpwd = os.getcwd()
    os.chdir(f"{oldpwd}/{folder_path}/")
    os.system(f"djvm -c {full_text_id}.djvu{all_djvu_pages}")
    os.chdir(oldpwd)

    return None
    # return img_tags
# --------------------------------------------------------------------------------------------------------------------
# all of the above was copied from https://github.com/PseudoSkull/QuickTranscribe, with only slight modifications. I need to organize this better and make it handle files already downloaded. 
# --------------------------------------------------------------------------------------------------------------------
while True:
    full_text_id = input("Enter HathiTrust ID: ")
    directory = f"Images_from_{full_text_id}"
    options = input("Are the images already downloaded? [yN]")
    if options == "n" or options == "N":
        get_hathitrust_images(full_text_id)
        break
    
