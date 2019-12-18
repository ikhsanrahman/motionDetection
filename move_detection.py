import cv2, time, numpy as np, pandas as pd
from datetime import datetime 

cap = cv2.VideoCapture(0)
# test = cv2.VideoCapture(2)
first_frame = None
status_list = [None, None]
times = []
df = pd.DataFrame(columns=["start", "end"])

while True:
	check, frame = cap.read()
	# check, wew = test.read()
	status = 0
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21,21), 0)

	if first_frame is None:
		first_frame = gray
		continue

	delta_frame = cv2.absdiff(first_frame, gray)
	print(first_frame==gray)
	thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
	thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)
	cnts, __ = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for contour in cnts:
		if cv2.contourArea(contour)<10000:
			continue
		status = 1
		(x,y,w,h) = cv2.boundingRect(contour)
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
	# status_list.append(status)
	# status_list = status_list[-2:]

	# print(status_list)

	# if status_list[-1] ==1 and status_list[-2:] ==0:
	# 	times.append(datetime.now())

	# if status_list[-1] ==0 and status_list[-2] ==1:
	# 	times.append(datetime.now())

	# for i in range(0, len(times),2):
	# 	df = df.append({"start":times[i], "end":times[i+1]}, ignore_index=True)

	# df.to_csv("Times.csv")

	cv2.imshow('frame', frame)
	# cv2.imshow('frame', wew)
	cv2.imshow('capturing', gray)
	cv2.imshow('delta', delta_frame)
	cv2.imshow('thresh', thresh_delta)


	key = cv2.waitKey(1)
	if key == ord('q'):
		break



cap.release()
cv2.destroyAllWindows()