"""posfix_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from main.views import *

urlpatterns = [
                  re_path(r'^$', threedPaymentRequest, name='threedPaymentRequest'),
                  re_path(r'^nonThreeDPayment/', nonThreeDPaymentRequest, name='nonThreeDPayment'),
                  re_path(r'^paymentInquiry/', paymentInquiryRequest, name='paymentInquiry'),
                  re_path(r'^paymentInquiryWithTime/', paymentInquiryWithTimeRequest,
                      name='paymentInquiryWithTime'),
                  re_path(r'^paymentLinkDelete/', paymentLinkDeleteRequest, name='paymentLinkDelete'),
                  re_path(r'^paymentLinkCreate/', paymentLinkCreateRequest, name='paymentLinkCreate'),
                  re_path(r'^paymentLinkInquiry/', paymentLinkInquiryRequest,
                      name='paymentLinkInquiry'),
                  re_path(r'^paymentRefundInquiry/', paymentRefundInquiryRequest,
                      name='paymentRefundInquiry'),
                  re_path(r'^paymentRefund/', paymentRefundRequest, name='paymentRefund'),
                  re_path(r'^getCardFromWallet/', getCardFromWallet, name='getCardFromWallet'),
                  re_path(r'^addCartToWallet/', addCartToWallet, name='addCartToWallet'),
                  re_path(r'^deleteCardFromWallet/', deleteCardFromWallet,
                      name='deleteCardFromWallet'),
                  re_path(r'^binRequest/', binRequest, name='binRequest'),
                  re_path(r'^binV4Request/', binV4Request, name='binV4Request'),
                  re_path(r'^nonThreeDPaymentWithWallet/', nonThreeDPaymentWithWallet,
                      name='nonThreeDPaymentWithWallet'),
                  re_path(r'^admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
