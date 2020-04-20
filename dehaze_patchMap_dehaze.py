import numpy as np
import cv2
from find_atmosphericLight import find_atmosphericLight
from find_darkchannel import find_darkchannel
from matplotlib import pyplot as plt

def dehaze_patchMap(image, omega, patchMap):

    m, n = image.shape[0], image.shape[1]

    transmissionMap = np.ones((m, n))
    darkchannelMap = np.ones((m, n))

    patchMap = np.ceil(patchMap)
    #patchMap(find(patchMap<1))=1
    #patchMap(find(patchMap>120))=120
    patchMap[patchMap<1]=1
    patchMap[patchMap>120]=120

    '''patchMap = guided_filter(rgb2gray(image), patchMap, 15, 0.001)
    patchMap = ceil(patchMap)
    patchMap(find(patchMap<1))=1
    patchMap(find(patchMap>120))=120'''

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)/255
    print(type(gray), gray.shape, type(patchMap), patchMap)
    patchMap = guidedFilter(gray, patchMap, 15, 0.001).astype(np.uint8)
    patchMap[patchMap<1]=1
    patchMap[patchMap>120]=120

    '''[patch_size, ~, patchIdx] = unique(patchMap)
    patchIdx = reshape(patchIdx, m, n)
    patch_size_num = size(patch_size)'''

    patch_size = np.unique(patchMap)

    '''for i = 1: patch_size_num(1)
        i
        dark_channel = find_darkchannel(image, patch_size(i))
        atmosphere = find_atmosphericLight(image, dark_channel)
        atmosphere_est = repmat(reshape(atmosphere, [1, 1, 3]), m, n)
        est_term = image./atmosphere_est
        tx_estimation = 1-omega*find_darkchannel(est_term, patch_size(i))
        tx_estimation = reshape(tx_estimation, m, n)
        patchIdx = patchMap == patch_size(i)
        transmissionMap(patchIdx) = tx_estimation(patchIdx)
        darkchannelMap(patchIdx) = dark_channel(patchIdx)     


        tx_refine = guided_filter(rgb2gray(image), transmissionMap, 15, 0.001)
        tx_refine = reshape(tx_refine, m, n)
        A_predict = find_atmosphericLight(image, darkchannelMap)
        A_predict = repmat(reshape(A_predict, [1, 1, 3]), m, n)
        tx = repmat(max(tx_refine, 0.1), [1, 1, 3])
        recover_result = ((image - A_predict) ./ tx) + A_predict'''
    
    image = image / 255
    for i in range(len(patch_size)):
        print(str(i), end= ' ')
        dark_channel = find_darkchannel(image, patch_size[i])

        atmosphere = find_atmosphericLight(image, dark_channel)
        
        #atmosphere_est = repmat(reshape(atmosphere, [1, 1, 3]), m, n)
        #est_term = image./atmosphere_est

        '''atmosphere_est = np.zeros((m, n, 3))
        atmosphere_est[...,0] = atmosphere[0]
        atmosphere_est[...,1] = atmosphere[1]
        atmosphere_est[...,2] = atmosphere[2]
        est_term = image / atmosphere_est'''
        est_term = image / atmosphere

        tx_estimation = 1 - omega * find_darkchannel(est_term, patch_size[i])
        tx_estimation = np.reshape(tx_estimation, (m, n))
        '''patchIdx = patchMap == patch_size(i)
        transmissionMap(patchIdx) = tx_estimation(patchIdx)
        darkchannelMap(patchIdx) = dark_channel(patchIdx)  '''
        patchIdx = patchMap==patch_size[i]
        transmissionMap[patchIdx] = tx_estimation[patchIdx]
        darkchannelMap[patchIdx] = dark_channel[patchIdx]

        '''tx_refine = guided_filter(rgb2gray(image), transmissionMap, 15, 0.001)
        tx_refine = reshape(tx_refine, m, n)
        A_predict = find_atmosphericLight(image, darkchannelMap)
        A_predict = repmat(reshape(A_predict, [1, 1, 3]), m, n)
        tx = repmat(max(tx_refine, 0.1), [1, 1, 3])
        recover_result = ((image - A_predict) ./ tx) + A_predict'''
        tx_refine = guidedFilter(gray, transmissionMap, 15, 0.001) #guided_filter(rgb2gray(image), transmissionMap, 15, 0.001)
        #tx_refine = reshape(tx_refine, m, n)
        A_predict = find_atmosphericLight(image, darkchannelMap)
        #A_predict = repmat(reshape(A_predict, [1, 1, 3]), m, n)
        #tx = repmat(max(tx_refine, 0.1), [1, 1, 3])
        tx = np.reshape(tx_refine,(m,n,1))
        tx[tx < 0.1] = 0.1
        tx = np.concatenate((tx,tx,tx), axis=2)
        recover_result = (image - A_predict) / tx + A_predict
        #plt.imshow(recover_result); plt.show()

    return recover_result * 255, tx
    
def guidedFilter(I, p, r, eps):
    hei, wid = p.shape
    N = cv2.boxFilter(np.ones((hei, wid)), -1, (r,r))

    meanI = cv2.boxFilter(I, -1, (r,r)) / N
    meanP = cv2.boxFilter(p, -1, (r,r)) / N
    corrI = cv2.boxFilter(I * I, -1, (r,r)) / N
    corrIp = cv2.boxFilter(I * p, -1, (r,r)) / N

    varI = corrI - meanI * meanI
    covIp = corrIp - meanI * meanP

    a = covIp / (varI + eps)
    b = meanP - a * meanI

    meanA = cv2.boxFilter(a, -1, (r,r)) / N
    meanB = cv2.boxFilter(b, -1, (r,r)) / N

    q = meanA * I + meanB
    return q