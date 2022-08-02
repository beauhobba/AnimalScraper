import cv2
import numpy as np

# Rights of the map go to https://wearebecome.com/article/tongjiziliao/cf/australian-ecosystems-k.html
map = "./maps/IBRA2.png"
LIMITS = 5

def convert_hsv_to_ranges(hsv):
    h = hsv[0]*255/360
    s = hsv[1]*255/100
    v = hsv[2]*255/100
    return [h, s, v]

def convert_to_ranges(hsv):
    new_hsv = convert_hsv_to_ranges(hsv)
    upper = [new_hsv[0]+LIMITS, new_hsv[1]+LIMITS, new_hsv[2]+LIMITS]
    lower = [new_hsv[0]-LIMITS, new_hsv[1]-LIMITS, new_hsv[2]-LIMITS]
    
    for idx, val in enumerate(upper):
        if val>255:
            upper[idx] = 255
    for idx, val in enumerate(lower):
        if val<0:
            lower[idx] = 0
    return [np.array(lower), np.array(upper)]

ibra_regs = {
    'CAR': [np.array([0, 77, 245], np.uint8), np.array([29, 98, 255], np.uint8)],
    'GAS': [np.array([25, 69, 226], np.uint8), np.array([39, 78, 255], np.uint8)],
    'PIL': [81, 17, 85],
    'MUR': [np.array([23, 61, 208], np.uint8), np.array([27, 68, 227], np.uint8)],
    'GES': [77, 15, 95],
    'YAL': [35, 21, 99],
    'SWA': [52, 18,100],
    'AVW': [51, 19, 92],
    'JAF': [110, 25, 99],
    'WAR': [122, 27, 90],
    'ESP': [48, 52, 88],
    'MAL': [35, 38, 87],
    'COO': [48, 33, 86],
    'PIL': [81, 17, 85],
    'DMR': [np.array([0, 0, 235], np.uint8), np.array([10, 255, 255], np.uint8)],
    'CHC': [np.array([10, 75, 226], np.uint8), np.array([13, 78, 240], np.uint8)],
}

text = [np.array([0, 0, 0]), np.array([254, 255, 127])]
outline = [np.array([0, 0, 255]), np.array([0, 0, 255])]


img = cv2.imread(map, 1)
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(hsv_img, *ibra_regs['CHC'])
res = cv2.bitwise_and(img, img, mask=mask)

ret, threshold = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

mask_bkg = ~(cv2.inRange(hsv_img, *outline))
mask_text = (cv2.inRange(hsv_img, *text))

image2 = img.copy()
image2[mask_bkg > 0] = (0, 0, 0)
image2[mask_text > 0] = (0, 0, 0)
im = image2 | res

# mask_gray_border = 255
# mask_white = cv2.inRange(hsv_img, lower_white, upper_white)

bkd = mask_bkg + mask_text

window_name = 'image'
cv2.imshow(window_name, im)
cv2.waitKey(0) 
  
#closing all open windows 
cv2.destroyAllWindows() 