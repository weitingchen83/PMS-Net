import numpy as np

def find_atmosphericLight(image, dark_channel):

    m, n = image.shape[0], image.shape[1]

    search_A_pixel = np.floor(m*n*0.01)
    image_save = np.reshape(image, (m*n, 3))
    darkchannel_save = np.reshape(dark_channel, m*n)

    saver = np.zeros((1, 3))
    idx = np.argsort(-darkchannel_save)

    for pixel_idx in range(int(search_A_pixel)):
        saver = saver + image_save[ idx[pixel_idx], :]

    A = saver / search_A_pixel
    return A