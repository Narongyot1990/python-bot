import cv2 
import numpy as np 


bg = cv2.imread('bg.png', cv2.IMREAD_REDUCED_COLOR_2)
obj = cv2.imread('obj.png', cv2.IMREAD_REDUCED_COLOR_2)

result = cv2.matchTemplate(bg, obj, cv2.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % max_val)

threshold = 0.8
if max_val >= threshold:
    print('Found Obj.')

    obj_w = obj.shape[1]
    obj_h = obj.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + obj_w, top_left[1] + obj_h)

    cv2.rectangle(bg, top_left, bottom_right,
                  color=(0, 255, 0),thickness=2, lineType=cv2.LINE_4)
    
    #cv2.imwrite('result.png', bg)  # Save the result image
    cv2.waitKey()
    
else:
    print('Obj not found')