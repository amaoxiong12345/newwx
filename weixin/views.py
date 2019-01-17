import hashlib
import random

import httputils as HttpUtils
import time
from django.http.response import HttpResponse
from rest_framework.response import Response
from urllib import parse
from .WXBizMsgCrypt import WXBizMsgCrypt
from django.shortcuts import render
import xml.etree.cElementTree as ET

# Create your views here.
from rest_framework.views import APIView

class response_msg:
    def __init__(self, toUser, fromUser, recvMsg):
        self._toUser = toUser
        self._fromUser = fromUser
        self._recvMsg = recvMsg
        self._nowTime = int(time.time())

    def structReply(self):
        content = self._recvMsg
        text = """
                <xml>
                <ToUserName><![CDATA[{0}]]></ToUserName>
                <FromUserName><![CDATA[{1}]]></FromUserName>
                <CreateTime>{2}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{3}]]></Content>
                </xml>
                """.format(self._fromUser, self._toUser, self._nowTime, content)  # 前面两个参数的顺序需要特别注意

        return text

class WeiXinMsg(APIView):
    def get(self,request):
        sToken = "TwlFTETxx97OJVwRRdxElWy2u5D"
        sEncodingAESKey = "EsA7TqrESZAoShEmMeLjMY3fvxBpbmx0sUVpBVWaPkb"
        sCorpID = "wxa1ee89c194f047fb"
        sMsgSig = request.query_params.get("msg_signature")
        sTimeStamp = request.query_params.get("timestamp")
        sNonce = request.query_params.get("nonce")
        sEchoStr = request.query_params.get("echostr")
        # sEchoStr = "123321"
        # sMsgSig = sVerifyMsgSig.encode('utf8')
        # sTimeStamp = sVerifyTimeStamp.encode('utf8')
        # sNonce = sVerifyNonce.encode('utf8')
        # sEchoStr = sVerifyEchoStr.encode('utf8')
        # print(type(sToken))
        # sortlist = [sToken, sTimeStamp, sNonce, sEchoStr]
        # sortlist.sort()
        # sha = hashlib.sha1()
        # sha.update("".join(sortlist))
        # print(sha.hexdigest())
        wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
        # ret = wxcpt.VerifyAESKey()
        ret, sEStr = wxcpt.VerifyURL(sMsgSig, sTimeStamp, sNonce,sEchoStr)
        return HttpResponse(sEStr)
    def post(self,request):
        sToken = "TwlFTETxx97OJVwRRdxElWy2u5D"
        sEncodingAESKey = "EsA7TqrESZAoShEmMeLjMY3fvxBpbmx0sUVpBVWaPkb"
        sCorpID = "wxa1ee89c194f047fb"
        wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
        sMsgSig = request.query_params.get("msg_signature")
        sTimeStamp = request.query_params.get("timestamp")
        sNonce = request.query_params.get("nonce")
        r_xml = request.raw_data
        print(r_xml)
        ret, sMsg = wxcpt.DecryptMsg(r_xml, sMsgSig, sTimeStamp, sNonce)
        if ret != 0:
            print('错误')
        else:
            xml_tree = ET.fromstring(sMsg)
            req_content = xml_tree.find("Content").text
            ToUsername = xml_tree.find("ToUsername").text #企业微信ip
            FromUerName = xml_tree.find("FromUserName").text  #成员userid
            AgentID = xml_tree.find("AgentID").text

            print(req_content)
            res_msg = "hello world"
            rTimeStamp = time.time()
            print(rTimeStamp)
            # rNonce = random.choices(range(0,10),k=6,weights=range(0,10))
            sReqNonce = "1597212914"
            sReqTimeStamp = "1476422779"
            sRespData = """<xml>
            <ToUserName><![CDATA[{0}]]></oUserName>
            <FromUserName><![CDATA[{1}]]></FromUserName>
            <CreateTime>{2}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{3}]]></Content>
            <MsgId>{4}</MsgId>
            <AgentID>{5}</AgentID>
            </xml>""".format(FromUerName,"shi",rTimeStamp,res_msg,1,AgentID)
            ret,sEncryptMsg = wxcpt.EncryptMsg(sRespData,sReqNonce,sReqTimeStamp)
            if (ret != 0):
                print("ERR: EncryptMsg ret: " + str(ret))
                # ret == 0 加密成功，企业需要将sEncryptMsg返回给企业号
            return HttpResponse(sEncryptMsg)