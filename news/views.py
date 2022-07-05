import logging

from django.http import JsonResponse, QueryDict

from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests # HTTP 요청을 보내는 모듈
import datetime # 날짜시간 모듈

from datetime import date, datetime, timedelta # 현재 날짜 외의 날짜 구하기 위한 모듈

from urllib import parse


logger = logging.getLogger(__name__)


@api_view(["GET"])
def WthrWrnList(request):
    
    news_url = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getPwnCd"

    today = datetime.now()
    date = today.strftime("%Y-%m-%d")

    payload = {
        "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
        "dataType": "json",
        "areaCode": "L1100200",
        "warningType": 12 
        # "fromTmFc": date,
        # "toTmFc": date,
    }
    
    # requests package use "encoder" for url in .get method
    # By so, we should use DECODED serviceKey for authenticattion
    # https://brownbears.tistory.com/501
    res = requests.get(news_url, params=payload)
    print(res.url)
    return Response(res.json())


@api_view(["GET"])
def PwnCd(request):
    
    news_url = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getPwnCd"

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    date = today.strftime("%Y-%m-%d")
    yesterday_date = yesterday.strftime("%Y-%m-%d")

    payload = {
        "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
        "dataType": "json",
        # "fromTmFc": yesterday_date,
        # "toTmFc": yesterday_date,
        "areaCode": "L1100200",
        "warningType": 12,
        "stnld": 108
    }
    
    # requests package use "encoder" for url in .get method
    # By so, we should use DECODED serviceKey for authenticattion
    # https://brownbears.tistory.com/501
    res = requests.get(news_url, params=payload)
    print(res.url)
    return Response(res.json())




@api_view(["GET"])
def PwnStatus(request):
    
    news_url = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getPwnStatus"

    payload = {
        "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
        "dataType": "json",
        "numOfRows": 10
    }
    
    # requests package use "encoder" for url in .get method
    # By so, we should use DECODED serviceKey for authenticattion
    # https://brownbears.tistory.com/501
    res = requests.get(news_url, params=payload)
    print(res.url)
    return Response(res.json())