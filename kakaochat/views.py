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


@api_view(["POST", "GET"])
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


@api_view(["POST", "GET"])
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


@api_view(["POST", "GET"])
def UltraSrtNcst(request):
    
    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?"
    
    service_key = "1gBJqXUPjw9pRznJDfyVledJCQop%2B%2BUzpFZhWjhGrMZKjQ305PGGxoTr%2BGSNYpMExVLCQRIsBtI2ccZmKoxK%2Bg%3D%3D"

    today = date.today()
    base_date = today.strftime("%Y%m%d")

    hour = datetime.now().hour - 1
    # TODO by minutes making accurate base_time hour settings needed
    # datetime.now().minute

    if int(hour) < 10:
        base_time = "0" + str(hour) + "00"
    else:
        base_time = str(hour) + "00"

    nx = "61"
    ny = "126"
    
    payload = "serviceKey=" + service_key + "&" +\
                "dataType=json" + "&" +\
                "base_date=" + base_date + "&" +\
                "base_time=" + base_time + "&" +\
                "nx=" + nx + "&" +\
                "ny=" + ny

    res = requests.get(weather_url + payload)


    res_data = res.json()
    items = res_data.get('response').get('body').get('items').get('item')


    pty_dict = {
        "0": "맑음",
        "1": "비",
        "2": "비/눈",
        "3": "눈",
        "5": "빗방울",
        "6": "빗방울눈날림",
        "7": "눈날림",
    }

    results = {}
    results["basetime"] = base_time[:2] + "시"
    for item_dict in items:
        if item_dict.get('category') == "T1H":
            results["temperature"] = item_dict.get('obsrValue') + "°C"
        if item_dict.get('category') == "RN1":
            results["precipitation"] = item_dict.get('obsrValue') +"mm"
        if item_dict.get('category') == "REH":
            results["humidity"] = item_dict.get('obsrValue') + "%"
        if item_dict.get('category') == "PTY":
            obsr_value = item_dict.get('obsrValue')
            results["rain_type"] = pty_dict.get(obsr_value)


    # return Response(end_results)


    message = "기준 시각: " + results["basetime"] + "\n" + "현재 기온: " + results["temperature"] + "\n" +\
              "현재 날씨: " + results["rain_type"] + "\n" + "현재 강수량: " + results["precipitation"] + "\n" +\
              "현재 습도: " + results["humidity"]
    
    # re = []
    # re.append("현재 기온: {0} " + end_results["0000"]["temperature"])
    # re.append("현재 날씨: {1} " + end_results["0000"]["rain_type"])
    # re[2] = "현재 강수량: " + end_results["0000"]["precipitation"]
    # re[3] = "현재 습도: " + end_results["0000"]["humidity"]
    # re.join("/n")
                
    
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": message
                    }
                }
            ]
        }
    }

    return JsonResponse(res)


@api_view(["GET"])
def UltraSrtFcst(request):
    
    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?"
    
    service_key = "1gBJqXUPjw9pRznJDfyVledJCQop%2B%2BUzpFZhWjhGrMZKjQ305PGGxoTr%2BGSNYpMExVLCQRIsBtI2ccZmKoxK%2Bg%3D%3D"

    today = date.today()
    base_date = today.strftime("%Y%m%d")

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
    return Response(res.json())


@api_view(["POST", "GET"])
def VilageFcst(request):
    
    weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"
    
    service_key = "1gBJqXUPjw9pRznJDfyVledJCQop%2B%2BUzpFZhWjhGrMZKjQ305PGGxoTr%2BGSNYpMExVLCQRIsBtI2ccZmKoxK%2Bg%3D%3D"
    
    today = date.today()
    base_date = today.strftime("%Y%m%d")

    base_time = "0700"

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
    return Response(res.json())
    #items = res.json().get('reponse').get('body').get('items')


@api_view(["POST", "GET"])
def template(request):
    res = {
      "version": "2.0",
      "template": {
        "outputs": [
          {
            "listCard": {
              "header": {
                "title": "챗봇 관리자센터를 소개합니다."
              },
              "items": [
                {
                  "title": "챗봇 관리자센터",
                  "description": "새로운 AI의 내일과 일상의 변화",
                  "imageUrl": "http://k.kakaocdn.net/dn/APR96/btqqH7zLanY/kD5mIPX7TdD2NAxgP29cC0/1x1.jpg",
                  "link": {
                    "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                  }
                },
                {
                  "title": "챗봇 관리자센터",
                  "description": "카카오톡 채널 챗봇 만들기",
                  "imageUrl": "http://k.kakaocdn.net/dn/N4Epz/btqqHCfF5II/a3kMRckYml1NLPEo7nqTmK/1x1.jpg",
                  "action": "block",
                  "blockId": "62654c249ac8ed78441532de",
                  "extra": {
                    "key1": "value1",
                    "key2": "value2"
                  }
                },
                {
                  "title": "Kakao i Voice Service",
                  "description": "보이스봇 / KVS 제휴 신청하기",
                  "imageUrl": "http://k.kakaocdn.net/dn/bE8AKO/btqqFHI6vDQ/mWZGNbLIOlTv3oVF1gzXKK/1x1.jpg",
                  "action": "message",
                  "messageText": "Kakao i Voice Service",
                  "extra": {
                    "key1": "value1",
                    "key2": "value2"
                  }
                }
              ],
              "buttons": [
                {
                  "label": "구경가기",
                  "action": "block",
                  "blockId": "62654c249ac8ed78441532de",
                  "extra": {
                    "key1": "value1",
                    "key2": "value2"
                  }
                }
              ]
            }
          }
        ]
      }
    }
    
    return JsonResponse(res)