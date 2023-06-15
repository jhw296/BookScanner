import cv2
import numpy as np
import pytesseract
from PIL import Image

def text_extraction():
    def draw_rect(img):
        rois = [(p - small, small * 2) for p in pts1]
        for (x, y), (w, h) in np.int32(rois):
            roi = img[y:y + h, x:x + w]
            val = np.full(roi.shape, 80, np.uint8)
            cv2.add(roi, val, roi)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 1)
        cv2.polylines(img, [pts1.astype(int)], True, (0, 255, 0), 1)
        cv2.imshow("Select Region", img)

    def warp(img):
        perspect_mat = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, perspect_mat, (500, 100), cv2.INTER_CUBIC)
        roi_image = img_contrast(dst)

        # 관심 영역(ROI)의 너비와 높이 계산
        roi_width = int(pts1[1][0] - pts1[0][0])
        roi_height = int(pts1[3][1] - pts1[0][1])

        # ROI 이미지 크기 조정
        resized_roi = cv2.resize(roi_image, (roi_width, roi_height))

        # cv2.imshow("Perspective Transform", dst)
        # cv2.imshow("Scanned Image", resized_roi)

        image_pdf = Image.fromarray(resized_roi)
        image_pdf = image_pdf.convert('RGB')
        # image_pdf.save('./scanned_image.pdf')

        text = pytesseract.image_to_string(resized_roi, lang='eng')
        print('스캔된 텍스트:')
        print(text)
        return text

    def img_contrast(img):
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        final = cv2.cvtColor(limg, cv2.COLOR_Lab2BGR)
        return final
    
    def scan_document(image_path):
        image = cv2.imread(image_path)
        draw_rect(np.copy(image))
        cv2.setMouseCallback("Select Region", onMouse)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def onMouse(event, x, y, flags, param):
        global check, s_button_pressed
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, p in enumerate(pts1):
                p1, p2 = p - small, p + small
                if contain_pts((x, y), p1, p2):
                    check = i

        if event == cv2.EVENT_LBUTTONUP:
            check = -1

        if check >= 0:
            pts1[check] = (x, y)
            draw_rect(np.copy(image))

    def contain_pts(p, p1, p2):
        return p1[0] <= p[0] < p2[0] and p1[1] <= p[1] < p2[1]

    small = np.array((12, 12))
    check = -1
    pts1 = np.float32([(100, 100), (300, 100), (300, 300), (100, 300)])
    pts2 = np.float32([(0, 0), (500, 0), (500, 100), (0, 100)])
    s_button_pressed = False

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow('Text Reader', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            image = frame
            s_button_pressed = True
            break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if s_button_pressed:
        image_path = './captured_image.png'
        # cv2.imwrite(image_path, image)
        scan_document(image_path)
        last_txt = warp(np.copy(image))
    return last_txt

# text_extraction()
