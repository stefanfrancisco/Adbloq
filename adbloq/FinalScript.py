##Final Script that has everything. 
# Written by: Stefan Francisco, Kevin Manan, Nathan Sanders, & Thomas Stubblebine

import sys
sys.path.append('/home/rbruce/caffeV2/caffe/python')
import caffe
import cv2
import os
import lmdb
import numpy as np
import glob
from caffe.proto import caffe_pb2

caffe.set_mode_gpu()


#Size of images
IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224


def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

    return img


'''
Reading mean image, caffe model and its weights 
'''
#Read mean image
def Classify(img): #openCV image. 
    mean_blob = caffe_pb2.BlobProto()
    with open('/home/rbruce/caffeV2/adbloq/databases/mean.binaryproto') as f:
        mean_blob.ParseFromString(f.read())
    mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
        (mean_blob.channels, mean_blob.height, mean_blob.width))


    #Read model architecture and trained model's weights
    net = caffe.Net('/home/rbruce/caffe/deeplearning-cats-dogs-tutorial/caffe_models/caffe_model_1/caffenet_deploy_1.prototxt',
                    '/home/rbruce/caffeV2/adbloq/snapshots/_iter_10000.caffemodel',
                    caffe.TEST)

    #Define image transformers
    # try:
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_mean('data', mean_array)
    transformer.set_transpose('data', (2,0,1))

    '''
    Making predicitions
    '''
    #Reading image paths
    #test_img_paths = [img_path for img_path in glob.glob("/home/student/Documents/test1.jpeg")]
    #since we already have the image passed. we don't need this. 
    #Making predictions
    test_ids = []
    preds = []
    # for img_path in test_img_paths:
    #img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    h1, w1, z = img.shape
    if w1 < IMAGE_WIDTH or h1 < IMAGE_HEIGHT:
        return 0
    img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)

    net.blobs['data'].data[...] = transformer.preprocess('data', img)
    out = net.forward()
    pred_probas = out['prob']

    # test_ids = test_ids + [img_path.split('/')[-1][:-4]]
    preds = preds + [pred_probas.argmax()]

#    print img_path
    return pred_probas.argmax() ##this is where it gets returned. 1 for advertisement, 0 for not an ad. 
    # except ValueError:
    #     return 0
#    print '-------'


def makeTransparent(img):
	width, height, channels = img.shape
	img = cv2.rectangle(img, (0, 0), (height, width),(255, 255, 255), -1)
	# cv2.imshow('test', img)
	# cv2.waitKey(0)
	# cv2.imwrite('/Users/kevinmanan/Desktop/test/test.jpg', img)
	return img


# image = cv2.imread('/home/rbruce/Desktop/test3.jpg')

# print Classify(image)