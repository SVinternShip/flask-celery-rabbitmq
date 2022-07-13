# worker의 task 파일
#!/usr/bin/env python
# coding: utf-8

import os
from tensorflow import keras
import sys
import numpy as np
from os import path
import tempfile
import requests
import io
import datetime
import cv2
from PIL import Image
sys.path.append(path.dirname(path.abspath(__file__)))

import predict_module

dcm_file_path = 'ID_00a4abdde.dcm'
patient_result = 11


img_original = predict_module.dicom2nparray(dcm_file_path) # 원본이미지
img_preprocessed, patient_id, patient_name, study_modality,ct_study_id,ct_study_date,ct_study_time  = predict_module.preprocess(dcm_file_path) # batch,환자 ID,StudyModality
predicted, img_lime = predict_module.predict_and_lime(img_preprocessed, img_original) # 모델결과문장,lime이미지
print('patient_id : {}, study_modality : {}, predicted : {}'.format(patient_id, study_modality, predicted))
print(type(img_lime), type(img_original)) # <class 'NoneType'>, <class 'numpy.ndarray'>
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

now = str(datetime.datetime.now())

pil_original = Image.fromarray(img_original)
pil_lime = Image.fromarray(img_lime)

temp_original_file = tempfile.NamedTemporaryFile()
pil_original.save(temp_original_file, 'png')


temp_lime_file = tempfile.NamedTemporaryFile()
pil_lime.save(temp_lime_file, 'png')
#
#
print(temp_original_file.name)
url = "http://localhost:8000/api/ct/storeResult"
payload = {'prediction': predicted,
           'patient_result': patient_result,
           'studyDate': ct_study_date+'T'+ct_study_time,
           'patientName': patient_name,
           'fileName':dcm_file_path}

files=[
  ('original_image',(dcm_file_path.replace("dcm", "png"),open(temp_original_file.name,'rb'),'image/png')),
  ('lime_image',(dcm_file_path.replace("dcm", "png"),open(temp_lime_file.name,'rb'),'image/png'))
]

response = requests.request("POST", url, data=payload, files=files)

print(response)



