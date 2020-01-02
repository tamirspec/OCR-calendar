from pytesseract import pytesseract
from Main.image_reader import Image
import re

class Image_processor():
    def __init__(self, image):
        self.image = image

    def get_size(self):
        size = self.image.getbbox()
        return size

    def image_to_string(self):
        text = pytesseract.image_to_string(self.image)
        text = self.text_editor(text)
        return text

    def image_to_location(self):
        image = self.image
        location_text = pytesseract.image_to_boxes(image)
        row_list = location_text.split('\n')
        location_dict_list = []
        for specific_row in row_list:
            line = specific_row.split(' ')
            location_dict = {'letter':line[0],
                        'x':line[1],
                        'y':line[2],
                        'z':line[3],
                        'n': line[4]}
            location_dict_list.append(location_dict)
        return location_dict_list

    def text_editor(self,text): #to improve to perfect discription
        remove_signs = '!@#$%^&*~<>|'
        for sing in remove_signs:
            text = text.replace(sing,'')
        text = text.replace('\n\n' ,'\n')
        return text

    def convert_date_to_google_format(self,date_list):
        for place in enumerate(date_list):
            if place[0] == 2:
                if len(place[1]) < 4:
                    date_list[place[0]] = f'20{date_list[place[0]]}'

            elif int(date_list[place[0]]) < 10 and len(date_list[place[0]])<2:
                date_list[place[0]] = f'0{date_list[place[0]]}'

        google_format_date = f'{date_list[2]}-{date_list[0]}-{date_list[1]}T00:00:00%s'
        return google_format_date

    def get_formated_google_date(self):
        text = self.image_to_string()
        date = re.findall('[0-9]{1,2}[-|.\/]{1}[0-9]{1,2}[-|.\/]{1}[\d]{2,4}',text) #to fix for all dates
        sepreters = '/\._'
        date_list = []
        for speratre in sepreters:
            if speratre in date[0]:
                date_list = date[0].split(speratre)
                break
        google_date = self.convert_date_to_google_format(date_list)
        return google_date
    # def get_date_verbal(self):
