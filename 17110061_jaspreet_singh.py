import numpy as np
import cv2
count=0
vid = cv2.VideoCapture(0)# FOR WEB CAM
#vid = cv2.VideoCapture('rtsp://admin:12345@192.168.60.35:554/')# FOR IP CAM
#vid = cv2.VideoCapture('VIDEO MANE.MP4')# FOR VIDEO 
frame_width = int( vid.get(cv2.CAP_PROP_FRAME_WIDTH))   #
frame_height =int( vid.get( cv2.CAP_PROP_FRAME_HEIGHT))    #
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))
ret, frame1 = vid.read()  # read video frame by frame as time t
ret, frame2 = vid.read()   # read video frame by frame at time t+1
while vid.isOpened():
    diff = cv2.absdiff(frame1, frame2)   # take difference between two frames

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)   # convert the frame colours to gray scale

    blur = cv2.GaussianBlur(gray, (5,5), 0)    # convert grey scale into gaussian

    _, thresh = cv2.threshold(blur, 10, 11, cv2.THRESH_BINARY)    # setting the threshold values to check

    dilated = cv2.dilate(thresh, None, iterations=3)  # diluting the threshold values

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)  # converting contour into rectangular box

        if cv2.contourArea(contour)<6000:  # sensitivity of detection CHANGE FROM 600 TO 10000 ACCORDING TO NEED
            continue

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.imwrite("./output/frame%d.jpg" % count, frame1)
        count+=1
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
    

    image = cv2.resize(frame1, (1080,720))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = vid.read()
    if cv2.waitKey(40) == 27:
        break
cv2.destroyAllWindows()
vid.release()
out.release()
