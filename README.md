# PHPWeathermap-Viewer

PHP-Weathermap을 Stand-alone으로 동작 시킬 때 웹 상에서 보기 좋게 보여주는 Flask 기반 웹 UI 입니다.

# 사용법
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

즉, 모든 설정이 완료되었을 때 아래와 같은 폴더 구조가 됩니다.

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