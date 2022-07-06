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
    """기상 특보 목록 조회"""
    
    news_url = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getWthrWrnList"

    today = datetime.now()
    date = today.strftime("%Y-%m-%d")

    payload = {
        "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
        "dataType": "json",
        "stnId": 109
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
def WthrWrnMsg(request):
    """기상 특보 통보문 조회"""
    
    news_url = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getWthrWrnMsg"

    today = datetime.now()
    date = today.strftime("%Y-%m-%d")

    payload = {
        "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
        "dataType": "json",
        "stnId": 109
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
def WthrInfo(request):
    """기상 정보문 조회"""
    info_list_url = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getWthrInfoList"
    payload = {
        "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
        "dataType": "json",
        "stnId": 109
        # "fromTmFc": date,
        # "toTmFc": date,
    }

    res_list = requests.get(info_list_url, params=payload)
    print(res_list.url)
    item_list = res_list.json().get("response").get("body").get("items").get("item")

    wthr_news_url = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getWthrInfo"
    payload = {
        "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
        "dataType": "json",
        "stnId": 109
        # "fromTmFc": date,
        # "toTmFc": date,
    }

    res_news = requests.get(wthr_news_url, params=payload)
    print(res_news.url)
    news_list = res_news.json().get("response").get("body").get("items").get("item")

    for i, item in enumerate(item_list):
        item["Info"] = news_list[i]

    return Response(item_list)

@api_view(["GET"])
def PwnCd(request):
    
    news_url = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getPwnCd"

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    date = today.strftime("%Y-%m-%d")
    yesterday_date = yesterday.strftime("%Y-%m-%d")

    warn = "1-강풍, 2-호우, 3-한파, 4-건조, 5-폭풍해일, 6-풍랑, 7-태풍, 8-대설, 9-황사, 12-폭염"
    warn_l = warn.split(",")
    warn_l_c = [word.strip() for word in warn_l]
    warn_dict = {}
    for word in warn_l_c:
        warn_dict[int(word.split("-")[0])] = word.split("-")[1]

    end_result = {}
    for i in warn_dict.keys():
        payload = {
            "serviceKey": "g5Zc7ZwONtAhYmlXEjbbN5OnPGAHEx8u9vPSfJpV+7XGBUR81SrcuRXpegLTnbwzW4nKMRyR0cL+XMqMMd+Tww==",
            "dataType": "json",
            # "fromTmFc": yesterday_date,
            # "toTmFc": yesterday_date,
            "areaCode": "L1100200",
            "warningType": i,
            # "stnld": 109
        }
        
        # requests package use "encoder" for url in .get method
        # By so, we should use DECODED serviceKey for authenticattion
        # https://brownbears.tistory.com/501
        res = requests.get(news_url, params=payload)
        print(res.url)
        try:
            item = res.json().get("response").get("body").get("items").get("item")
        except:
            item = []
        end_result[warn_dict[i]] = item
    return Response(end_result)



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
