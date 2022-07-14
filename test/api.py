# celery app 생성하는 파일

from flask_cors import CORS
from flask import Flask, jsonify, request

APP = Flask(__name__)

# 일단 모든 도메인에 대해 CORS 설정 (특정 주소/도메인/포트만 사용하게 설정할 수도 있음)
CORS(APP)
CORS(APP, resources={r'*': {'origins': '*'}})


@APP.route('/', methods=['GET'])
def index():
    return jsonify(
        text='Hello, world'
    )


@APP.route('/ct/storeResult', methods=['GET', 'POST'])
def store_result():
    import tasks

    # 로컬에 request에 있는 것 저장
    dcm_file = request.files['file']
    dcm_file_path = dcm_file.filename
    print('dcm_file_path : {}'.format(dcm_file_path))
    # dcm_file.save(dcm_file_path)  # request.filename 이거로 저장하기

    patient_result = request.form['patient_result']
    # print(dcm_file, patient_result)

    task_id_predicted = tasks.get_dcm_predicted.delay(dcm_file_path,
                                                      patient_result)  # 여기서 리턴값 오는 게 아니라 task_id 만 받아올 수 있음. 셀러리에서 pydicom에서 로컬path로 받을수있음. 그 저장한 path를 셀러리로 보냄. 그후 로컬에 저장한 파일 삭제
    print("task id--------------")
    print(task_id_predicted)

    print("aaaaaaaa")
    print(task_id_predicted)

    return jsonify(
        task_id=str(task_id_predicted)
    )


if __name__ == '__main__':
    APP.run(host='0.0.0.0')
