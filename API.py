# coding=UTF-8
# __author__ = 'andy.zheng'

import re
import simplejson
from jinja2 import Template
import os
import unittest
import time
from Common.request import restful_api
# from pprint import pprint
from SQL.sql import exec_sql
# from SQL.sql import backup_db, restore_db
from Common.util import md5_secret, sort_data, get_value, decode_str, get_values_by_key
from Common.validator import checker
from Config import config
from RedisOperation.red import RedisOperation
import sys
from imp import reload
reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable


class Context(object):
    """
    Define the Context to store the return value.
    """
    def __init__(self):
        self.key_value = {}


def template_json(context, filename):
    """
    param context: 上下文关联,保存需要用到的返回key-value对.
    param filename:  接口用例步骤文件,json文件.
    return:  返回读取的的数据.
    """
    value = open(filename).read()
    try:
        t = Template(value)
        value = t.render(key=context.key_value, pre=config.preData)
    except Exception as e:
        print(e)
        return False
    value = simplejson.loads(value)
    return value


def check_data(context, filename):
    """
    最后执行的关键步骤，请求输入，输出检查。
    :param context: 上下文关联存储器
    :param filename: 用例文件绝对路径
    :return:  布尔（True或者False）
    """
    val = template_json(context, filename)
    if "author" in val.keys():
        print("测试用例编写责任人：{}".format(val["author"]))
    # print(val)
    # 获取接口请求输入数据
    if "input" in val.keys():
        method = None
        headers = None
        param = None
        files = None
        url = val["input"]["url"]
        if "rest" in val["input"].keys():
            rest = val["input"]["rest"]
            url_full = url + rest
        else:
            url_full = url
        print("接口请求地址: \n{}".format(url_full))
        if "method" in val["input"].keys():
            method = val["input"]["method"]
            print("\nThe request method is :{}".format(method))
        if "param" in val["input"].keys():
            param = val["input"]["param"]
            print("\nThe request parameter is:\n{}\n".format(param))
            # if "Secret Key" in param:
            #     secret = param["Secret Key"]
            #     sort_value = sort_data(param)
            #     secret_value = md5_secret(sort_value, secret)
            #     context.key_value.update({"sign": secret_value})
            #     print(context.key_value)
        if "files" in val["input"].keys():
            files = {'{}'.format(config.filename): open(val["input"]["files"], 'rb')}
            print("\n发送的文件为:\n{}".format(val["input"]["files"]))
        if "headers" in val["input"].keys():
            headers = val["input"]["headers"]
            # if "param" in val.keys() and "Secret Key" in param:
            #     headers.update({"Authorization": context.key_value["sign"]})
            print("\n接口请求头文件为:\n{}\n".format(headers))
        start_time = time.time()
        data = restful_api(url_full, method, params=param, files=files, headers=headers)
        """
        下面为检测是否需要Mock数据辅助测试。此操作为了避免接口未开发完成是可以进行调试。
        """
        if config.method == "MOCK":
            if "mock" in val.keys():
                data = val["mock"]
        end_time = time.time()
        print("*" * 100)
        print("\n接口请求响应时延为:\n {}\n".format(end_time-start_time))
        print("\n接口请求返回值:")
        print(decode_str(data))
        print("*" * 100)

        """
        获取是否该步骤是否需要保存的对应Key值。如该key对应返回有多个，则在上下文中保存为key+i(递归下去，从index为1开始））
        """
        if "key" in val.keys():
            if isinstance(val["key"], list):
                """
                当获取需要保存的Key为数组，此类输入适合那些返回值中只有唯一一个key时获取value。
                """
                for i in range(len(val["key"])):
                    ma = re.findall("[a-z]*[\d]", val["key"][i])
                    if ma:
                        value = get_values_by_key(data, val["key"][i][0:-1], values=[])
                    else:
                        value = get_values_by_key(data, val["key"][i], values=[])
                    if isinstance(value, list):
                        for k, each in enumerate(value, 1):
                            context.key_value.update({val["key"][i] + "%d" % k: each})
                    else:
                        context.key_value.update({val["key"][i]: value})
            elif isinstance(val["key"], dict):
                """
                当获取需要保存的Key为字典，此类输入适合那些返回值中有多个个key时，根据输入路径获取value。
                """
                for each in val["key"].keys():
                    value = get_value(val["key"][each], data)
                    context.key_value.update({each: value})
        print("\nThe Global Context key and value is :")
        print(context.key_value)

        """
        # 检查是否有输出校验，如果有进行追个对比。
        """
        if "output" in val.keys():
            count = 0
            print("\n期望检测的返回值:")
            print(decode_str(val["output"]))
            for each in val["output"].keys():
                if not isinstance(val["output"][each], dict):
                    if checker(each, data, val["output"][each]):
                        count += 1
                    else:
                        print("检查返回 : %s 失败。\n" % each)
                        return False
                else:
                    try:
                        if not isinstance(data, dict) and not isinstance(data, list):
                            if not isinstance(data, int):
                                data = data.encode("utf-8")
                            if checker(each, data, val["output"][each]):
                                count += 1
                            else:
                                print("检查返回 : %s 失败。\n" % data)
                                return False
                        else:
                            for typo in val["output"][each].keys():
                                if len(each.split(".")) > 1:
                                    value = get_value(each, data)
                                else:
                                    value = get_values_by_key(data, each, values=[])
                                if type(value).__name__ == "unicode":
                                    value = str(value)
                                else:
                                    pass
                                # print(value)
                                if not checker(typo, value, val["output"][each][typo]):
                                    print("检查key: %s返回值失败。\n" % each)
                                    return False
                            count += 1
                        print("检查key: {}的返回值通过".format(each))
                    except Exception as e:
                        print(e)
                        return False

            if count == len(val["output"].keys()):
                print("\n所有检查Key值返回通过.")
                return True
        return True

    """
    SQL 输入检查并对SQL语句处理。
    """
    if "sql" in val.keys():
        result = None
        try:
            print(val["sql"])
            if isinstance(val["sql"], list):
                for each in val["sql"]:
                    result = exec_sql(each)
                    # print result
            else:
                result = exec_sql(val["sql"])
            for item in val["sql"]:
                if "SELECT" in item or "select" in item:
                    if "key" in val.keys() and isinstance(val["key"], list):
                        for i, item1 in enumerate(val["key"]):
                            context.key_value.update({item1: result[0][i]})
                    print(context.key_value)
                if "output" in val.keys():
                    number = 0
                    for i, each in enumerate(val["output"].keys()):
                        for item3 in val["output"][each].keys():
                            # print item,  context.key_value[each], val["output"][each][item]
                            if checker(item3, context.key_value[each], val["output"][each][item3]):
                                pass
                            else:
                                print("Key:{0}获取的值与期望不匹配{1}测试失败。".format(each, item3))
                                return False
                        number += 1
                    if number == len(val["output"]):
                        print("SQL :执行SQL成功，返回值检查成功。")
                        return True
            if isinstance(result, tuple):
                print("SQL :执行SQL成功，返回值检查成功。")
                return True
        except Exception as e:
            print(e)
            print("SQL :SQL返回值检查失败。")
            return False
    """
    REDIS 操作处理。
    """
    if "redis" in val.keys():
        f = RedisOperation(config.redis_host, config.redis_port, config.redis_db)
        if "set" in val["redis"]:
            for each in val["redis"]["set"].keys():
                f.redis_set(each, val["redis"]["set"][each])
        if "get" in val["redis"]:
            for each in val["redis"]["get"]:
                value = f.redis_get(each)
                if "key" in val.keys():
                    if each in val["key"]:
                        context.key_value.update({each: value})
        if "size" in val["redis"]:
            value = f.redis_size()
            context.key_value.update({"redis_size": value})
        if "delete" in val["redis"]:
            for each in val["redis"]["delete"]:
                f.redis_del(each)

        if "flushall" in val["redis"]:
            f.redis_flush_all()
        print(context.key_value)
        return True


def case_list(case_path):
    """
    此方法为了方便后面的test用例名获取显示
    :param case_path: 用例的绝对路径
    :return:  所有用例的列表
    """
    for root, dirs, files in os.walk(case_path):
        cases = dirs
        return cases


def get_test_steps(path_dir, case):
    """
    :param path_dir: 工程根目录路径。
    :param case:  用例名称，从case_list中获取。单纯的取其中一个。
    :return: 获取输入测试用例的所有测试步骤。
    """
    for root, dirs, files in os.walk(os.path.join(path_dir, case)):
        steps = []
        for each in files:
            each = os.path.join(os.path.join(path_dir, case), each)
            steps.append(each)
        return steps


def check_case(con, cases):
    """
    运行所有测试用例的使用方法。
    :param con: 使用到的上下文关联。
    :param cases: 所有测试用例列表。
    :return: 返回检查结果（boolean）
    """
    sleep_time = float(os.environ.get('SLEEP_TIME', 0))
    mark = 0
    for x, item in enumerate(cases, 1):
        print("测试步骤%d : " % x)
        print("-"*100)
        if check_data(con, item):
            mark += 1
        else:
            print("测试步骤%d失败。\n" % x + "-"*100)
            return False
        print("-"*100+"\n")
        time.sleep(sleep_time)
    if mark == len(cases):
        return True


class UnitTest(unittest.TestCase):

    def setUp(self):
        # backup_db("%s/backup.sql" % os.path.join(os.path.dirname(os.path.abspath(__file__)), "SQL"))
        # print("\n测试准备开始时间: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        unittest.TestCase.setUp(self)
        # lists = []
        self.context = Context()
        # pre_folder = os.environ.get('PRECONDITION_FOLDER', "None")
        # if pre_folder:
        #     test_dir = os.path.join(os.path.dirname(__file__), pre_folder)
        #     cases = case_list(test_dir)
        #     for i in range(len(cases)):
        #         steps = get_test_steps(test_dir, cases[i])
        #         lists.append(steps)
        #     print("\n开始执行预设置步骤: ")
        #     for steps in lists:
        #         check_case(self.context, steps)
        #     print("\n预设置步骤执行完成。")

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        # restore_db("%s/backup.sql" % os.path.join(os.path.dirname(os.path.abspath(__file__)), "SQL"))

    def run_case(self, steps):
        print("\n测试用例开始时间: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        # for each in allStepList:
        # context = Context()
        self.assertTrue(check_case(self.context, steps), "Test FAIL.")

    @staticmethod
    def get_test_func(steps):
        """
        :param steps: 测试步骤
        :return: 调用单元测试中的run_case执行测试。
        """
        def func(self):
            self.run_case(steps)
        return func


def __generate_test_cases():
    """
    本地执行产生对应的test suite。
    :return:  产生testsuite 把所有用例传递到UnitTest中的get_test_func进行测试。
    """
    lists = []
    caselist = []
    folder = os.environ.get('CASE_FOLDER', "Projects/ZZKGUser")
    folders = folder.split("; ")
    for each in folders:
        suite_dir = os.path.join(os.path.dirname(__file__), each)
        cases = case_list(suite_dir)
        # print(cases)
        for item in cases:
            caselist.append(item)
        for j in range(len(cases)):
            steps = get_test_steps(suite_dir, cases[j])
            lists.append(steps)
    item = int(os.environ.get('UT_ITEM', -1))
    items = os.environ.get("CASELIST", "").split(",")
    print('-' * 100)
    if item == -1 and items == [""]:
        for i in range(len(lists)):
            test_func = "test_" + caselist[i]
            setattr(UnitTest, test_func, UnitTest.get_test_func(lists[i]))
    elif item == -1 and items != [""]:
        for each in items:
            test_func = "test_" + caselist[int(each)-1]
            setattr(UnitTest, test_func, UnitTest.get_test_func(lists[int(each)-1]))
    elif item != -1 and items == [""]:
        test_func = "test_" + caselist[item]
        setattr(UnitTest, test_func, UnitTest.get_test_func(lists[item]))
    elif item != -1 and items != [""]:
        test_func = "test_" + caselist[item]
        setattr(UnitTest, test_func, UnitTest.get_test_func(lists[item]))

__generate_test_cases()


def suite():
    lists = []
    caselist = []
    folder = os.environ.get('CASE_FOLDER', "Projects/JiHe")
    folders = folder.split("; ")
    for i, each in enumerate(folders):
        suite_dir = os.path.join(os.path.dirname(__file__), each)
        cases = case_list(suite_dir)
        for item in cases:
            caselist.append(item)
        for j in range(len(cases)):
            steps = get_test_steps(suite_dir, cases[j])
            lists.append(steps)
    item = int(os.environ.get('UT_ITEM', -1))
    items = os.environ.get("CASELIST", "").split(",")
    print('-' * 100)
    if item == -1 and items == [""]:
        print('当前选择所有测试用例执行。'.encode("utf-8"))
        for i in range(len(lists)):
            test_func = "test_" + caselist[i]
            setattr(UnitTest, test_func, UnitTest.get_test_func(lists[i]))
    elif item == -1 and items != [""]:
        print('当前选择部分测试用例执行：'.encode("utf-8"))
        for each in items:
            test_func = "test_" + caselist[int(each)-1]
            setattr(UnitTest, test_func, UnitTest.get_test_func(lists[int(each)-1]))
    elif item != -1 and items == [""]:
        print('当前选择第%d个用例执行测试。'.encode("utf-8") % (item+1))
        test_func = "test_" + caselist[item]
        setattr(UnitTest, test_func, UnitTest.get_test_func(lists[item]))
    elif item != -1 and items != [""]:
        print('当前选择第%d个用例执行测试。'.encode("utf-8") % (item+1))
        test_func = "test_" + caselist[item]
        setattr(UnitTest, test_func, UnitTest.get_test_func(lists[item]))
    print('-' * 100)
    suit = unittest.TestSuite()
    suit.addTest(unittest.makeSuite(UnitTest))
    return suit
#
if __name__ == "__main__":
    # restore_db("%s/backup.sql" % os.path.join(os.path.dirname(os.path.abspath(__file__)),"sqldata"))
    unittest.main()
