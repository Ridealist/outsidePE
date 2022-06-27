import logging

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests # HTTP 요청을 보내는 모듈
import json # json 파일 파싱하여 데이터 읽는 모듈
import datetime # 날짜시간 모듈

from datetime import date, datetime, timedelta # 현재 날짜 외의 날짜 구하기 위한 모듈

import random


logger = logging.getLogger(__name__)


@api_view(["POST"])
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


@api_view(["POST"])
def weekday(request):
    week_list = ["월", "화", "수", "목", "금", "토", "일"]
    # 카카오 서버에서 스킬이 보내는 요청 데이터
    req = ((request.body).decode('utf-8'))
    request_data = json.loads(req)
    print(request_data)

    # get date parmas
    # 파라미터에서 날짜 파라미터의 값 가져오기(문자열로 되어 있으므로 별도로 json 변환 필요)
    date = request_data['action']['params']['date'] # 파라미터 가져오기
    # param_date = json.loads(params['sys_date_params'])

    try:
        idx_y = date.find("년")
        param_year = date[:idx_y]
    except:
        param_year = datetime.today().year
    idx_m = date.find("월")
    param_month = date[(idx_m - 2):idx_m].strip()
    idx_d = date.find("일")
    param_day = date[(idx_d - 2):idx_d].strip()
    
    # 해당 날짜를 (파이썬 날짜/시간 저장형식) datetime 형식으로 저장하기(년도 정보가 없는 겅우 현재 년도 지정)
    date_obj = date(
        int(param_year),
        int(param_month),
        int(param_day)
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
def UltraSrtNcst(request):
    
    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?"
    
    service_key = "1gBJqXUPjw9pRznJDfyVledJCQop%2B%2BUzpFZhWjhGrMZKjQ305PGGxoTr%2BGSNYpMExVLCQRIsBtI2ccZmKoxK%2Bg%3D%3D"

    today = date.today()
    base_date = today.strftime("%Y%m%d")

    hour = datetime.now().hour
    # TODO by minutes making accurate base_time hour settings needed
    minute = datetime.now().minute

    if minute >= 45:
        h = hour + 1
    else:
        h = hour

    end_results = {}
    for i in range(h):
        if i < 10:
            base_time = "0" + str(i) + "00"
        else:
            base_time = str(i) + "00"

        nx = "61"
        ny = "126"
        
        payload = "serviceKey=" + service_key + "&" +\
                    "dataType=json" + "&" +\
                    "base_date=" + base_date + "&" +\
                    "base_time=" + base_time + "&" +\
                    "nx=" + nx + "&" +\
                    "ny=" + ny
                    
        res = requests.get(weather_url + payload)
        items = res.json().get('response').get('body').get('items').get('item')


        pty_dict = {
            "0": "없음",
            "1": "비",
            "2": "비/눈",
            "3": "눈",
            "5": "빗방울",
            "6": "빗방울눈날림",
            "7": "눈날림",
        }

        result = {}
        for item_dict in items:
            if item_dict.get('category') == "T1H":
                result["temperature"] = item_dict.get('obsrValue') + "°C"
            if item_dict.get('category') == "RN1":
                result["precipitation"] = item_dict.get('obsrValue') +"mm"
            if item_dict.get('category') == "REH":
                result["humidity"] = item_dict.get('obsrValue') + "%"
            if item_dict.get('category') == "PTY":
                obsr_value = item_dict.get('obsrValue')
                result["rain_type"] = pty_dict.get(obsr_value)

        end_results[base_time] = result

    return Response(end_results)

    # res = {
    #     "version": "2.0",
    #     "template": {
    #         "outputs": [
    #             {
    #                 "simpleText": {
    #                     "text": "weather for now: " + end_results["0000"]["temperature"]
    #                 }
    #             }
    #         ]
    #     }
    # }

    # return JsonResponse(res)



@api_view(["GET"])
def UltraSrtFcst(request):

    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?"
    
    service_key = "1gBJqXUPjw9pRznJDfyVledJCQop%2B%2BUzpFZhWjhGrMZKjQ305PGGxoTr%2BGSNYpMExVLCQRIsBtI2ccZmKoxK%2Bg%3D%3D"

    today = date.today()
    # yesterday = datetime.today() - timedelta(days=1)
    base_date = today.strftime("%Y%m%d")
    # base_date = yesterday.strftime("%Y%m%d")

    hour = datetime.now().hour
    minute = datetime.now().minute

    if minute >= 50:
        h = hour
    else:
        h = hour - 1

    if h < 10:
        base_time = "0" + str(h) + "30"
    else:
        base_time = str(h) + "30"

    # 행당동 coordinate
    nx = "61"
    ny = "126"

    payload = "serviceKey=" + service_key + "&" +\
                "dataType=json" + "&" +\
                "base_date=" + base_date + "&" +\
                "base_time=" + base_time + "&" +\
                "nx=" + nx + "&" +\
                "ny=" + ny + "&" +\
                "numOfRows=60"

    res = requests.get(weather_url + payload)
    # return Response(res.json())

    items_dict_list = res.json().get('response').get('body').get('items').get('item')

    # time_list = []
    # for i in range(7):
    #     fcst_h = h + i
    #     if fcst_h < 10:
    #         fcst_time = "0" + str(fcst_h) + "00"
    #     else:
    #         fcst_time = str(fcst_h) + "00"
    # time_list.append(fcst_time)

    pty_dict = {
        "0": "없음",
        "1": "비",
        "2": "비/눈",
        "3": "눈",
        "5": "빗방울",
        "6": "빗방울눈날림",
        "7": "눈날림",
    }

    sky_dict = {
        "1": "맑음",
        "2": "구름조금",
        "3": "구름많음",
        "4": "흐림",
    }

    result = {}

    for item_dict in items_dict_list:
        time = item_dict.get('fcstTime')
        result[time] = dict()

    for item_dict in items_dict_list:
        time = item_dict.get('fcstTime')
        if item_dict.get('category') == "T1H":
            result[time]["temperature"] = item_dict.get('fcstValue') + "°C"

        elif item_dict.get('category') == "RN1":
            result[time]["precipitation"] = item_dict.get('fcstValue')

        elif item_dict.get('category') == "SKY":
            obsr_value = item_dict.get('fcstValue')
            result[time]["atomosphere"] = sky_dict.get(obsr_value)

        elif item_dict.get('category') == "PTY":
            obsr_value = item_dict.get('fcstValue')
            result[time]["rain_type"] = pty_dict.get(obsr_value)

    return Response(result)


@api_view(["GET"])
def VilageFcst(request):
    
    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"
    
    service_key = "1gBJqXUPjw9pRznJDfyVledJCQop%2B%2BUzpFZhWjhGrMZKjQ305PGGxoTr%2BGSNYpMExVLCQRIsBtI2ccZmKoxK%2Bg%3D%3D"
    
    today = date.today()
    base_date = today.strftime("%Y%m%d")

    base_time = "0500"

    nx = "61"
    ny = "126"

    payload = "serviceKey=" + service_key + "&" +\
                "dataType=json" + "&" +\
                "base_date=" + base_date + "&" +\
                "base_time=" + base_time + "&" +\
                "nx=" + nx + "&" +\
                "ny=" + ny + "&" +\
                "numOfRows=809"
                
    res = requests.get(weather_url + payload)
    # return Response(res.json())

    items_dict_list = res.json().get('response').get('body').get('items').get('item')

    pty_dict = {
        "0": "없음",
        "1": "비",
        "2": "비/눈",
        "3": "눈",
        "4": "소나기",
    }

    sky_dict = {
        "1": "맑음",
        "2": "구름조금",
        "3": "구름많음",
        "4": "흐림",
    }

    result = {}
    result["baseDate"] = base_date
    result["baseTime"] = base_time
    # result["fcstTime"] = []

    for item_dict in items_dict_list:
        time = item_dict.get('fcstTime')
        result[time] = dict()

    for item_dict in items_dict_list:
        time = item_dict.get('fcstTime')
        if item_dict.get('category') == "POP":
            result[time]["rain_prob"] = item_dict.get('fcstValue') + "%"

        elif item_dict.get('category') == "PTY":
            obsr_value = item_dict.get('fcstValue')
            result[time]["rain_type"] = pty_dict.get(obsr_value)

        elif item_dict.get('category') == "PCP":
            result[time]["1h_precipitation"] = item_dict.get('fcstValue')

        elif item_dict.get('category') == "SKY":
            obsr_value = item_dict.get('fcstValue')
            result[time]["atomosphere"] = sky_dict.get(obsr_value)

        elif item_dict.get('category') == "TMP":
            result[time]["1h_temp"] = item_dict.get('fcstValue') + "°C"

        elif item_dict.get('category') == "TMX":
            result[time]["highest_temp"] = item_dict.get('fcstValue') + "°C"

        elif item_dict.get('category') == "TMN":
            result[time]["lowest_temp"] = item_dict.get('fcstValue') + "°C"

    return Response(result)
