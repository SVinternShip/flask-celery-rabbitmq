# worker의 task 파일

#!/usr/bin/env python
# coding: utf-8
import os
import os.path
from warnings import filterwarnings
import sys
from os import path
import requests
from celery_app import celery
import pydicom as dicom
sys.path.append(path.dirname(path.abspath(__file__)))


filterwarnings("ignore", category=DeprecationWarning)
filterwarnings("ignore", category=FutureWarning)
filterwarnings("ignore", category=UserWarning)


@celery.task
def get_dcm_predicted(dcm_file_path):
    import predict_module

    img_original = predict_module.dicom2nparray(dcm_file_path) # 원본이미지
    img_preprocessed, patient_id, study_modality = predict_module.preprocess(dcm_file_path) # batch,환자 ID,StudyModality
    predicted, img_lime = predict_module.predict_and_lime(img_preprocessed, img_original) # 모델결과문장,lime이미지
    print('original_img : {}, lime_img : {}, '.format(img_original, img_lime)) # celery 실행된 터미널에 찍힘
    print('patient_id : {}, study_modality : {}, predicted : {}'.format(patient_id, study_modality, predicted))
    print(type(img_lime), type(img_original)) # <class 'NoneType'>, <class 'numpy.ndarray'>

    url = "http://127.0.0.1:5000/ct/storeResult"
    payload = {'prediction': str(predicted),
               'patient_result': '7',
               'studyDate': '2022-07-06 23:11:35.573131+09',
               'patientName': '전준형',
               'patient_id': str(patient_id),
               'study_modality': str(study_modality)}
    #files = [ # jpg 타입으로 받으면 바꾸기
    #    ('original_image', img_original)
    #    ('lime_image', img_lime)
    #]
    headers = {
        'Cookie': 'csrftoken=MURZta4Ehw5gv0BOsfo5NNqm2cH0amkQh4hwdA5ejHLgwLpAGXvlyxxoUx2IFr8A'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files={'logo':open("img.jpeg",'rb')})

    os.remove(dcm_file_path)
    return predicted, patient_id, study_modality


@celery.task
def callback(results):
    return results
