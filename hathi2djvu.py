from bs4 import BeautifulSoup
import requests
import subprocess
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
    
    for page_num in range(1, number_of_pages+1):
        print(f"Attempting to download {page_num} of {number_of_pages}...")
        page_url = f"https://babel.hathitrust.org/cgi/imgsrv/image?id={full_text_id};seq={page_num};size=full"
        while 1: # make SURE the image downloads.
            response = requests.get(page_url)
            if response.status_code == 200:
                # Save the image to the specified path
                image_path = os.path.join(folder_path, f"{page_num}.jpg")
                with open(image_path, 'wb') as file:
                    file.write(response.content)
                    print(f"Image for page #{page_num} saved successfully!")
                    break

            print(f"Failed to download the image file for page #{page_num}! Trying again...")

    print(f"All images downloaded from Hathi scan {full_text_id} successfully!")

    return folder_path
    # return img_tags
# --------------------------------------------------------------------------------------------------------------------
# all of the above was copied from https://github.com/PseudoSkull/QuickTranscribe, with only slight modifications
# --------------------------------------------------------------------------------------------------------------------

full_text_id = input("Enter HathiTrust ID: ")
directory = f"Images_from_{full_text_id}"
options = input("Are the images already downloaded? [yN]")
if options == "n" or options == "N":
    get_hathitrust_images(full_text_id)
else:
    # begin the djvu conversion process
    start_conversion = input("Begin DjVu conversion? [yN]")
    if start_conversion == "y" or start_conversion == "Y":
        # subprocess.run(["mkdir", f"Converted_DjVu_files_of_{full_text_id}"])
        for root, dirs, files in os.walk(directory):
            for filename in files:
                print(filename) 
                filenamevariable = filename[:-4]
                print(filenamevariable)
   #             if filename.endswith(".jpg"):
                print("starting conversion")
                djvupage = f"{filenamevariable}.djvu"
                print(djvupage)
                name = f"Images_from_{full_text_id}/{filename}"
                truncated = name[:-4]
                last = f"{truncated}.pbm"
                subprocess.run(["convert", name, last])
                subprocess.run(["cjp2", "-dpi 300", last, djvupage])
                print("djvu conversion for this page successful!")
        djvuname = f"{full_text_id}.djvu"
        subprocess.run(["djvm", "-c", djvuname, "*.djvu"])
    else: 
        print("we respect your decision. Have a great rest of your day")

