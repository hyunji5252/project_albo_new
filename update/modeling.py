

from django.db import connection
from main.models import *


import pandas as pd
from PIL import Image
import tensorflow as tf
import os,glob
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Input, Dense, GlobalAveragePooling2D
import shutil
import random

trade_path = r'C:\\projects\\albo\\media\\' # \\ 두 개씩 써주기
TRAIN_DATA_DIR = 'C:\\projects\\albo\\media\\train\\' #기존 데이터
VALIDATION_DATA_DIR = 'C:\\projects\\albo\\media\\trade_images\\' #거래완료데이터

NUM_CLASSES = 3
IMG_WIDTH, IMG_HEIGHT = 300, 300
BATCH_SIZE = 64
Epochs = 100


# 학습에서 제외시킬 데이터 삭제
def exclude_from_training():

    global trade_path

    df = pd.DataFrame(list(Trade.objects.all().values()))
    # df.to_csv('C:\MyTest\PJT1\df.csv')
    #os.remove('C:\MyTest\PJT1\df.csv')


    df['item_img'] = trade_path+df['item_img'] 


    condition1 = df.item_price < 100000
    condition2 = df.item_price >= 1600000
    drop_idx = df[condition1 | condition2 ].index
    # condition3 = df.price % 1000 !=0
    # drop_idx = df[condition1 | condition2 | condition3].index
    df.drop(drop_idx, axis=0, inplace=True)

    return df

# 가격에 따라 라벨링하고 train set에 추가하기
def add_label_column():

    df = exclude_from_training()

    # 가격에 따른 라벨링
    label = []
    prices = df.item_price.to_list()
    new_data_size = len(prices)

    for i in range(new_data_size):
        if prices[i] < 450000:
            label.append(2)
        elif prices[i] < 800000:
            label.append(3)
        else:
            label.append(4)
    
    df['label'] = label

    return df

# train set과 validation set에 각각 데이터 추가하기
def add_data_to_train_and_val_sets():

    df = add_label_column()

    for category in set(df.label):
        condition = (df.label == category)
        img_paths = df.loc[condition].item_img.to_list()

        train_path = TRAIN_DATA_DIR + str(category) + '\\'
        val_path = VALIDATION_DATA_DIR + str(category) + '\\'

        val_img_paths=[]
        val_size = int(len(img_paths)* 0.3)
        for i in random.sample(img_paths, val_size):
            val_img_paths.append(i)
        train_img_paths = [x for x in img_paths if x not in val_img_paths]

        for i in range(len(train_img_paths)):
            image_name = train_img_paths[i].split('\\')[-1]  

            shutil.copy(img_paths[i], train_path+image_name) # shutil.move로 바꿔도 됨


        for i in range(len(val_img_paths)):
            image_name = val_img_paths[i].split('\\')[-1]  

            shutil.copy(img_paths[i], val_path+image_name) # shutil.move로 바꿔도 됨
    
  

    return None

#add_data_to_train_and_val_sets()

def get_num_of_train_samples(train_dir_path):
    TRAIN_SAMPLES = 0
    for i in range(2,5):
        folder_path = train_dir_path + str(i)
        dirListing = os.listdir(folder_path)
        TRAIN_SAMPLES += len(dirListing)
    return TRAIN_SAMPLES

# 추가된 데이터로 인해 바뀐 validation 데이터의 개수 구하기
def get_num_of_val_samples(val_dir_path):
    VALIDATION_SAMPLES = 0
    for i in range(2,5):
        folder_path = val_dir_path + str(i)
        dirListing = os.listdir(folder_path)
        VALIDATION_SAMPLES += len(dirListing)
    return VALIDATION_SAMPLES

# 이미지 증강
def augment_image():
    train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input,
                                      rotation_range=20,
                                      width_shift_range=0.2,
                                      height_shift_range=0.2,
                                      zoom_range=0.2)
    
    train_generator = train_datagen.flow_from_directory(TRAIN_DATA_DIR,
                                                        target_size=(IMG_WIDTH,IMG_HEIGHT),
                                                        batch_size=BATCH_SIZE,
                                                        shuffle=True,
                                                        seed=12345,
                                                        class_mode='categorical')


    val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    
    validation_generator = val_datagen.flow_from_directory(VALIDATION_DATA_DIR,
                                                          target_size=(IMG_WIDTH, IMG_HEIGHT),
                                                          batch_size=BATCH_SIZE,
                                                          shuffle=False,
                                                          class_mode='categorical')
    return train_generator, validation_generator

# 모델 구조 만들기
def model_maker():
    
    base_model = VGG16(include_top=False, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))
    
    input = Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3))
    
    custom_model = base_model(input)
    custom_model = GlobalAveragePooling2D()(custom_model)
    custom_model = Dense(256, activation='relu')(custom_model)
    custom_model = Dense(128, activation='relu')(custom_model)
   
    predictions = Dense(NUM_CLASSES, activation='softmax')(custom_model)
    
    return Model(inputs=input, outputs=predictions)

# 학습 시키기 및 모델 저장
def train_and_save_model():
    
    TRAIN_SAMPLES = get_num_of_train_samples(TRAIN_DATA_DIR)
    VALIDATION_SAMPLES = get_num_of_val_samples(VALIDATION_DATA_DIR)

    train_generator, validation_generator = augment_image()
  
    model_final = model_maker()
    model_final.compile(loss='categorical_crossentropy',
                  optimizer=tf.keras.optimizers.Adam(0.000001), #adam parameter 더 적게
                  metrics=['acc'])
    
    history = model_final.fit(train_generator,
                              steps_per_epoch=TRAIN_SAMPLES // BATCH_SIZE, # number of updates
                              epochs=Epochs,
                              validation_data=validation_generator,
                              validation_steps=VALIDATION_SAMPLES // BATCH_SIZE)

    model_final.save(r'C:\\projects\\albo\\epoch100_1.h5')
    return None

def main():
    global TRAIN_DATA_DIR, VALIDATION_DATA_DIR
    global NUM_CLASSES, IMG_WIDTH, IMG_HEIGHT, BATCH_SIZE, Epochs

    add_data_to_train_and_val_sets()
    train_and_save_model()

    return None