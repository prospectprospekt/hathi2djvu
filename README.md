# hathi2djvu

# Hathitrust-image-downloader
A program to download images from hathitrust (WIP). The hathitrust downlodaer was copied from quicktranscribe. 
To use this application you need both requests and beautifulsoup4. see https://requests.readthedocs.io/en/latest/user/install/#install and https://www.crummy.com/software/BeautifulSoup/
and djvulibre lmao

;format=image%2Ftiff
;format=image%2Ftiff

Trying to figure out how to get the original images from hathitrust. https://babel.hathitrust.org/cgi/imgsrv/image?id={full_text_id};seq={page_num};size=full produces png images when the text is bitonal and jpeg images when the text is either greyscale or colored, determined by metadata. https://babel.hathitrust.org/cgi/imgsrv/image?id={full_text_id};seq={page_num};size=full;format=image%2Ftiff produces bitonal tiff files converted from pnm files and also colored files, depending on type of page. You can also download jp2 and ppm files, which is interesting. osu.32435055416200

For example: 
https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=1;size=full -- jpeg file
https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=1;size=full;format=image%2Ftiff -- original scan? 
https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=14;size=full;format=image%2Fjp2
https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=14;size=full;format=image%2Fpnm
https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=1;size=full;format=image%2Fppm
https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=1;size=full;format=image%2Fpbm
https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=14;size=full;format=image%2Fpbm

https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=14;size=full;format=image/jp2
https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=14;size=full;format=image/tiff

https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=14;size=full;format=image/ - will just return pgm?????
https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=1;size=full;format=image/  - ppm????
https://babel.hathitrust.org/cgi/imgsrv/image?id=osu.32435055416200;seq=20;size=full;format=image/

see also https://github.com/hathitrust/feed_no_history

https://github.com/hathitrust/imgsrv/blob/dee475f42ea20e8718c8587bb2dcf763ccf3beed/bin/image
