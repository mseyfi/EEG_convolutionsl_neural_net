import sys, random, time, json, os

import numpy as np

from scipy.io import loadmat

from keras.models import Sequential, model_from_json

from keras.layers import Dense, Activation, Flatten

from keras.layers import Convolution1D, Convolution2D, Convolution3D, AveragePooling2D, Reshape, Lambda, Permute

from keras.utils import np_utils

from keras import backend as K

from grnnf import parse_data, model_manip, data_manip

description = ""
if sys.argv[2] != None:
    description = sys.argv[2]
else:
    description = str(time.time())
    
model = Sequential()

def logIt(x):
    return K.log(x)

model.add(Convolution2D(40, (1,5), activation="relu", input_shape=(1,124,32), data_format="channels_first"))
model.add(Permute((3,2,1)))
model.add(Reshape((1,28,124,40)))
model.add(Convolution3D(40, (1,124,40), activation="relu", data_format="channels_first"))
model.add(Lambda(lambda x: x ** 2))
model.add(Reshape((40,28,1)))
#model.add(AveragePooling2D((1, 5), (1, 1)))
#model.add(Activation("relu"))
#literal garbage
#model.add(Lambda(logIt))
model.add(Flatten())
model.add(Dense(6, activation="softmax"))
model.summary()

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

#save model structure as json to 'model/structure/'
model_manip.save_model("../models/structure/model" + description + ".json", model)

directory = "../models/weights/" + description + "/"
if not os.path.exists(directory):
            os.makedirs(directory)
