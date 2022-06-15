from django.http import JsonResponse
from rest_framework.decorators import api_view

import requests # HTTP 요청을 보내는 모듈
import json # json 파일 파싱하여 데이터 읽는 모듈
import datetime # 날짜시간 모듈

from datetime import date, datetime, timedelta # 현재 날짜 외의 날짜 구하기 위한 모듈

import random

@api_view(["GET", "POST"])
def random_function(request):
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(random.randint(1,10))
                    }
                }
            ]
        }
    }
    return JsonResponse(res)


@api_view(["GET", "POST"])
def weather(request):
    
    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"
    
    service_key = "1gBJqXUPjw9pRznJDfyVledJCQop%2B%2BUzpFZhWjhGrMZKjQ305PGGxoTr%2BGSNYpMExVLCQRIsBtI2ccZmKoxK%2Bg%3D%3D"
    
    today = datetime.today()
    base_date = today.strftime("%Y%m%d")
    base_time = "0800"

    nx = "61"
    ny = "126"
    
    payload = "serviceKey=" + service_key + "&" +\
                "dataType=json" + "&" +\
                "base_date=" + base_date + "&" +\
                "base_time=" + base_time + "&" +\
                "nx=" + nx + "&" +\
                "ny=" + ny
                
    res = requests.get(weather_url + payload)
    
    print(res)
    return JsonResponse(res.json())
    #items = res.json().get('reponse').get('body').get('items')
