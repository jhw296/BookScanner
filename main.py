import cv2
import requests
import os
import numpy as np
import barcode_recognition as barR
import text_extraction as txtE
# import pytesseract import Output
import pytesseract
from pyzbar.pyzbar import decode
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from PIL import Image


def main():
    # barR.barcorde_recognition()
    txtE.text_extraction()
    
if __name__ == '__main__':
    main()
