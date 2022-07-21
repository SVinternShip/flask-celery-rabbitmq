# flask.celery.rabbitmq


#### Requires Google Cloud Storage

    https://cloud.google.com/docs/

#### Go to Cloud Storage and Dig Buckets
    

    https://cloud.google.com/docs/authentication/production?hl=ko#create-service-account-console

    
#### Access json key file issue and git clone
    

    https://cloud.google.com/docs/authentication/production?hl=ko#create_service_account

    
    
#### Modify the code to match the corresponding key file path and bucket name to task.py
    
    def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'service_account.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
        
### *tasks.py*

[pro > flask api ,

뒤에 ml

![image](https://user-images.githubusercontent.com/53938323/180130812-5a5a8a28-2544-4dba-99a5-aa7404f66b19.png)


#### RABBITMQ

    Rabbitmq assigns continuous (long-term) tasks to CELERY WORKERS.
    CELERY WOKERS store the original image from the preprocessing function and the Lime image returned from the predict_and_lime on the server.
    Finally, it returns predicated, patient_id, study_modality.
    
    Each CELERY WORKER has to load each deep learning model, but it's expensive. So load and use one global model.
    Of course, when multiple requests are received at the same time, the time is delayed because the results must be sequentially waited from one model.
    An alternative to this is to give two or more BATCHSIZE so that multiple inputs can be received at the same time and processed at the same time.
    
    
### *predict_module.py*


#### preprocess

![image](https://user-images.githubusercontent.com/53938323/180136039-a29d5f12-3736-44fa-87b6-1813e01cccca.png)

    make gray scale dicom file to 3 channel jpg file



#### predict & lime explain

   
![image](https://user-images.githubusercontent.com/53938323/180135637-4643b279-a90b-4f7a-891e-f79f21292ffc.png)

    The dicom file is preprocessed according to the model input value and other dicom attributes are extracted.
    The preprocessed image is input to the model, and a mask explaining the reason predicted through the rim expander is returned.

    [작성중]
    해당 결과(모델 예측, 라임 마스트)를 장고 서버로 전송
    원본 다이콤 파일을 구글 스토리지에 저장
