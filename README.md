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



    

   
