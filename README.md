![image](https://user-images.githubusercontent.com/53938323/180675642-09d2cefd-7561-4f33-9011-dd6648578728.png)



# flask.celery.rabbitmq


#### docker build

    docker-compose up --build
    
    
#### model load

     wandb link : https://wandb.ai/pypyp/aiinternship/runs/2u55kqpw/files?workspace=user-sykim1106
     download model-best.h5 and change model file path

#### Requires Google Cloud Storage

    https://cloud.google.com/docs/

#### Go to Cloud Storage and Dig Buckets
    

    https://cloud.google.com/docs/authentication/production?hl=ko#create-service-account-console

    
#### Access json key file issue and git clone
    

    https://cloud.google.com/docs/authentication/production?hl=ko#create_service_account

    
    
#### Modify the code to match the corresponding key file path and bucket name to task.py
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./robotic-haven-356701-952019494169.json"
    bucket_name = 'savedcmbucket'    # 서비스 계정 생성한 bucket 이름 입력
        
### *tasks.py*

![image](https://user-images.githubusercontent.com/53938323/180138287-48fe799d-9f3a-4422-afcf-13a85657cce2.png)

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

    make gray scale dicom file to 3 channel image file



#### predict & lime explain

   
![image](https://user-images.githubusercontent.com/53938323/180142309-80089304-7b9c-43cf-a973-3ab5c465d471.png)



    The dicom file is preprocessed according to the model input value and other dicom attributes are extracted.
    The preprocessed image is input to the model, and a mask explaining the reason predicted through the rim expander is returned.

    Send the corresponding result (model prediction, lime mask) to Django Server
    Save the original image to Google Storage
    
    
   
