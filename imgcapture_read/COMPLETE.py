from selenium import webdriver
from urllib.request import urlretrieve
from PIL import Image
import pytesseract
import requests
import re
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen as uOp

pytesseract.pytesseract.tesseract_cmd = (r"C:\Program Files\Tesseract-OCR\Tesseract.exe")

class Fill_Req():
    DL = ''
    DOB = ''
    driver = webdriver.Chrome()
    url = "https://parivahan.gov.in/rcdlstatus/?pur_cd=101"
    driver.get(url)


    def __init__(self,DL,DOB):
        self.DL = DL
        self.DOB = DOB

    def get_captcha(self):

        try:
            captcha = self.driver.find_element_by_xpath("""//*[@id="form_rcdl:j_idt34:j_idt41"]""")
            src = captcha.get_attribute('src')
            urlretrieve(src, "captcha.png")
            image_new = Image.open("captcha.png")
            text_img = pytesseract.image_to_string(image_new, lang='eng', config='--psm 10 --oem 3').strip().lower()
            Captcha = re.sub(r'[^a-zA-Z0-9)]', "", text_img)
            print(Captcha)

            if len(Captcha) == 5:
                return Captcha
        except:
            raise Exception("Wrong Captcha Code Please Try Again!")

    def fill(self):
        try:
            self.driver.maximize_window()
            DL = self.DL
            DOB = self.DOB
            code = self.get_captcha()

            self.driver.find_element_by_id('form_rcdl:tf_dlNO').send_keys(DL)
            self.driver.find_element_by_id('form_rcdl:tf_dob_input').send_keys(DOB)
            self.driver.find_element_by_id('form_rcdl:j_idt34:CaptchaID').send_keys(code)
            self.driver.find_element_by_id('form_rcdl:j_idt46').click()
            # new_url=self.driver.current_url()
            # return new_url

        except:
            raise Exception("Captcha not found please re-run the code!")


if __name__ == '__main__':
    # dl = input("Enter the Driving Licence No. : ")
    dl = 'DL-0420110149646'
    dob = '09-02-1976'
    # dob = input("Enter the Date of Birth : ")
    FA = Fill_Req(dl,dob)
    FA.get_captcha()
    FA.fill()
    FA.get_data()
