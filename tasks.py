# worker의 task 파일
# !/usr/bin/env python
# coding: utf-8

import os
import tempfile

import numpy as np
import requests
from datetime import datetime
from PIL import Image
from celery import Celery
import predict_module
from tensorflow import keras
from google.cloud import storage
BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit'
#BROKER_URL = 'amqp://guest:guest@localhost:5672'

CELERY = Celery('tasks',
                broker=BROKER_URL,
                backend='rpc://')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./robotic-haven-356701-952019494169.json"
bucket_name = 'savedcmbucket'    # 서비스 계정 생성한 bucket 이름 입력
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

# 여기서 글로벌로 먼저 모델 불러 와서, predict_module.predict_and_lime() 에 매개변수로 모델을 넘겨주도록 해줘야 함.
loaded = keras.models.load_model('./model-best.h5')

# CELERY.conf.accept_content = ['json', 'msgpack']
# CELERY.conf.result_serializer = 'msgpack'

@CELERY.task()
def get_dcm_predicted(dcm_file_path, patient_result):
    global loaded
    img_original = predict_module.dicom2nparray(dcm_file_path)  # 원본이미지
    img_preprocessed, patient_id, patient_name, study_modality, ct_study_id, ct_study_date, ct_study_time = predict_module.preprocess(
        dcm_file_path)  # batch,환자 ID,StudyModality
    predicted, img_lime = predict_module.predict_and_lime(img_preprocessed, img_original, loaded)  # 모델결과문장,lime이미지
    print('patient_id : {}, study_modality : {}, predicted : {}'.format(patient_id, study_modality, predicted))
    print(type(img_lime), type(img_original))  # <class 'NoneType'>, <class 'numpy.ndarray'>
    print(type(predicted), type(patient_result), type(study_modality), type(patient_id))
    print(patient_result)

    if predicted == 'hemorrhage':
        predicted = 'False'
    else:
        predicted = 'True'

    img_original = img_original.astype(np.uint8)
    if img_lime is None:
        img_lime = img_original

    print(img_lime.dtype, img_original.dtype)

    pil_original = Image.fromarray(img_original)
    pil_lime = Image.fromarray(img_lime)

    temp_original_file = tempfile.NamedTemporaryFile()
    pil_original.save(temp_original_file, 'png')

    temp_lime_file = tempfile.NamedTemporaryFile()
    pil_lime.save(temp_lime_file, 'png')

    print(temp_original_file.name)

    dcm_file_name = dcm_file_path.split('/')[-1]
    url = "http://54.180.55.27:8000/api/ct/storeResult"
    payload = {'prediction': predicted,
               'patient_result': patient_result,
               'studyDate': ct_study_date + 'T' + ct_study_time,
               'patientName': patient_name,
               'fileName': dcm_file_name}
    png_file_name = dcm_file_name.replace("dcm", "png")
    files = [
        ('original_image', (png_file_name, open(temp_original_file.name, 'rb'), 'image/png')),
        ('lime_image', (png_file_name, open(temp_lime_file.name, 'rb'), 'image/png'))
    ]
    response = requests.request("POST", url, data=payload, files=files)
    print(response)
    destination_blob_name = str(datetime.now()) + '_' + dcm_file_path.split('/')[-1]
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(dcm_file_path)

    os.remove(dcm_file_path)

    # return 'good'
    return predicted, patient_id, study_modality # flower dashboard에 result로 찍힘

