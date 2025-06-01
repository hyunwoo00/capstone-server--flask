from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from app.cache import init_cache
from app.openai_api import call_openAi
from app.yamnet import model_output
from app.routes import main as main_blueprint
import numpy as np
import json

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins="*") # cors 허용

#blueprint 등록(다른 파일에 http routes 정리)
app.register_blueprint(main_blueprint)

@socket.on('test')
def socket_test(data):
    socket.emit('data_response', {"message": "완료"})

@socket.on('audio')
def handle_audio(audio_data):
    #이미지 데이터 전처리
    wav = np.array(audio_data, dtype=np.float32)

    #yamnet 모델 실행
    label, category = model_output(wav)

    if category != -1:
        socket.emit('audio_response', {"label": label, "category": category})

@socket.on('screenshot')
def handle_openAi(request):
    if isinstance(request, str):  # 문자열이면 JSON 파싱
        request = json.loads(request)
    
    print("요청: ", request)

    img_data = request["image"]
    label = request["label"]
    
    result = call_openAi(img_data, label)
    
    socket.emit('gpt_response', {"suggestion":result, "label": label})

if __name__ == '__main__':
    host='0.0.0.0'
    port=5001
    socket.run(app, host='0.0.0.0', port=port)