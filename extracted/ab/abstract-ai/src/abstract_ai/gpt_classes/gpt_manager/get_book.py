from abstract_ocr import *
from abstract_utilities import *
images = '''/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/1.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/2.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/3.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/4.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/5.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/6.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/7.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/8.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/10.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/11.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/12.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/13.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/14.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/15.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/16.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/17.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/18.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/19.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/20.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/21.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/22.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/23.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/24.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/25.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/26.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/27.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/28.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/29.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/30.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/31.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/32.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/33.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/34.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/35.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/36.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/37.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/38.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/39.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/40.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/41.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/42.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/43.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/44.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/45.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/46.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/47.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/48.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/49.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/50.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/51.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/52.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/53.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/54.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/55.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/56.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/57.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/58.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/59.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/60.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/61.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/62.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/63.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/64.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/65.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/66.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/68.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/69.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/70.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/71.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/72.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/73.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/74.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/76.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/77.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/78.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/79.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/80.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/81.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/82.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/83.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/84.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/85.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/86.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/87.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/88.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/89.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/90.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/91.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/92.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/93.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/94.jpg
/home/computron/Desktop/downloaded_site/epsteinsblackbook.com/epsteinsblackbook.com/black-book-images/95.jpg'''
images = images.split('\n')
def is_number_in_text(text):
   for char in text:
       if is_number(char):
           return True
   return False
curr_dir = os.getcwd()
file_path = os.path.join(curr_dir,'the_names.json')
data=[]
for image in images:
    text = convert_image_to_text(image)
    texts = text.split('\n\n')
    for text in texts:
        for line in text.split('\n'):
            if line:
                if is_number_in_text(line):
                    if data ==[]:
                        data.append([])
                    data[-1].append(line)
                else:
                    data.append([line])
    safe_dump_to_file(data=data,file_path=file_path)
safe_dump_to_file(data=data,file_path=file_path)
