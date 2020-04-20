import numpy as np
import cv2
from keras.models import load_model
import scipy.io as sio





base_path_hazyImg = 'image/' 
base_path_result = 'patchMap/'
imgname = 'waterfall.tif'
modelDir = 'PMS-Net.h5'


print ("Process image: ", imgname)



hazy_sample = cv2.imread(base_path_hazyImg + imgname)
hazy_sample = cv2.resize(hazy_sample,(640,480))
hazy_input = np.reshape(hazy_sample,(1, 480, 640, 3))
model = load_model(modelDir)
patchMap = model.predict(hazy_input, verbose = 1)
patchMap = np.reshape(patchMap,(-1,1))
patchMap = np.reshape(patchMap,(480, 640))
patchMap = np.float64(patchMap)


imgname = imgname.replace('.tif','')


print('saveDir:',base_path_result + imgname + '.mat')

sio.savemat(base_path_result + imgname + '.mat',{"patchMap":patchMap})




