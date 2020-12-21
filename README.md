# PHPWeathermap-Viewer

PHP-Weathermap을 Stand-alone으로 동작 시킬 때 웹 상에서 보기 좋게 보여주는 Flask 기반 웹 UI 입니다.

## UI 예제
![메인화면](sample/main_1.png)

## MAP 적용 UI 예제
![메인화면](sample/main_2.png)



# 사용법

## 사용을 위한 기본 준비
기본적으로 cacti 및 php-weathermap은 설치되어 있어야 하며, crontab을 통하여 weathermap 이미지가 지속적으로 생성되어야 합니다.

아래는 weathermap 생성 스크립트의 예 입니다.

```
#!/bin/bash

BASE_DIR="[Weathermap 설치 디렉토리]"
OUTPUT_DIR="[Weathermap 이미지 파일 저장 디렉토리]"
CONFIG_DIR="[Weathermap 설정 파일 저장 디렉토리]"

datestamp=`date -I`
timestamp=`date -Iminutes`

mkdir ${OUTPUT_DIR}/${datestamp}

cd ${BASE_DIR}

./weathermap --config ${CONFIG_DIR}/[설정파일 이름] --output ${OUTPUT_DIR}/${datestamp}/${timestamp}.png
```

해당 스크립트에서 이미지 파일 저장 위치는 Flask 폴더 내부 app/static/image 폴더여야 합니다.

즉, 해당 코드를 다운받아서 압축을 푼 후 app/static/image 폴더를 설정해주시면 됩니다. 최종적으로 아래와 같은 디렉토리 구성을 가지게 됩니다.

```
FLASK_ROOT /
           / weathermap.wsgi
           / run.py
           / app /
                 / __init__.py
                 / config.py
                 / static /
                          / css /
                                / main.css 
                          / js /
                               / main.js
                          / image / [년-월-일] / [년-월-일T시:분+09:00.png]    # php weathermap을 통해 생성된 이미지들
                 / template /
                            / index.html
```

## 설정 파일 수정

설정 파일 수정은 간단합니다.
```
FLASK_ROOT / app / config.py
```
파일을 열어 아래와 같이 수정합니다.

```
TITLE = """페이지에 표시될 타이틀"""
IMAGE_PATH = """[FLASK_ROOT]/app/static/image"""
MAP_BASE_URL = """"""
MAP_DATA = []
```

MAP\_BASE\_URL과 MAP\_DATA는 MAP을 사용하여, 그래프를 볼 수 있게 만드는 경우에만 사용합니다.

```
FLASK_ROOT / weathermap.wsgi
```

파일을 열어 아래와 같이 수정합니다.

```
#!/usr/bin/python3
import sys
sys.path.insert(0, "[FLASK_ROOT]")
from app import app as application
```

## 테스트 실행
[FLASK_ROOT]/run.py를 실행합니다.

## MAP을 사용하여 cacti 그래프 보이게 하기

### cacti, guest 사용자 설정하기
cacti 설정화면에서 인증탭으로 이동하여, 일반사용자를 "guest"로 설정합니다.

![cacti 설정 화면](sample/01.png)

### cacti, 사용자 로그아웃하고 그래프 확인하기

먼저 그래프 ID를 알아야 합니다.

cacti 에서 "관리" -> "그래프" 로 들어가서 그래프를 선택하시고 위의 주소창을 보시면

```
http://[cacti 접속주소]/graphs.php?action=graph_edit&id=72
```
를 확인할 수 있습니다. 해당 주소의 마지막 id 값을 확인 합니다. 여기서는 72번 입니다. 확인하셨으면 로그아웃 합니다.

로그아웃 하고 해당 아이디 값을 이용하여 아래 주소를 생성합니다.

```
http://[cacti 접속주소]/graph_image.php?local_graph_id=72
```

위의 링크로 접속하였을 때 아래와 같이 결과가 나오면 정상적으로 설정된 것입니다.

![cacti 로그인 없이 그래프 보기](sample/02.png)