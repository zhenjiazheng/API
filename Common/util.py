# coding=UTF-8
import hashlib
import sys
import simplejson
from imp import reload
reload(sys)
sys.setdefaultencoding("utf8")  # @UndefinedVariable


def get_values_by_key(input_json, key, values=list):
    key_value = None
    value = None
    if isinstance(input_json, dict):
        for json_result in input_json.values():
            if key in input_json.keys():
                key_value = input_json.get(key)
                if key_value not in values:
                    values.append(key_value)
            else:
                get_values_by_key(json_result, key, values)
    elif isinstance(input_json, list):
        for json_array in input_json:
            get_values_by_key(json_array, key, values)
    if values:
        if len(values) > 1:
            value = values
        elif len(values) == 1:
            value = values[0]
        return value
    else:
        return "Cannot find the value"


# def get_value_by_key(in_dict, param):
#     """
#     :param in_dict: 输入的数据，一般为接口请求返回值。
#     :param param: 需要获取对应value的key值。
#     :return: 返回value，一般为单个数值，也可以数值。
#     """
#     value = ""
#     values = []
#     if isinstance(in_dict, int):
#         value = in_dict
#     if isinstance(in_dict, list):
#         for element in in_dict:
#             if isinstance(element, dict):
#                 if param in element:
#                     value = element[param]
#                     if (value or value == 0 or value == 0.0) and value not in values:
#                         if isinstance(value, list):
#                             for each in value:
#                                 values.append(each)
#                         else:
#                             values.append(value)
#             else:
#                 pass
#     elif isinstance(in_dict, dict):
#         for each in in_dict.keys():
#             if param == each:
#                 value = in_dict[each]
#                 if (value or value == 0 or value == 0.0) and value not in values:
#                     if isinstance(value, list):
#                         for each2 in value:
#                             values.append(each2)
#                     else:
#                         values.append(value)
#             elif isinstance(in_dict[each], dict):
#                 for each2 in in_dict[each].keys():
#                     if param == each2:
#                         # print(in_dict[each][each2])
#                         value = in_dict[each][each2]
#                         if (value or value == 0 or value == 0.0) and value not in values:
#                             if isinstance(value, list):
#                                 for each3 in value:
#                                     values.append(each3)
#                             else:
#                                 values.append(value)
#                     elif isinstance(in_dict[each][each2], list):
#                         for element in in_dict[each][each2]:
#                             if isinstance(element, dict) and param in element.keys():
#                                 value = get_value_by_key(element, param)
#                                 if (value or value == 0 or value == 0.0) and value not in values:
#                                     if isinstance(value, list):
#                                         for each4 in value:
#                                             values.append(each4)
#                                     else:
#                                         values.append(value)
#                     elif isinstance(in_dict[each][each2], dict):
#                         for each3 in in_dict[each][each2].keys():
#                             if param == each3:
#                                 value = in_dict[each][each2][each3]
#                                 if (value or value == 0 or value == 0.0) and value not in values:
#                                     if isinstance(value, list):
#                                         for each4 in value:
#                                             values.append(each4)
#                                     else:
#                                         values.append(value)
#             elif isinstance(in_dict[each], list):
#                 for element in in_dict[each]:
#                     if isinstance(element, int) or isinstance(element, str):
#                         pass
#                     elif isinstance(element, list):
#                         if param in element:
#                             value = get_value_by_key(element, param)
#                             if (value or value == 0 or value == 0.0) and value not in values:
#                                 if isinstance(value, list):
#                                     for each2 in value:
#                                         values.append(each2)
#                                 else:
#                                     values.append(value)
#                     elif isinstance(element, dict):
#                         for key in element.keys():
#
#                             if param == key:
#                                 value = element[param]
#                                 if (value or value == 0 or value == 0.0) and value not in values:
#                                     if isinstance(value, list):
#                                         for each2 in value:
#                                             values.append(each2)
#                                     else:
#                                         values.append(value)
#                             if isinstance(element[key], dict):
#                                 for key2 in element[key].keys():
#                                     if param == key2:
#                                         value = element[key][key2]
#                                         if (value or value == 0 or value == 0.0) and value not in values:
#                                             if isinstance(value, list):
#                                                 for each3 in value:
#                                                     values.append(each3)
#                                             else:
#                                                 values.append(value)
#             else:
#                 pass
#
#     fun = lambda x, y: x if y in x else x + [y]
#     values = reduce(fun, [[], ] + values)
#     if len(values) > 1:
#         return values
#     else:
#         return value


def sort_data(di, ignore="Secret Key"):
    """
    此方法为了接口文档中的Headers secret使用
    :param di: 输入参数的params
    :param ignore: 对应的secret key
    :return:
    """
    for k in di.keys():
        if ignore in di.keys():
            di.pop(ignore)
    for k in di.keys():
        if di[k] is None:
            di.pop(k)
    return "".join(["{0}={1}&".format(k, di[k]) for k in sorted(di.keys())])[:-1].encode("utf-8")


def md5_secret(in_str, serect_key):
    """
    MD5加密
    :param in_str:
    :param serect_key:
    :return:
    """
    md_str = in_str+"&secret="+serect_key
    # print md_str
    md = hashlib.md5()
    md.update(md_str)
    md_ret = md.hexdigest().upper()
    return md_ret


def md5_s(in_str):
    """
    MD5加密
    :param in_str:
    :return:
    """
    md_str = in_str
    # print md_str
    md = hashlib.md5()
    md.update(md_str)
    md_ret = md.hexdigest()
    return md_ret


def get_current_stamp():
    import datetime
    import time
    return str(int(time.mktime(datetime.datetime.now().timetuple())))


class OptionalException(Exception):
    pass


def get_value(property_path, data):
    temp = data
    for k in property_path.split("."):
        if k.endswith("?"):
            k = k[:-1]
            is_optional = True
        else:
            is_optional = False

        try:
            idx = int(k)
            try:
                temp = temp[idx]
            except IndexError as e:
                if is_optional:
                    # return None
                    raise OptionalException()
                else:
                    raise e

        except ValueError as e:
            try:
                temp = temp[k]
            except KeyError as e:
                if is_optional:
                    # return None
                    raise OptionalException()
                else:
                    raise e
    return temp


def decode_str(content, encoding='utf-8'):
    # 只支持json格式
    # indent 表示缩进空格数
    return simplejson.dumps(content, encoding=encoding, ensure_ascii=False, indent=4)


# if __name__ == "__main__":
#     data = {"code": "1234", "phone": "17712345669", "Secret Key": "39htfdynqu43mnjd8gxuhc6evin2p2eo"}
#     secret_key = data["Secret Key"]
#     in_str = sort_data(data)
#     print (md5_secret(in_str, secret_key).upper())
#     # data = {"code": 0, "data": {"code": "1234","test":{"code": "92992"},"yd":[{"code":"678"}]}, "msg": "返回值"}
#     print get_value_by_key(data, "headImg")
