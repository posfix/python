# coding=utf-8
import json
from main.posfix_lib.Helper import Helper, HttpClient

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

    # Ön Otorizasyon Açma Servis cagrisini temsil eder.
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

    class Product:
        code = ""
        title = ""
        quantity = ""
        price = ""

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
