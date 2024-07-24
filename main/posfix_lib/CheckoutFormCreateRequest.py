# coding=utf-8
import json
from main.posfix_lib.Helper import Helper, HttpClient
from xml.etree.ElementTree import Element, SubElement, tostring


class CheckoutFormCreateRequest(object):
    ThreeD = ""
    Amount = ""
    OrderId = ""
    VendorId = ""
    AllowedInstallments = ""
    CallbackUrl = ""
    Purchaser = ""
    Products = ""
    CustField1 = ""
    Echo = ""

    # 3D Secure Olmadan Odeme Servis cagsirini temsil eder.
    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey + req.Mode + req.Purchaser.name + req.Purchaser.surname + \
                             req.Purchaser.email + configs.TransactionDate

        json_data = json.dumps({
            'orderId': req.OrderId,
            'amount': req.Amount,
            'callbackUrl': "https://apitest.posfix.com.tr/rest/payment/threed/test/result",
            'threed': req.ThreeD,
            'allowedInstallments': list({"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"}),  # kontrol et
            'mode': req.Mode,
            'purchaser': {
                'name': req.Purchaser.name,
                'surname': req.Purchaser.surname,
                'email': req.Purchaser.email,
                'clientIp': '127.0.0.1',
                'invoiceAddress': {
                    'name': "Ahmet",
                    'surname': "Veli",
                    'address': "Mevlüt Pehlivan Mah. PosFix Plaza Şişli",
                    'zipcode': "34782",
                    'city': "34",
                    'country': "TR",
                    'tcCertificate': "1234567890",
                    'taxNumber': "9999999999",
                    'taxOffice': "Kozyatağı",
                    'companyName': "PosFix",
                    'phoneNumber': "2122222222"
                },
                'shippingAddress': {
                    'name': "Ahmet",
                    'surname': "Veli",
                    'address': "Mevlüt Pehlivan Mah. PosFix Plaza Şişli",
                    'zipcode': "34782",
                    'city': "34",
                    'country': "TR",
                    'phoneNumber': "2122222222"
                }
            },
            'echo': req.Echo,
            'version': req.Version,
            'transactionDate': configs.TransactionDate,
            'vendorId': "",
            'products': [
                {
                    'productCode': 'Bilgisayar',
                    'productName': 'BLG0001',
                    'quantity': '1',
                    'price': '5000',
                },
                {
                    'productCode': 'TLF0001',
                    'productName': 'Telefon',
                    'quantity': '1',
                    'price': '5000',
                },
            ],
        })

        result = HttpClient.post(configs.BaseUrl + "rest/checkoutForm/create",
                                 helper.GetHttpHeaders(
                                     configs, helper.Application_json),
                                 json_data)

        return result

    class PurchaserClass:
        name = ""
        surname = ""
        birthDate = ""
        email = ""
        gsmPhone = ""
        tcCertificate = ""
        clientIp = ""
        invoiceAddress = ""
        shippingAddress = ""
