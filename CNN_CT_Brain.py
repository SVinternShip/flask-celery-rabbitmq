# worker의 task 파일
#!/usr/bin/env python
# coding: utf-8

import os
from warnings import filterwarnings
import sys
from os import path
import requests
from celery_app import celery
import io
import cv2
import matplotlib.pyplot as plt
from PIL import Image
sys.path.append(path.dirname(path.abspath(__file__)))


filterwarnings("ignore", category=DeprecationWarning)
filterwarnings("ignore", category=FutureWarning)
filterwarnings("ignore", category=UserWarning)


@celery.task
def get_dcm_predicted(dcm_file_path, patient_result):
    import predict_module
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    img_original = predict_module.dicom2nparray(dcm_file_path) # 원본이미지
    print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
    img_preprocessed, patient_id, study_modality = predict_module.preprocess(dcm_file_path) # batch,환자 ID,StudyModality
    print("ccccccccccccccccccccccccccccccc")
    predicted, img_lime = predict_module.predict_and_lime(img_preprocessed, img_original) # 모델결과문장,lime이미지
    print('original_img : {}, lime_img : {}, '.format(img_original, img_lime)) # celery 실행된 터미널에 찍힘
    print('patient_id : {}, study_modality : {}, predicted : {}'.format(patient_id, study_modality, predicted))
    print(type(img_lime), type(img_original)) # <class 'NoneType'>, <class 'numpy.ndarray'>
    print(type(predicted), type(patient_result), type(study_modality), type(patient_id))
    print(patient_result)
    if predicted == 'hemorrhage':
        predicted = 'True'
    else:
        predicted = 'False'
    try:
        if img_lime is None:
            img_lime = img_original

        original_bytes = img_original.tobytes()
        original_stream = io.BytesIO(original_bytes)
        lime_bytes = img_lime.tobytes()
        lime_stream = io.BytesIO(lime_bytes)

        url = "http://54.180.55.27:8000/api/ct/storeResult"
        payload = {'prediction': predicted,
                   'patient_result': patient_result,
                   'studyDate': '2022-07-06 23:11:35.573131+09',
                   'patientName': patient_id}
        files = [
            ('original_image', ('original_stream.png', original_stream, 'image/png')),
            ('lime_image', ('lime_stream.png', lime_stream, 'image/png'))
        ]
        #files = {"original_image": original_stream, "lime_image": lime_stream}
        response = requests.request("POST", url, data=payload, files=files)
        os.remove(dcm_file_path)
    except Exception as e:
        print(e.with_traceback())

    #return predicted, patient_id, study_modality # flower dashboard에 result로 찍힘
    return 'good'


@celery.task
def callback(results):
    return results
