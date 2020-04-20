import cv2
import scipy.io as sio
import numpy as np
from dehaze_patchMap_dehaze import dehaze_patchMap

hazy_img_dir = 'image/'
patchMap_dir = 'patchMap/'
save_dir = 'result/'
imgname= 'girls.tif'


image = cv2.imread(hazy_img_dir + imgname)
if image.shape[0] != 480 or image.shape[1] != 640:
    print('resize image tp 640*480')
    image = cv2.resize(image,(640,480))
    
print(imgname)
patchMapname = imgname[:-4] + '.mat'

patchMap = sio.loadmat(patchMap_dir + patchMapname)
patchMap = np.array(patchMap['patchMap'])
        
recover_result, tx = dehaze_patchMap(image, 0.95, patchMap)

savename_result = save_dir + 'py_recover_' + imgname

cv2.imwrite(savename_result, recover_result)


   
