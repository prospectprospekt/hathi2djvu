from bs4 import BeautifulSoup
import requests
from contextlib import chdir
import os
import math
# reqiires: cd to directory where images are going to be downloaded, and all inputs are strings
# modifies: print
# effects: downloads files, and possibly deletes them. 
def get_single_hathitrust_image(full_text_id, page_num, orientation):
  if orientation == "upright":  
    url_upright = f"https://babel.hathitrust.org/cgi/imgsrv/image?id={full_text_id};seq={page_num};size=full;format=image/png"
    while True:
      print("Getting page (upward orientation)")
      response = requests.get(url_upright)
      if response.status_code == 200:
        image_path = f"{page_num}_upright.png"
        with open(image_path, 'wb') as file:
          file.write(response.content)
        print(f"Upright image for #{page_num} saved successfully!")
        break
      print("Download failed. Trying again.")
  elif orientation == "upside down":
    url_upside_down = f"https://babel.hathitrust.org/cgi/imgsrv/image?id={full_text_id};seq={page_num};size=full;format=image/png;rotation=180"
    while True:
      print("Getting page (upside down orientation)")
      response = requests.get(url_upside_down)
      if response.status_code == 200:
        image_path = f"{page_num}_upside_down.png"
        with open(image_path, 'wb') as file:
          file.write(response.content)
        print(f"Upright image for #{page_num} saved successfully!")
        break
      print("Download failed. Trying again.")
def find_height(full_text_id, page_num):
  url = f"https://babel.hathitrust.org/cgi/imgsrv/image?id={full_text_id};seq={page_num};size=full;format=image/png"
  while True:
    response = requests.get(url)
    if response.status_code == 200:
      return response.headers['content-length']
      break
    print("didn't get height; trying again")
  
get_single_hathitrust_image("osu.32435055416200", "1", "upright")
get_single_hathitrust_image("osu.32435055416200", "1", "upside down")
print(find_height("osu.32435055416200", "1"))
