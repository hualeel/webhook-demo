# -*- coding:utf-8 -*-
"""
Author:
名称：kubeovn demo
功能描述：
"""

from flask import Flask, request
from flask_cors import *
import socket
import os
import hmac

github_secret = 'abcdefg123456'


def encryption(data):
    key = github_secret.encode('utf-8')
    obj = hmac.new(key, msg=data, digestmod='sha1')
    return obj.hexdigest()


app = Flask(__name__,
            static_url_path='/python',  # 访问静态资源的url前缀，默认值是static
            static_folder='static',  # 静态文件目录，默认就是static
            template_folder='templates',  # 模板文件的目录，默认是templates
            )


@app.route('/webhook', methods=["POST"])
@cross_origin()
def playload():
    """
        github加密是将post提交的data和WebHooks的secret通过hmac的sha1加密，放到HTTP headers的
        X-Hub-Signature参数中
    """
    post_data = request.data
    # 生成 token
    token = encryption(post_data)

    # 认证签名是否有效
    signature = request.headers.get('X-Hub-Signature', '').split('=')[-1]
    if signature != token:
        return " webhook token认证无效", 401

    # 运行处理程序
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    print("Host name: %s" % host_name)
    print("IP address: %s" % ip_address)
    return "Host name: %s" % host_name + "<br>" + "IP address: %s" % ip_address


if __name__ == '__main__':
    # 通过url_map可以查看整个flask中的路由信息
    print(app.url_map)

    # 启动flask程序
    # service_port = os.getenv("SERVICE_PORT")
    service_port = 6001
    app.run(host="0.0.0.0", port=service_port)
