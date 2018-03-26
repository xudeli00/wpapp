from flask import Flask, request
from config import token
import hashlib
import receive, reply

app = Flask(__name__)

# shandler = logging.StreamHandler
# shandler.setLevel(logging.DEBUG)
# app.logger.addHandler(shandler)
# logging.config.fileConfig('logging.conf')

@app.route("/",methods = ['GET', 'POST'])
def index():

    if request.method == 'GET':
        try:
            signature = request.args.get("signature")
            timestamp = request.args.get("timestamp")
            nonce = request.args.get("nonce")
            echostr = request.args.get("echostr")
            if signature is None or timestamp is None or nonce is None or echostr is None:
                app.logger.info("Not get expect parameter, bad request!")
                return "Hello flask!"

            app.logger.debug(str(signature) + "|" + str(echostr))
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                return echostr
            else:
                app.logger.warning("Signature not match!")
                return ""
        except Exception , e:
            app.logger.exception("Exception occurred!")
            return "Error occurred:", e.message

    if request.method == 'POST':
        try:
            data = request.data
            app.logger.debug("Get post data:" + str(data))
            recMsg = receive.parse_xml(data)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    content = "test"
                    #口算题
                    if recMsg.Content == "\xe5\x8f\xa3\xe7\xae\x97\xe9\xa2\x98":
                        import math20
                        rslt = math20.main()
                        for _m in rslt:
                            content += "%s %s %s =\n" % _m
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
            else:
                print "Process later."
                return "success"
        except Exception, Argment:
            return Argment


if __name__ == '__main__':
    import logging
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    app.logger.addHandler(console)
    app.run(host='0.0.0.0', port=8000)
