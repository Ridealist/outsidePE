from django.http import JsonResponse
from rest_framework.decorators import api_view

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