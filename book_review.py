import cv2
from pyzbar.pyzbar import decode
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    # 바코드 인식
    barcodes = decode(frame)

    # 인식된 바코드가 있는 경우
    if len(barcodes) > 0:
        # 바코드 데이터 출력
        barcode_data = barcodes[0].data.decode("utf-8")
        print("Barcode data:", barcode_data)

        # ISBN 바코드인 경우 (978, 979로 시작하는 13자리 숫자)
        if (barcode_data.startswith("978") or barcode_data.startswith("979")) and len(barcode_data) == 13:
            isbn = barcode_data
            key = os.environ.get('key')
            url = f"https://www.nl.go.kr/NL/search/openApi/search.do?key={key}&detailSearch=true&isbnOp=isbn&isbnCode={isbn}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser') # html 파일
            
            title = soup.find('title_info').text

            if title is None:
                title = "Not Found"
            else:
                print("Title: ", title)
        else:
            print("Not an ISBN barcode")

    cv2.imshow('Barcode reader', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
