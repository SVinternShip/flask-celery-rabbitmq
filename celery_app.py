# celery app 생성하는 파일

from flask import Flask, jsonify, request, Blueprint
from celery import Celery
from flask_cors import CORS, cross_origin
import sys
from os import path


bp = Blueprint('main', __name__, url_prefix='/')


def create_app():
    # flask app 생성, __name__ 변수에 모듈명(파일명) "pybo" 담김
    flask_app = Flask(__name__)
    flask_app.register_blueprint(bp)
    return flask_app


def make_celery(flask_app):
    cel = Celery(
        'tasks'
        , broker='amqp://guest:guest@localhost:5672//' # amqp://rabbitmq:rabbitmq@rabbit:5672// : rabbitmq를 celery app 처리할 broker. 나중에 혼자할땐 amqp://kjeon:kjeon@localhost:5672//으로 바꿔야 함. (amqp://guest:guest@localhost:5672//)
        , backend='rpc://' # rabbitmq를 처리된 결과 보관하는 broker 로. 이거 정해줘야 task 실행 결과 받을 수 있음.
        , include=[ # worker가 처리할 task 지정
            'CNN_CT_Brain'
        ]
    )
    cel.conf.update(flask_app.config)

    class ContextTask(cel.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    cel.Task = ContextTask
    return cel


app = create_app()
'''
app.config.update(
    CELERY_BROKER_URL='amqp://rabbit:5672//', # ?
    CELERY_RESULT_BACKEND='rpc://localhost:5672/0' # ?
)
'''

# 일단 모든 도메인에 대해 CORS 설정 (특정 주소/도메인/포트만 사용하게 설정할 수도 있음)
CORS(app)
CORS(app, resources={r'*': {'origins': '*'}})
celery = make_celery(app)
sys.path.append(path.dirname(path.abspath(path.abspath(__file__))))


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        text='Hello, world'
    )


@app.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


'''
import requests

url = "http://127.0.0.1:8000/ct/storeResult"

payload={'prediction': 'True',
'patient_result': '7',
'studyDate': '2022-07-06 23:11:35.573131+09',
'patientName': '전준형'}
files=[
  ('original_image',('AdobeStock_227788356.jpeg',open('/Users/joonhyoungjeon/Downloads/AdobeStock_227788356.jpeg','rb'),'image/jpeg')),
  ('lime_image',('free-icon-rod-of-asclepius-659124.png',open('/Users/joonhyoungjeon/Downloads/free-icon-rod-of-asclepius-659124.png','rb'),'image/png'))
]
headers = {
  'Cookie': 'csrftoken=MURZta4Ehw5gv0BOsfo5NNqm2cH0amkQh4hwdA5ejHLgwLpAGXvlyxxoUx2IFr8A'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)
'''


@app.route('/ct/storeResult', methods=['GET', 'POST'])
def store_result():
    import CNN_CT_Brain

    # 로컬에 request에 있는 것 저장
    dcm_file = request.files['file']
    dcm_file_path = dcm_file.filename
    print('dcm_file_path : {}'.format(dcm_file_path))
    dcm_file.save(dcm_file_path) # request.filename 이거로 저장하기

    patient_result = request.form['patient_result']
    # print(dcm_file, patient_result)


    task_id_predicted = CNN_CT_Brain.get_dcm_predicted.delay(dcm_file_path) # 여기서 리턴값 오는 게 아니라 task_id 만 받아올 수 있음. 셀러리에서 pydicom에서 로컬path로 받을수있음. 그 저장한 path를 셀러리로 보냄. 그후 로컬에 저장한 파일 삭제
    print("task id--------------")
    print(task_id_predicted)

    print("aaaaaaaa")
    print(task_id_predicted)

    return jsonify(
        task_id=str(task_id_predicted)
    )










