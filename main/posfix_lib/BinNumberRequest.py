# coding=utf-8
import json

from main.posfix_lib.Helper import Helper, HttpClient
from main.posfix_lib.configs import Configs


class BinNumberRequest:
    # Bin Sorgulama servisleri içerisinde kullanılacak olan bin numarasını temsil eder.
    binNumber = ""
    amount = ""
    threeD = ""

    def __init__(self):
        pass

    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey+req.binNumber+configs.TransactionDate

        json_data = json.dumps(req.__dict__)  # Json Serilestirme

        result = HttpClient.post(configs.BaseUrl+"/rest/payment/bin/lookup/v2",
                                 helper.GetHttpHeaders(configs, helper.Application_json), json_data)
        return result
