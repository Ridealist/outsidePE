from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests # HTTP 요청을 보내는 모듈
import json # json 파일 파싱하여 데이터 읽는 모듈
import datetime # 날짜시간 모듈
import pprint

from datetime import date, datetime, timedelta # 현재 날짜 외의 날짜 구하기 위한 모듈

import random

@api_view(["GET"])
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
def weekday():
    week_list = ["월", "화", "수", "목", "금", "토", "일"]
    # 카카오 서버에서 스킬이 보내는 요청 데이터
    request_data = json.loads(requests.get_data(), encoding="utf-8")
    print(request_data)

    # get date parmas
    # 파라미터에서 날짜 파라미터의 값 가져오기(문자열로 되어 있으므로 별도로 json 변환 필요)
    params = request_data['action']['params'] # 파라미터 가져오기
    param_date = json.loads(params['sys_date_params']) # 파라미터 중 날짜 파라미터 가져오기
    print(param_date)

    # 해당 날짜를 (파이썬 날짜/시간 저장형식) datetime 형식으로 저장하기(년도 정보가 없는 겅우 현재 년도 지정)
    date_obj = datetime.datetime(
        int(param_date['year']) if param_date['year'] else datetime.datetime.today().year,
        int(param_date['month']),
        int(param_date['day'])
    )
    
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        # 요일정보를 받아와 글자로 치환하여 출력
                        "text": week_list[date_obj.weekday()] + "요일"
                    }
                }
            ]
        }
    }

    return JsonResponse(res)


@api_view(["GET"])
def VilageFcst(request):
    
    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"
    
    service_key = "1gBJqXUPjw9pRznJDfyVledJCQop%2B%2BUzpFZhWjhGrMZKjQ305PGGxoTr%2BGSNYpMExVLCQRIsBtI2ccZmKoxK%2Bg%3D%3D"
    
    yesterday = date.today() - timedelta(days=1)
    base_date = yesterday.strftime("%Y%m%d")
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


@api_view(["GET"])
def ShrtNcst(request):
    
    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?"
    
    service_key = "1gBJqXUPjw9pRznJDfyVledJCQop%2B%2BUzpFZhWjhGrMZKjQ305PGGxoTr%2BGSNYpMExVLCQRIsBtI2ccZmKoxK%2Bg%3D%3D"
    
    today = date.today()
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
    
    res.json()
    # return JsonResponse(res.json())
    
    return Response(res.json())