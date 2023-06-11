import cv2
import requests
import os
import numpy as np
import pytesseract
from pyzbar.pyzbar import decode
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from PIL import Image

global title, author, isbn, publisher, pubdata, discount, description, image_url
title = None
author = None
isbn = None
publisher = None
pubdata = None 
discount = None 
description = None
image_url = None

def barcorde_recognition():
    global title, author, isbn, publisher, pubdata, discount, description, image_url
    load_dotenv()
    barcode_cnt = 0
    
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = decode(gray) # 바코드 인식

        for barcode in barcodes:
            barcode_cnt += 1
            x, y, w, h = barcode.rect
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            barcode_text = '%s (%s)' % (barcode_data, barcode_type)
            # print("Barcode data:", barcode_data)
            
            # barcode bounding box 생성
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(frame, barcode_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

            # ISBN 바코드인 경우 (978, 979로 시작하는 13자리 숫자)
            if (barcode_data.startswith("978") or barcode_data.startswith("979")) and len(barcode_data) == 13:
                isbn = barcode_data
                id = os.environ.get('clientId')
                secret = os.environ.get('clinetSecret')
                headers = {
                    "X-Naver-Client-Id": id,
                    "X-Naver-Client-Secret": secret
                }
                url = f"https://openapi.naver.com/v1/search/book_adv.json?d_isbn={isbn}"
                response = requests.get(url, headers=headers)
                data =  response.json()
                
                if "items" in data:
                    items = data["items"]
                    if items:
                        title = items[0]["title"]
                        author = items[0]["author"]
                        publisher = items[0]["publisher"]
                        pubdata = None #items[0]["pubdata"]
                        discount = items[0]["discount"]
                        description = items[0]["description"]
                        image_url = items[0]["image"]
                    else:
                        title = "Not Found"
                        print("Not Found")
                        
                # 바코드가 지속적으로 10번 이상 감지될 경우 해당 도서 정보 출력
                if barcode_cnt >= 10:
                    # path = './img/snapshot_' + str(title) + '.jpg'
                    # cv2.imwrite(path, frame)
                    cap.release()
                    book_info()
                    
            else:
                print("Not an ISBN barcode")

        cv2.imshow('Barcode reader', frame)
        # cv2.imshow('grayscale', gray) 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def book_info():
    global title, author, isbn, publisher, pubdata, discount, description, image_url
    # print("Title: ", title)
    # print("Author: ", author)
    
    return title, author, isbn, publisher, pubdata, discount, description, image_url
