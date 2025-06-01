#FROM python:3.9 : Python 3.9 기반의 도커 이미지 사용
#WORKDIR /app: 컨테이너 내의 작업 디렉토리를 /app으로 설정
#COPY . /app: 현재 디렉토리와 모든 파일을 /app으로 복사
#RUN pip install --upgrade pip: pip 업그레이드
#RUN pip install -r requirements.txt: 모든 의존성 패키지 설치
#CMD []: 컨테이너 시작할 때 실행할 기본 명령어

FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

COPY requirements.txt .
COPY ./app /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#gunicorn은 보통 앱의 루트 디렉토리를 프로젝트 최상위로 잡기 때문에 app/ 폴더 내에 app.py의 app을 실행한다는 의미.
#따라서 app내에 파일을 import할 때 app. 을 붙여 사용해야 함.
#왜 gunicorn 실행할 때는 app.py처럼 파일을 실행하지 않나 ?
#-> gunicorn이 실행할 wsgi 어플리케이션 객체를 지정하는 것임.
CMD ["gunicorn", "-k", "eventlet", "-w", "2", "-b", "0.0.0.0:5001", "app.app:app"]
#CMD ["python", "app/app.py"]

