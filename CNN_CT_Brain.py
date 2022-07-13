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
import datetime
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
    img_preprocessed, patient_id, patient_name, study_modality, ct_study_id, ct_study_date, ct_study_time = predict_module.preprocess(dcm_file_path) # batch,환자 ID,환자명,StudyModality,StudyID,StudyDate,StudyTime
    print("ccccccccccccccccccccccccccccccc")
    predicted, img_lime = predict_module.predict_and_lime(img_preprocessed, img_original) # 모델결과문장,lime이미지
    print('original_img : {}, lime_img : {}, '.format(img_original, img_lime)) # celery 실행된 터미널에 찍힘
    print('patient_id : {}, study_modality : {}, predicted : {}'.format(patient_id, study_modality, predicted))
    print(type(img_lime), type(img_original)) # <class 'NoneType'>, <class 'numpy.ndarray'>
    print(type(predicted), type(patient_result), type(study_modality), type(patient_id))
    print(patient_result)
    if predicted == 'hemorrhage':
        predicted = 'False'
    else:
        predicted = 'True'
    try:
        if img_lime is None:
            img_lime = img_original

        '''
        original_bytes = img_original.tobytes()
        original_stream = io.BytesIO(original_bytes)
        lime_bytes = img_lime.tobytes()
        lime_stream = io.BytesIO(lime_bytes)
        '''
        # 로컬에저장 : datetime.datetime.now() + dcm_file_path
        # 파일명 : dcm_file_path.replace('.dcm', '.png') 둘다 이렇게,
        # numpy array를 cv2로 저장하고, 각각 읽어와서 보낸 뒤 삭제
        now = str(datetime.datetime.now()).replace(' ', '_').replace('.', '_').replace(':', '_').replace('-', '_')
        cv2.imwrite(now + 'img_original.png', img_original)
        cv2.imwrite(now + 'img_lime.png', img_lime)
        png_original = open(now +'img_original.png', 'rb')
        png_lime = open(now + 'img_lime.png', 'rb')

        url = "http://54.180.55.27:8000/api/ct/storeResult"
        payload = {'prediction': predicted,
                   'patient_result': patient_result,
                   'studyDate': ct_study_date+'T'+ct_study_time,
                   'patientName': patient_name,
                   'fileName': dcm_file_path}
        files = [
            ('original_image', (dcm_file_path.replace('.dcm', '.png'), png_original, 'image/png')),
            ('lime_image', (dcm_file_path.replace('.dcm', '.png'), png_lime, 'image/png'))
        ]
        #files = {"original_image": original_stream, "lime_image": lime_stream}
        response = requests.request("POST", url, data=payload, files=files)
        png_original.close()
        png_lime.close()
        os.remove(now + 'img_original.png')
        os.remove(now + 'img_lime.png')
        os.remove(dcm_file_path)

    except Exception as e:
        print(e.with_traceback())


    #return predicted, patient_id, study_modality # flower dashboard에 result로 찍힘
    return 'good'


@celery.task
def callback(results):
    return results
