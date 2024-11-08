# coding=utf-8
import json

from main.posfix_lib.Helper import Helper, HttpClient


class BinNumberV4Request:
    # Bin Sorgulama v4 servisleri içerisinde kullanılacak olan bin numarasını temsil eder.
    binNumber = ""
    amount = ""
    threeD = ""

    def __init__(self):
        pass

    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey + req.binNumber + configs.TransactionDate

        json_data = json.dumps(req.__dict__)  # Json Serilestirme

        result = HttpClient.post(configs.BaseUrl + "/rest/payment/bin/lookup/v4",
                                 helper.GetHttpHeaders(configs, helper.Application_json), json_data)
        return result
