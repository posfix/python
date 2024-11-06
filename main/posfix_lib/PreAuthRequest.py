# coding=utf-8
import json
from main.posfix_lib.Helper import Helper, HttpClient
from xml.etree.ElementTree import Element, SubElement, tostring


class PreAuthRequest(object):
    Echo = ""
    Mode = ""
    ThreeD = ""
    OrderId = ""
    Amount = ""
    CardOwnerName = ""
    CardNumber = ""
    CardExpireMonth = ""
    CardExpireYear = ""
    Installment = ""
    Cvc = ""
    VendorId = ""
    UserId = ""
    CardId = ""
    ThreeDSecureCode = ""
    Products = ""
    Purchaser = ""
    Version = ""

    # 3D Secure Olmadan Odeme Servis cagsirini temsil eder.
    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey + req.OrderId + req.Amount + req.Mode + \
                             req.CardOwnerName + req.CardNumber + req.CardExpireMonth + req.CardExpireYear + \
                             req.Cvc + req.UserId + req.CardId + req.Purchaser.name + req.Purchaser.surname + \
                             req.Purchaser.email + configs.TransactionDate

        json_data = json.dumps({
            'orderId': req.OrderId,
            'cardOwnerName': req.CardOwnerName,
            'cardNumber': req.CardNumber,
            'cardExpireMonth': req.CardExpireMonth,
            'cardExpireYear': req.CardExpireYear,
            'cardCvc': req.Cvc,
            'userId': req.UserId,
            'cardId': req.CardId,
            'installment': '1',
            'amount': req.Amount,
            'echo': '',
            'language': 'tr-TR',
            'purchaser': {
                'name': req.Purchaser.name,
                'surname': req.Purchaser.surname,
                'email': req.Purchaser.email,
                'clientIp': '127.0.0.1',
            },
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
            'mode': req.Mode,
            'version': req.Version,
            'transactionDate': configs.TransactionDate,
        })

        result = HttpClient.post(configs.BaseUrl + "rest/payment/preauth",
                                 helper.GetHttpHeaders(
                                     configs, helper.Application_json),
                                 json_data)

        return result

    # Bu sınıf cüzdana kart ekleme servisi isteği sonucunda ve cüzdandaki kartları getir
    # isteği sonucunda bize döndürülen alanları temsil eder.
    class BankCard:
        cardId = ""
        maskNumber = ""
        alias = ""
        bankId = ""
        bankName = ""
        cardFamilyName = ""
        supportsInstallment = ""
        supportedInstallments = ""
        Type = ""
        serviceProvider = ""
        threeDSecureMandatory = ""
        cvcMandatory = ""

        def __init__(self):
            pass

    # Bu sınıf 3D secure olmadan ödeme kısmında ürün bilgisinin kullanılacağı yerde
    # ve 3D secure ile ödemenin 2. adamında ürün bilgisinin istendiği yerde kullanılır.
    class PurchaserAddress:
        name = ""
        surname = ""
        address = ""
        zipCode = ""
        cityCode = ""
        tcCertificate = ""
        country = ""
        taxNumber = ""
        taxOffice = ""
        companyName = ""
        phoneNumber = ""

        def __init__(self):
            pass

    # Bu sınıf 3D secure olmadan ödeme kısmında ürün bilgisinin kullanılacağı yerde
    # ve 3D secure ile ödemenin 2. adamında ürün bilgisinin istendiği yerde kullanılır.
    class Product:
        code = ""
        title = ""
        quantity = ""
        price = ""

    # Bu sınıf 3D secure olmadan ödeme kısmında ürün bilgisinin kullanılacağı yerde
    # ve 3D secure ile ödemenin 2. adamında ürün bilgisinin istendiği yerde kullanılır.

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

    # Bu sınıf 3D Secure ile Ödeme işlemlerinin 1. ve 2. adımında kullanılan parametreleri temsil eder.

    class PosFixAuth:
        threeD = ""
        orderId = ""
        amount = ""
        echo = ""
        cardOwnerName = ""
        cardNumber = ""
        cardExpireYear = ""
        installment = ""
        cvc = ""
        mode = ""
        vendorId = ""
        threeDSecureCode = ""
        products = ""
        purchaser = ""
