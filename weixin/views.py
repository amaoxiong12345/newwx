import hashlib

import httputils as HttpUtils
from rest_framework.response import Response
from urllib import parse
from .WXBizMsgCrypt import WXBizMsgCrypt
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


class WeiXinMsg(APIView):
    def post(self,request):
        data = request.data
        print(data)
        print(type(data))
    def get(self,request):
        print('调用')
        sToken = "XhzEDr67M1R"
        sEncodingAESKey = "WkzthlvZptEp3xgscJruNRBDBtLFGROqHqi99ARqReV"
        sCorpID = "wxa1ee89c194f047fb"
        sMsgSig = request.query_params.get("msg_signature")
        sTimeStamp = request.query_params.get("timestamp")
        sNonce = request.query_params.get("nonce")
        sEchoStr = request.query_params.get("echostr")
        # sMsgSig = sVerifyMsgSig.encode('utf8')
        # sTimeStamp = sVerifyTimeStamp.encode('utf8')
        # sNonce = sVerifyNonce.encode('utf8')
        # sEchoStr = sVerifyEchoStr.encode('utf8')
        print(sMsgSig)
        print(type(sMsgSig))
        print('***********')
        print(sTimeStamp)
        print(type(sTimeStamp))
        print('***********')
        print(sNonce)
        print(type(sNonce))
        print('************')
        print(sEchoStr)
        # print(type(sToken))
        # sortlist = [sToken, sTimeStamp, sNonce, sEchoStr]
        # sortlist.sort()
        # sha = hashlib.sha1()
        # sha.update("".join(sortlist))
        # print(sha.hexdigest())
        wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
        ret, sEchoStr = wxcpt.VerifyURL(sMsgSig, sTimeStamp, sNonce, sEchoStr)
        print('^^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^')
        print(ret)
        print(sEchoStr)
        print('git_test')
        return Response(sEchoStr)