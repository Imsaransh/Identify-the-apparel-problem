# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 07:46:23 2019

@author: admin
"""

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing import image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from tqdm import tqdm

train=pd.read_csv("train.csv")

# We have grayscale images, so while loading the images we will keep grayscale=True, if you have RGB images, you should set grayscale as False
train_image = []
for i in tqdm(range(train.shape[0])):
    img = image.load_img('train/'+train['id'][i].astype('str')+'.png', target_size=(28,28,1), grayscale=True)
    img = image.img_to_array(img)
    img = img/255
    train_image.append(img)
X = np.array(train_image)

y=train['label'].values
y = to_categorical(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=(28,28,1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='Adam',metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

model.save("Fashion.h5")
model.save("Fashion.model")
""" LOADING MODEL
    from keras.models import load_model
    model=load_model("Fashion.h5")
"""
# Inputting test data
test=pd.read_csv("test.csv")
test_image = []
for i in tqdm(range(test.shape[0])):
    img = image.load_img('test/'+test['id'][i].astype('str')+'.png', target_size=(28,28,1), grayscale=True)
    img = image.img_to_array(img)
    img = img/255
    test_image.append(img)
test = np.array(test_image)

# Making Predictions

prediction = model.predict_classes(test)
model.evaluate(X_test,y_test)


sample = pd.read_csv('sample_submission_I5njJSF.csv')
sample['label'] = prediction
sample.to_csv('sample_cnn.csv', header=True, index=False)