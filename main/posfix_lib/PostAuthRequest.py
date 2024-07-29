# coding=utf-8
import json
from main.posfix_lib.Helper import Helper, HttpClient
from xml.etree.ElementTree import Element, SubElement, tostring


class PostAuthRequest(object):
    OrderId = ""
    Amount = ""
    ClientIp = ""
    Mode = ""

    # Ön Otorizasyon Kapama Servis cagrisini temsil eder.
    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey + req.OrderId + req.Amount + req.Mode + \
                             req.ClientIp + configs.TransactionDate

        json_data = json.dumps({
            'orderId': req.OrderId,
            'amount': req.Amount,
            'mode': req.Mode,
            'clientIp': req.ClientIp
        })

        result = HttpClient.post(configs.BaseUrl + "rest/payment/postauth",
                                 helper.GetHttpHeaders(
                                     configs, helper.Application_json),
                                 json_data)

        return result
