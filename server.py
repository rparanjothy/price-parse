import json
import urllib3
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from functools import reduce

app = Flask(__name__)
CORS(app)
http = urllib3.PoolManager()


def getData(x):
    print(x)
    headers = {
        'User-Agent': "PostmanRuntime/7.19.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        # 'Postman-Token': "d062d532-f5ed-4c04-b92c-2f3b76db3164,e6f2726f-dc16-4af7-8ff3-ab6061678dc5",
        # 'Host': "www.homedepot.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    url = 'https://www.homedepot.com/p/svcs/frontEndModel/{0}'.format(str(x))
    try:
        res = requests.request("GET", url, headers=headers)
        # print(res.status_code)
        if res.status_code == 200:
            data = res.json()
            o = {'isOutOfStock': data['inventory'] and data['inventory']['online']['isOutOfStock'],
                 'media': reduce(lambda x, y: y+x, map(lambda x: x['location'], filter(lambda x: x['mediaType'] == 'IMAGE_CATALOG_VIEW' and x['height'] == '300', data['primaryItemData']['media']['mediaList']))),
                 #  'pricing': reduce(lambda x, y: x, map(lambda x: {'dollarOff': x['dollarOff'], 'originalPrice': x['originalPrice'], 'specialPrice': x['specialPrice'], 'percentageOff': x['percentageOff']}, map(lambda x: x['pricing'], filter(lambda x: x['storeId'] == '8119', data['primaryItemData']['storeSkus']))))
                 'pricing': reduce(lambda x, y: x,  map(lambda x: x['pricing'], filter(lambda x: x['storeId'] == '8119', data['primaryItemData']['storeSkus'])))
                 }
            return {'itemid': x, "data": o}
    except Exception as ex:
        print(ex)
        pass


@app.route("/<itemid>")
def getPrice(itemid):
    req = request.args
    if req:
        itemRange = req['d']
        print(itemRange)
        if '-' in itemRange:
            _ = [int(x) for x in itemRange.split("-")]
            return jsonify(list(filter(lambda s: s, map(getData, range(_[0], _[1]+1)))))
        else:
            return jsonify({"msg": "need range in -"})
    else:
        return jsonify({"msg": "need range"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True)
