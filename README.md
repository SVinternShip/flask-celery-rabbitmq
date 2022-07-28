![image](https://user-images.githubusercontent.com/53938323/180675642-09d2cefd-7561-4f33-9011-dd6648578728.png)



# flask.celery.rabbitmq
## Index
- [SVinternShip](#SVinternShip)
  - [1. Prerequisites](#1-prerequisites)
  - [2. Installation Process](#2-installation-process)
  - [3. Getting Started](#3-getting-started)
  - [4. File Manifest](#4-file-manifest)
  - [5. Copyrights / End User Licesnse](#5-copyrights--end-user-licesnse)
  - [6. Contact Information](#6-contact-information)

## 1. Prerequisites

Our service was created through the AI Application Development by Silicon Valley Engineering program organized by Headstart Silicon Valley.
http://www.learnflagly.com/courses/347/

## 2. Installation Process

```
$ pip3 install requirements.txt
```

## 3. Getting Started
- Please complete the Cuda installation and requirements installation


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
    

## 4. File Manifest && API
```

```


## 5. Copyrights / End User Licesnse

This project is not intended for commercial use, please do not use it for commercial purpose
   
| Name    | 전준형                                        |김민지                               | 김성윤                                        | 김정원                                    | 전경희                               |
| ------- | --------------------------------------------- | ------------------------------------ | --------------------------------------------- | --------------------------------------- | --------------------------------------------- |
| Profile | <img width="200px" src="https://user-images.githubusercontent.com/53938323/181186519-97376af4-dec2-4266-b481-84476a7b08cf.png" />|<img width="200px" src="https://user-images.githubusercontent.com/53938323/181186658-5fa337ab-1073-40c1-ba1f-821eca61a241.png" />| <img width="200px" src="https://user-images.githubusercontent.com/53938323/181186805-e25768c2-b5b3-4af1-9ebe-f4ab31eba8f0.png" />| <img width="200px" src="https://user-images.githubusercontent.com/53938323/181186873-68715eac-5ba7-4084-aed6-613461addf37.png" />| <img width="200px" src="https://user-images.githubusercontent.com/53938323/181186909-add7aa9e-40ba-4822-98dc-994f21c2c455.png" />|
| role    | Team ㅣLeader, <br>Backend , <br>Frontend                  | Frontend , <br>Backend                      | ML                                | Frontend | Backend |
| Github  | [@Joon_Hyoung](https://github.com/Gitko97) | [@Minji Kim](https://github.com/minji1289) | [@sykim1106](https://github.com/hanueluni1106) | [@grdnr13](https://github.com/grdnr13) |  [@kjeon0901](https://github.com/kjeon0901) |
