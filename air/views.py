import logging

from django.http import JsonResponse, QueryDict

from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests # HTTP 요청을 보내는 모듈
import datetime # 날짜시간 모듈

from datetime import date, datetime, timedelta # 현재 날짜 외의 날짜 구하기 위한 모듈

from urllib import parse


logger = logging.getLogger(__name__)


@api_view(["GET", "POST"])
def RltmMesure(request):
    
    air_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
    
    payload = {
        "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
        "stationName": "성동구",
        "dataTerm": "daily",
        "returnType": "json",
        "ver": "1.3",
    }
    
    # requests package use "encoder" for url in .get method
    # By so, we should use DECODED serviceKey for authenticattion
    # https://brownbears.tistory.com/501
    res = requests.get(air_url, params=payload)
    print(res.url)
    return Response(res.json())


@api_view(["GET", "POST"])
def CtprvnRltmMesure(request):
    
    air_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"
    
    payload = {
        "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
        "sidoName": "서울",
        "returnType": "json",
        "ver": "1.3",
    }
    
    # requests package use "encoder" for url in .get method
    # By so, we should use DECODED serviceKey for authenticattion
    # https://brownbears.tistory.com/501
    res = requests.get(air_url, params=payload)
    print(res.url)
    return Response(res.json())


@api_view(["GET", "POST"])
def DustFrcst(request):
    
    air_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth"

    today = datetime.now()
    date = today.strftime("%Y-%m-%d")

    payload = {
        "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
        "returnType": "json",
        "searchDate": date,
        "informCode": "PM10",
    }
    
    # requests package use "encoder" for url in .get method
    # By so, we should use DECODED serviceKey for authenticattion
    # https://brownbears.tistory.com/501
    res = requests.get(air_url, params=payload)
    print(res.url)
    return Response(res.json())


@api_view(["GET", "POST"])
def DustWeekFrcst(request):
    
    air_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustWeekFrcstDspth"

    today = datetime.now()
    date = today.strftime("%Y-%m-%d")

    payload = {
        "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
        "returnType": "json",
        "searchDate": date,
    }
    
    # requests package use "encoder" for url in .get method
    # By so, we should use DECODED serviceKey for authenticattion
    # https://brownbears.tistory.com/501
    res = requests.get(air_url, params=payload)
    print(res.url)
    return Response(res.json())