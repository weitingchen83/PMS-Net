import cv2

def find_darkchannel(image, patch_win_size):

    patch_win_size = int(patch_win_size)
    b,g,r = cv2.split(image)
    dc = cv2.min(cv2.min(r,g),b)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(patch_win_size,patch_win_size))
    dark_channel = cv2.erode(dc,kernel)

    return dark_channel