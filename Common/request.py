# -*- coding: utf-8 -*-
import requests
import requests_mock
from Config import config

way = config.method


def request_data(url, method, param=None, **kwargs):
    """

    :param url: 接口请求地址url
    :param method: 请求的方法（DEBUG或者MOCK，其中MOCK为自己构造的返回）
    :param param: 请求参数
    :param kwargs: 其他需要的kwargs
    :return: 请求返回数据
    """
    ret = None
    if way == "MOCK" or way == "mock":
        print("This is mock test.")

        @requests_mock.mock()
        def test_func(m):
            if method == "POST" or method == "post":
                m.post('http://test.com', text='this is test return data')
                return requests.post('http://test.com').text
            elif method == "GET" or method == "get":
                m.get('http://test.com', text='this is test return data')
                return requests.get('http://test.com').text
            elif method == "DELETE" or method == "delete":
                m.get('http://test.com', text='this is test return data')
                return requests.delete('http://test.com').text
            elif method == "PUT" or method == "put":
                m.get('http://test.com', text='this is test return data')
                return requests.put('http://test.com').text
            elif method == "PATCH" or "patch":
                m.get('http://test.com', text='this is test return data')
                return requests.patch('http://test.com').text
        return test_func()
    elif way == "DEBUG" or way == "debug":
        if method == "POST" or method == "post":
            ret = requests.post(url, param, **kwargs)
        elif method == "GET" or method == "get":
            ret = requests.get(url, param, **kwargs)
        elif method == "DELETE" or method == "delete":
            ret = requests.delete(url, **kwargs)
        elif method == "PUT" or method == "put":
            ret = requests.put(url, json=param, **kwargs)
        elif method == "PATCH" or method == "patch":
            ret = requests.patch(url, param, **kwargs)
        # cookies = ret.cookies
        # headers = ret.headers
        # print ret.content
        if ret.text:
            if "!DOCTYPE" in ret.text:
                return ret.content
            else:
                return ret.json()
        if ret.status_code == 500:
            return "Server Internal Error"
        if ret.status_code == 404:
            return "Cannot find the page, 404"
        else:
            return ret.text


def restful_api(req_url, req_method, params=None, files=None, headers=None, cookies=None):
    # ret = None
    if req_method == "POST" or req_method == "post":
        if files:
            ret = request_data(req_url, req_method, params, files=files, headers=headers, cookies=cookies,
                               allow_redirects=False)
        else:
            ret = request_data(req_url, req_method, json=params, files=files, headers=headers, cookies=cookies,
                               allow_redirects=False)
    else:
        ret = request_data(req_url, req_method, params, headers=headers, cookies=cookies, allow_redirects=False)
    return ret

#
# if __name__ == "__main__":
#     url = "http://release.thy360.com/py/dealer/backend/v5/seller/login/"
#     method = "POST"
#     param = {"phoneNumber":"13924595452", "password": "123456"}
#     ret = restful_api(url, method, param)
#     print ret
