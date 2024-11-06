# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render

from main.posfix_lib.configs import Configs
from main.posfix_lib.Helper import Helper
from main.posfix_lib.BankCardDeleteRequest import BankCardDeleteRequest
from main.posfix_lib.BankCardInquiryRequest import BankCardInquiryRequest
from main.posfix_lib.BinNumberRequest import BinNumberRequest
from main.posfix_lib.BinNumberV4Request import BinNumberV4Request
from main.posfix_lib.BankCardCreateRequest import BankCardCreateRequest
from main.posfix_lib.PaymentInquiryRequest import PaymentInquiryRequest
from main.posfix_lib.PaymentInquiryWithTimeRequest import PaymentInquiryWithTimeRequest
from main.posfix_lib.PaymentLinkDeleteRequest import PaymentLinkDeleteRequest
from main.posfix_lib.PaymentLinkCreateRequest import PaymentLinkCreateRequest
from main.posfix_lib.PaymentLinkInquiryRequest import PaymentLinkInquiryRequest
from main.posfix_lib.PaymentRefundInquiryRequest import PaymentRefundInquiryRequest
from main.posfix_lib.PaymentRefundRequest import PaymentRefundRequest
from main.posfix_lib.ThreedPaymentRequest import ThreedPaymentRequest
from main.posfix_lib.NonThreeDPaymentRequest import NonThreeDPaymentRequest
from main.posfix_lib.PreAuthRequest import PreAuthRequest
from main.posfix_lib.PostAuthRequest import PostAuthRequest
from main.posfix_lib.CheckoutFormCreateRequest import CheckoutFormCreateRequest
from random import randint
import json

config = Configs(
    # "Public Magaza Anahtarı
    # size mağaza başvurunuz sonucunda gönderilen public key (açık anahtar) bilgisini kullanınız.",
    '',
    # "Private Magaza Anahtarı
    # size mağaza başvurunuz sonucunda gönderilen privaye key (gizli anahtar) bilgisini kullanınız.",
    '',
    # PosFix web servisleri API url'lerinin başlangıç bilgisidir.
    # Restful web servis isteklerini takip eden kodlar halinde bulacaksınız.
    'https://api.posfix.com.tr/',  # BaseUrl
    # Test -> T, entegrasyon testlerinin sırasında "T" modunu,
    # canlı sisteme entegre olarak ödeme almaya başlamak için ise Prod -> "P" modunu kullanınız.
    'T',  # Mode
    '',  # Echo
    #  Kullandığınız PosFix API versiyonudur.
    '1.0',  # Version
    # Kullanacağınız hash bilgisini, bağlanmak istediğiniz web servis bilgisine göre doldurulmalıdır.
    # Bu bilgileri Entegrasyon rehberinin ilgili web servise ait bölümde bulabilirsiniz.
    '',  # HashString
    '',  # TransactionDate
)


# Ana Sayfamızda Ön Tanımlı Olarak 3D Ödeme Kısmı Gelmekte


def threedPaymentRequest(request):
    message = ""
    if request.POST:
        req = ThreedPaymentRequest()
        req.OrderId = str(randint(1, 10000))
        req.Echo = "Echo"
        req.Mode = config.Mode
        req.Version = config.Version
        req.Amount = request.POST.get('amount')
        req.CardOwnerName = request.POST.get('nameSurname')
        req.CardNumber = request.POST.get('cardNumber')
        req.CardExpireMonth = request.POST.get('month')
        req.CardExpireYear = request.POST.get('year')
        req.Installment = request.POST.get('installment')
        req.Cvc = request.POST.get('cvc')
        req.ThreeD = "true"
        req.UserId = ""
        req.CardId = ""
        req.PurchaserName = "Ahmet"
        req.PurchaserSurname = "Veli"
        req.PurchaserEmail = "ahmet@veli.com"
        req.SuccessUrl = "https://apitest.posfix.com.tr/rest/payment/threed/test/result"
        req.FailUrl = "https://apitest.posfix.com.tr/rest/payment/threed/test/result"

        # 3D formunun başlatılması için istek çağrısının yapıldığı kısımdır.
        message = req.execute(req, config)
    return render(None, 'index.html', {'message': message})


def preAuthRequest(request):
    message = ""
    if request.POST:
        preAuthRequest = PreAuthRequest()
        preAuthRequest.Echo = "Echo"
        preAuthRequest.Mode = config.Mode
        preAuthRequest.ThreeD = "false"
        preAuthRequest.Version = "1.0"
        preAuthRequest.OrderId = str(randint(1, 10000))
        preAuthRequest.Amount = request.POST.get('amount')
        preAuthRequest.CardOwnerName = request.POST.get('nameSurname')
        preAuthRequest.CardNumber = request.POST.get('cardNumber')
        preAuthRequest.CardExpireMonth = request.POST.get('month')
        preAuthRequest.CardExpireYear = request.POST.get('year')
        preAuthRequest.Installment = request.POST.get('installment')
        preAuthRequest.Cvc = request.POST.get('cvc')
        preAuthRequest.VendorId = ""
        preAuthRequest.UserId = ""
        preAuthRequest.CardId = ""
        preAuthRequest.ThreeDSecureCode = ""

        preAuthRequest.Purchaser = preAuthRequest.PurchaserClass()
        preAuthRequest.Purchaser.name = "Ahmet"
        preAuthRequest.Purchaser.surname = "Veli"
        preAuthRequest.Purchaser.birthDate = "1986-07-11"
        preAuthRequest.Purchaser.email = "mura@Veli.com"
        preAuthRequest.Purchaser.gsmPhone = "5881231212"
        preAuthRequest.Purchaser.tcCertificate = "58812312547"
        preAuthRequest.Purchaser.clientIp = "127.0.0.1"

        # Fatura Bilgileri
        preAuthRequest.Purchaser.invoiceAddress = preAuthRequest.PurchaserAddress()
        preAuthRequest.Purchaser.invoiceAddress.name = "Ahmet"
        preAuthRequest.Purchaser.invoiceAddress.surname = "Veli"
        preAuthRequest.Purchaser.invoiceAddress.address = "Mevlut Pehlivan Mah. PosFix Plaza Sisli"
        preAuthRequest.Purchaser.invoiceAddress.zipCode = "34782"
        preAuthRequest.Purchaser.invoiceAddress.cityCode = "34"
        preAuthRequest.Purchaser.invoiceAddress.tcCertificate = "1234567890"
        preAuthRequest.Purchaser.invoiceAddress.country = "TR"
        preAuthRequest.Purchaser.invoiceAddress.taxNumber = "123456"
        preAuthRequest.Purchaser.invoiceAddress.taxOffice = "Kozyatagi"
        preAuthRequest.Purchaser.invoiceAddress.companyName = "PosFix"
        preAuthRequest.Purchaser.invoiceAddress.phoneNumber = "2122222222"

        # Kargo Bilgileri
        preAuthRequest.Purchaser.shippingAddress = preAuthRequest.PurchaserAddress()
        preAuthRequest.Purchaser.shippingAddress.name = "Ahmet"
        preAuthRequest.Purchaser.shippingAddress.surname = "Veli"
        preAuthRequest.Purchaser.shippingAddress.address = "Mevlut Pehlivan Mah. PosFix Plaza Sisli"
        preAuthRequest.Purchaser.shippingAddress.zipCode = "34782"
        preAuthRequest.Purchaser.shippingAddress.cityCode = "34"
        preAuthRequest.Purchaser.shippingAddress.tcCertificate = "1234567890"
        preAuthRequest.Purchaser.shippingAddress.country = "TR"
        preAuthRequest.Purchaser.shippingAddress.phoneNumber = "2122222222"

        # Ürün Bilgileri
        preAuthRequest.Products = []
        product1 = preAuthRequest.Product()
        product1.title = "Telefon"
        product1.code = "TLF0001"
        product1.price = "5000"
        product1.quantity = "1"
        preAuthRequest.Products.append(product1)

        product2 = preAuthRequest.Product()
        product2.title = "Bilgisayar"
        product2.code = "BLG0001"
        product2.price = "5000"
        product2.quantity = "1"
        preAuthRequest.Products.append(product2)

        # API Cagrisi Yapiyoruz
        response = preAuthRequest.execute(preAuthRequest, config)
        message = json.dumps(json.loads(response), indent=4, ensure_ascii=False)

    return render(None, 'preAuth.html', {'message': message})


# Non-3D Ödeme Yaptığımız Kısım


def nonThreeDPaymentRequest(request):
    message = ""
    if request.POST:
        non3DPaymentRequest = NonThreeDPaymentRequest()
        non3DPaymentRequest.Echo = "Echo"
        non3DPaymentRequest.Mode = config.Mode
        non3DPaymentRequest.ThreeD = "false"
        non3DPaymentRequest.OrderId = str(randint(1, 10000))
        non3DPaymentRequest.Amount = request.POST.get('amount')
        non3DPaymentRequest.CardOwnerName = request.POST.get('nameSurname')
        non3DPaymentRequest.CardNumber = request.POST.get('cardNumber')
        non3DPaymentRequest.CardExpireMonth = request.POST.get('month')
        non3DPaymentRequest.CardExpireYear = request.POST.get('year')
        non3DPaymentRequest.Installment = request.POST.get('installment')
        non3DPaymentRequest.Cvc = request.POST.get('cvc')
        non3DPaymentRequest.VendorId = ""
        non3DPaymentRequest.UserId = ""
        non3DPaymentRequest.CardId = ""
        non3DPaymentRequest.ThreeDSecureCode = ""

        non3DPaymentRequest.Purchaser = non3DPaymentRequest.PurchaserClass()
        non3DPaymentRequest.Purchaser.name = "Ahmet"
        non3DPaymentRequest.Purchaser.surname = "Veli"
        non3DPaymentRequest.Purchaser.birthDate = "1986-07-11"
        non3DPaymentRequest.Purchaser.email = "mura@Veli.com"
        non3DPaymentRequest.Purchaser.gsmPhone = "5881231212"
        non3DPaymentRequest.Purchaser.tcCertificate = "58812312547"
        non3DPaymentRequest.Purchaser.clientIp = "127.0.0.1"

        # Fatura Bilgileri
        non3DPaymentRequest.Purchaser.invoiceAddress = non3DPaymentRequest.PurchaserAddress()
        non3DPaymentRequest.Purchaser.invoiceAddress.name = "Ahmet"
        non3DPaymentRequest.Purchaser.invoiceAddress.surname = "Veli"
        non3DPaymentRequest.Purchaser.invoiceAddress.address = "Mevlut Pehlivan Mah. PosFix Plaza Sisli"
        non3DPaymentRequest.Purchaser.invoiceAddress.zipCode = "34782"
        non3DPaymentRequest.Purchaser.invoiceAddress.cityCode = "34"
        non3DPaymentRequest.Purchaser.invoiceAddress.tcCertificate = "1234567890"
        non3DPaymentRequest.Purchaser.invoiceAddress.country = "TR"
        non3DPaymentRequest.Purchaser.invoiceAddress.taxNumber = "123456"
        non3DPaymentRequest.Purchaser.invoiceAddress.taxOffice = "Kozyatagi"
        non3DPaymentRequest.Purchaser.invoiceAddress.companyName = "PosFix"
        non3DPaymentRequest.Purchaser.invoiceAddress.phoneNumber = "2122222222"

        # Kargo Bilgileri
        non3DPaymentRequest.Purchaser.shippingAddress = non3DPaymentRequest.PurchaserAddress()
        non3DPaymentRequest.Purchaser.shippingAddress.name = "Ahmet"
        non3DPaymentRequest.Purchaser.shippingAddress.surname = "Veli"
        non3DPaymentRequest.Purchaser.shippingAddress.address = "Mevlut Pehlivan Mah. PosFix Plaza Sisli"
        non3DPaymentRequest.Purchaser.shippingAddress.zipCode = "34782"
        non3DPaymentRequest.Purchaser.shippingAddress.cityCode = "34"
        non3DPaymentRequest.Purchaser.shippingAddress.tcCertificate = "1234567890"
        non3DPaymentRequest.Purchaser.shippingAddress.country = "TR"
        non3DPaymentRequest.Purchaser.shippingAddress.phoneNumber = "2122222222"

        # Ürün Bilgileri
        non3DPaymentRequest.Products = []
        product1 = non3DPaymentRequest.Product()
        product1.title = "Telefon"
        product1.code = "TLF0001"
        product1.price = "5000"
        product1.quantity = "1"
        non3DPaymentRequest.Products.append(product1)

        product2 = non3DPaymentRequest.Product()
        product2.title = "Bilgisayar"
        product2.code = "BLG0001"
        product2.price = "5000"
        product2.quantity = "1"
        non3DPaymentRequest.Products.append(product2)

        # API Cagrisi Yapiyoruz
        message = Helper.formatXML(
            non3DPaymentRequest.execute(non3DPaymentRequest, config))

    return render(None, 'nonThreeDPayment.html', {'message': message})


def postAuthRequest(request):
    message = ""
    if request.POST:
        postAuthRequest = PostAuthRequest()
        postAuthRequest.Mode = config.Mode
        postAuthRequest.OrderId = request.POST.get('orderId')
        postAuthRequest.Amount = request.POST.get('amount')
        postAuthRequest.ClientIp = "127.0.0.1"
        # API Cagrisi Yapiyoruz
        response = postAuthRequest.execute(postAuthRequest, config)
        message = json.dumps(json.loads(response), indent=4, ensure_ascii=False)

    return render(None, 'postAuth.html', {'message': message})


# Ödeme Sorguladığımız Kısım


def paymentInquiryRequest(request):
    message = ""
    if request.POST:
        req = PaymentInquiryRequest()
        req.orderId = request.POST.get('orderId')

        # ödeme sorgulama servisi api çağrısının yapıldığı kısımdır.
        message = Helper.formatXML(req.execute(req, config))

    return render(None, 'paymentInquiry.html', {'message': message})


# Ödemeleri Zamana Göre Sorguladığımız Kısım


def paymentInquiryWithTimeRequest(request):
    message = ""
    if request.POST:
        req = PaymentInquiryWithTimeRequest()
        req.mode = config.Mode
        req.echo = config.Echo
        req.startDate = request.POST.get(
            'startYear') + "-" + request.POST.get(
            'startMonth') + "-" + request.POST.get('startDay') + " 00:00:00"
        req.endDate = request.POST.get(
            'endYear') + "-" + request.POST.get(
            'endMonth') + "-" + request.POST.get('endDay') + " 00:00:00"

        response = req.execute(req, config)
        message = json.dumps(json.loads(response),
                             indent=4, ensure_ascii=False)

    return render(None, 'paymentInquiryWithTime.html', {'message': message})


# Bin İsteği Yaptığımız Kısım


def binRequest(request):
    message = ""
    if request.POST:
        req = BinNumberRequest()
        req.binNumber = request.POST.get('binNumber')
        req.amount = request.POST.get('amount')
        req.threeD = request.POST.get('threeD')

        # Bin istegi icin yapılan API cagrisini temsil etmektedir
        response = req.execute(req, config)
        message = json.dumps(json.loads(response),
                             indent=4, ensure_ascii=False)

    return render(None, 'bininqury.html', {'message': message})


# Bin İsteği Yaptığımız Kısım


def binV4Request(request):
    message = ""
    if request.POST:
        req = BinNumberV4Request()
        req.binNumber = request.POST.get('binNumber')
        req.amount = request.POST.get('amount')
        req.threeD = request.POST.get('threeD')

        # Bin istegi icin yapılan API cagrisini temsil etmektedir
        response = req.execute(req, config)
        message = json.dumps(json.loads(response),
                             indent=4, ensure_ascii=False)

    return render(None, 'bininquryv4.html', {'message': message})


# Cüzdana Kart Eklediğimiz Kısım


def addCartToWallet(request):
    message = ""
    if request.POST:
        req = BankCardCreateRequest()
        req.userId = request.POST.get('userId')
        req.cardOwnerName = request.POST.get('nameSurname')
        req.cardNumber = request.POST.get('cardNumber')
        req.cardAlias = request.POST.get('cardAlias')
        req.cardExpireMonth = request.POST.get('month')
        req.cardExpireYear = request.POST.get('year')
        req.clientIp = "127.0.0.1"

        # Cüzdana kart eklemek için yapılan API cagrisini temsil etmektedir
        response = req.execute(req, config)
        message = json.dumps(json.loads(response),
                             indent=4, ensure_ascii=False)

    return render(None, 'addCartToWallet.html', {'message': message})


# Cüzdandaki Kartları Listelediğimiz Kısım


def getCardFromWallet(request):
    message = ""
    if request.POST:
        req = BankCardInquiryRequest()
        req.userId = request.POST.get('userId')
        req.cardId = request.POST.get('cardId')
        req.clientIp = "127.0.0.1"

        # Cüzdandan kartların getirildiği API cagrisini temsil etmektedir
        response = req.execute(req, config)
        message = json.dumps(json.loads(response),
                             indent=4, ensure_ascii=False)

    return render(None, 'getCardFromWallet.html', {'message': message})


# Cüzdandan Kart Sildiğimiz Kısım


def deleteCardFromWallet(request):
    message = ""
    if request.POST:
        req = BankCardDeleteRequest()
        req.userId = request.POST.get('userId')
        req.cardId = request.POST.get('cardId')
        req.clientIp = "127.0.0.1"

        # Cüzdanda bulunan karti silmek için yapılan API cagrisini temsil etmektedir
        response = req.execute(req, config)
        message = json.dumps(json.loads(response),
                             indent=4, ensure_ascii=False)

    return render(None, 'deleteCardFromWallet.html', {'message': message})


# Cüzdandaki Kartla Tek Tıkla Ödeme Yaptığımız Örnek


def nonThreeDPaymentWithWallet(request):
    message = ""
    if request.POST:
        req = NonThreeDPaymentRequest()
        req.OrderId = str(randint(1, 10000))
        req.Echo = "Echo"
        req.Mode = config.Mode
        req.Amount = "10000"
        req.CardOwnerName = ""
        req.CardNumber = ""
        req.CardExpireMonth = ""
        req.CardExpireYear = ""
        req.Installment = request.POST.get('installment')
        req.Cvc = ""
        req.ThreeD = "false"
        req.UserId = request.POST.get('userId')
        req.CardId = request.POST.get('cardId')

        # Sipariş veren bilgileri
        req.Purchaser = req.PurchaserClass()
        req.Purchaser.name = "Ahmet"
        req.Purchaser.surname = "Veli"
        req.Purchaser.birthDate = "1986-07-11"
        req.Purchaser.email = "ahmet@veli.com"
        req.Purchaser.gsmPhone = "5889541011"
        req.Purchaser.tcCertificate = "1234567890"
        req.Purchaser.clientIp = "127.0.0.1"

        # Fatura bilgileri
        req.Purchaser.invoiceAddress = req.PurchaserAddress()
        req.Purchaser.invoiceAddress.name = "Ahmet"
        req.Purchaser.invoiceAddress.surname = "Veli"
        req.Purchaser.invoiceAddress.address = "Mevlut Pehlivan Mah. PosFix Plaza Sisli"
        req.Purchaser.invoiceAddress.zipCode = "34782"
        req.Purchaser.invoiceAddress.cityCode = "34"
        req.Purchaser.invoiceAddress.tcCertificate = "1234567890"
        req.Purchaser.invoiceAddress.country = "TR"
        req.Purchaser.invoiceAddress.phoneNumber = "2122222222"

        # Kargo adresi bilgileri
        req.Purchaser.shippingAddress = req.PurchaserAddress()
        req.Purchaser.shippingAddress.name = "Ahmet"
        req.Purchaser.shippingAddress.surname = "Veli"
        req.Purchaser.shippingAddress.address = "Mevlut Pehlivan Mah. PosFix Plaza Sisli"
        req.Purchaser.shippingAddress.zipCode = "34782"
        req.Purchaser.shippingAddress.cityCode = "34"
        req.Purchaser.shippingAddress.tcCertificate = "1234567890"
        req.Purchaser.shippingAddress.country = "TR"
        req.Purchaser.shippingAddress.phoneNumber = "2122222222"

        # Ürün Bilgileri
        req.Products = []
        product1 = req.Product()
        product1.title = "Telefon"
        product1.code = "TLF0001"
        product1.price = "5000"
        product1.quantity = "1"
        req.Products.append(product1)

        product2 = req.Product()
        product2.title = "Bilgisayar"
        product2.code = "BLG0001"
        product2.price = "5000"
        product2.quantity = "1"
        req.Products.append(product2)

        # Cüzdandaki kart ile ödeme yapma API çağrısının yapıldığı kısımdır.
        message = Helper.formatXML(req.execute(req, config))

    return render(None, 'nonThreeDPaymentWithWallet.html', {'message': message})


# Ödeme Linki Oluşturduğumuz Kısım


def paymentLinkCreateRequest(request):
    message = ""
    if request.POST:
        req = PaymentLinkCreateRequest()
        req.clientIp = "127.0.0.1"
        req.name = request.POST.get('name')
        req.surname = request.POST.get('surname')
        req.tcCertificate = request.POST.get('tcCertificate')
        req.taxNumber = request.POST.get('taxNumber')
        req.email = request.POST.get('email')
        req.gsm = request.POST.get('gsm')
        req.amount = request.POST.get('amount')
        req.threeD = request.POST.get('threeD')
        req.expireDate = request.POST.get(
            'expireDateYear') + "-" + request.POST.get(
            'expireDateMonth') + "-" + request.POST.get('expireDateDay') + " 00:00:00"
        req.sendEmail = request.POST.get('sendEmail')
        req.mode = config.Mode
        req.commissionType = request.POST.get('commissionType')

        # ödeme sorgulama servisi api çağrısının yapıldığı kısımdır.
        response = req.execute(req, config)
        message = json.dumps(json.loads(response),
                             indent=4, ensure_ascii=False)

    return render(None, 'paymentLinkCreate.html', {'message': message})


# Ödeme Linki Sorguladığımız Kısım


def paymentLinkInquiryRequest(request):
    message = ""
    if request.POST:
        req = PaymentLinkInquiryRequest()
        req.clientIp = "127.0.0.1"
        req.email = request.POST.get('email')
        req.gsm = request.POST.get('gsm')
        req.linkState = request.POST.get('linkState')
        req.startDate = ''
        req.endDate = ''
        if request.POST.get('linkId'):
            req.linkId = request.POST.get('linkId')
        if (request.POST.get('startYear') and request.POST.get('startMonth') and request.POST.get('startDay')):
            req.startDate = request.POST.get(
                'startYear') + "-" + request.POST.get(
                'startMonth') + "-" + request.POST.get('startDay') + " 00:00:00"
        if (request.POST.get('endYear') and request.POST.get('endMonth') and request.POST.get('endDay')):
            req.endDate = request.POST.get(
                'endYear') + "-" + request.POST.get(
                'endMonth') + "-" + request.POST.get('endDay') + " 00:00:00"
        req.pageSize = request.POST.get('pageSize')
        req.pageIndex = request.POST.get('pageIndex')

        # ödeme sorgulama servisi api çağrısının yapıldığı kısımdır.
        response = req.execute(req, config)
        message = json.dumps(json.loads(response),
                             indent=4, ensure_ascii=False)

    return render(None, 'paymentLinkInquiry.html', {'message': message})


# Ödeme Linki Sildiğimiz Kısım


def paymentLinkDeleteRequest(request):
    message = ""
    if request.POST:
        req = PaymentLinkDeleteRequest()
        req.linkId = request.POST.get('linkId')
        req.clientIp = "127.0.0.1"

        # ödeme sorgulama servisi api çağrısının yapıldığı kısımdır.
        response = req.execute(req, config)
        message = json.dumps(json.loads(response),
                             indent=4, ensure_ascii=False)

    return render(None, 'paymentLinkDelete.html', {'message': message})


# İade Sorgulaması Yaptığımız Kısım


def paymentRefundInquiryRequest(request):
    message = ""
    if request.POST:
        req = PaymentRefundInquiryRequest()
        req.clientIp = "127.0.0.1"
        req.orderId = request.POST.get('orderId')
        req.amount = request.POST.get('amount')

        # ödeme sorgulama servisi api çağrısının yapıldığı kısımdır.
        response = req.execute(req, config)
        message = json.dumps(json.loads(response),
                             indent=4, ensure_ascii=False)

    return render(None, 'paymentRefundInquiry.html', {'message': message})


# İade Yaptığımız Kısım


def paymentRefundRequest(request):
    message = ""
    if request.POST:
        req = PaymentRefundRequest()
        req.clientIp = "127.0.0.1"
        req.orderId = request.POST.get('orderId')
        req.refundHash = request.POST.get('refundHash')
        req.amount = request.POST.get('amount')

        # ödeme sorgulama servisi api çağrısının yapıldığı kısımdır.
        response = req.execute(req, config)
        message = json.dumps(json.loads(response),
                             indent=4, ensure_ascii=False)

    return render(None, 'paymentRefund.html', {'message': message})


def checkoutFormCreateRequest(request):
    message = ""
    if request.method == "POST":
        checkoutFormCreateRequest = CheckoutFormCreateRequest()
        checkoutFormCreateRequest.OrderId = str(randint(1, 10000))
        checkoutFormCreateRequest.Amount = "10000"
        checkoutFormCreateRequest.ThreeD = "false"
        checkoutFormCreateRequest.Mode = config.Mode
        checkoutFormCreateRequest.Purchaser = checkoutFormCreateRequest.PurchaserClass()
        checkoutFormCreateRequest.Purchaser.name = "Ahmet"
        checkoutFormCreateRequest.Purchaser.surname = "Veli"
        checkoutFormCreateRequest.Purchaser.email = "mura@Veli.com"
        checkoutFormCreateRequest.Version = "1.0"
        checkoutFormCreateRequest.Echo = "Echo"

        # API Cagrisi Yapiyoruz
        response = checkoutFormCreateRequest.execute(checkoutFormCreateRequest, config)
        message = json.dumps(json.loads(response), indent=4, ensure_ascii=False)

    return render(None, 'checkoutFormCreate.html', {'message': message})
