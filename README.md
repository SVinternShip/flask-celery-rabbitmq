# flask.celery.rabbitmq


#### 구글 클라우드 스토리지가 필요

    https://cloud.google.com/docs/

#### 클라우드 스토리지에 가서 버킷 파내기
    

    https://cloud.google.com/docs/authentication/production?hl=ko#create-service-account-console

    
#### 접속 json key file 발급 받급 후 git clone
    

    https://cloud.google.com/docs/authentication/production?hl=ko#create_service_account

    
    
#### task.py 에 해당 key file path 에 맞게 코드 수정
    
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

![image](https://user-images.githubusercontent.com/53938323/180130812-5a5a8a28-2544-4dba-99a5-aa7404f66b19.png)


#### RABBITMQ

    rabbitmq 는 계속 오는 (오래걸리는) 작업들을 CELERY WORKER 들에게 배정한다.
    CELERY WOKER 들은 전처리 함수를 통해 나온 원본 이미지와, predict_and_lime 에서 반환된 Lime 이미지를 서버에 저장한다.
    최종적으로 predicted, patient_id, study_modality 를 반환한다.
    
    각 CELERY WORKER 들은 각 딥러닝 모델을 로드해야 하지만, 많은 비용이 소모되므로
    하나의 글로벌 모델을 로드하여 사용한다.
    물론, 동시에 여러 요청이 들어올 경우에는 하나의 모델로부터 순차적으로 결과를 대기해야 하므로 시간이 지연된다.
    이에 대한 대안으로는 BATCHSIZE 를 2 이상 주어서 동시에 여러 input 을 받아서 동시에 처리할 수 있도록 하면 된다.
    
    
    

   
