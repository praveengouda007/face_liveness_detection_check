import cv2
from .f_liveness_detection import detect_liveness
import cv2
import numpy as np
import imutils
import time
from face_liveness_detection import config as cfg
# from face_anti_spoofing import Liveness_Api

def bounding_box(img, box, match_name=[]):
    # import pdb; pdb.set_trace()
    for i in np.arange(len(box)):
        x0, y0, x1, y1 = box[i]
        img = cv2.rectangle(img,
                      (x0,y0),
                      (x1,y1),
                      (0,255,0),3);
        if not match_name:
            continue
        else:
            pass
            # cv2.putText(img, match_name[i], (x0, y0-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
    return img


# initializing blink count
COUNTER, TOTAL = 0, 0
input_type = "webcam"

# Image
if input_type == "image":
    i=2
    list_images = ["none.jpg", "praveen.jpg", "friends1.JPEG"]
    im = cv2.imread("data_test/"+list_images[i])
    im = imutils.resize(im, width=720)

    out = detect_liveness(im, COUNTER, TOTAL)
    print(out)

    boxes = out['box_face_frontal']+out['box_orientation']
    tags = out['emotion']+out['orientation']

    res_img = bounding_box(im, boxes, tags)
    cv2.imshow("liveness_detection", res_img)
    cv2.waitKey(0)

# Video
def checking_liveness(video, selfie_name):
    # import pdb; pdb.set_trace()
    COUNTER, TOTAL = 0, 0
    l = []
    m = []
    n = []
    temp = ''

    if input_type == "webcam":
        # cv2.namedWindow("preview")

        cam = cv2.VideoCapture(video)
        ret, frame = cam.read()
        init_time = time.time()
        while True:
            start_time = time.time()
            ret, im = cam.read()
            try:
                im = imutils.resize(im, width=720)
            except:
                return 'Fake'
            act_im = im.copy()

            # enter data stream
            out = detect_liveness(im, COUNTER, TOTAL)
            boxes = out['box_face_frontal']+out['box_orientation']
            tags = out['emotion']+out['orientation']
            TOTAL = out['total_blinks']
            l.extend(out['orientation'])
            if len(out['orientation']) == 0:
                l.extend(['neutral'])
            m.extend([out['total_blinks']])
            n.extend(out['emotion'])
            COUNTER = out['count_blinks_consecutives']
            res_img = bounding_box(im, boxes, tags)  # called bounding_box function
            # end_time = time.time() - start_time
            # FPS = 1/end_time
            cv2.putText(res_img, temp,(10,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            if (time.time()-init_time)>10:
                if (len(set(m))>1) or ((len(set(n))>1) and (len(set(l))>1)):
                    temp = 'Real'
                    box = out['box_face_frontal'][0]
                    crop_img = act_im[box[1]-30:box[3]+30,box[0]-30:box[2]+30]
                    cv2.imwrite(cfg.selfie_path+'\\'+selfie_name+'.png',crop_img)
                    init_time =time.time()
                    l=[]
                    m=[]
                    n=[]
                    break
                else:
                    temp = 'Fake!'
                    init_time = time.time()
                    l = []
                    m = []
                    n = []
        return temp
            # cv2.putText(res_img, f"blinks: {round(TOTAL,3)}",(10,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            # cv2.imshow('preview', res_img)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
