# coding=UTF-8
import re
# from util import decode_str


def type_validator(params, value):
    mark = 0
    if isinstance(params, list):
        if value == "list":
            return True
        for each in params:
            if type(each).__name__ == "unicode":
                if type(each.encode("utf-8")).__name__ in value:
                    mark += 1
            else:
                if type(each).__name__ in value:
                    mark += 1
        if len(params) == mark:
            return True
    elif type(params).__name__ == value:
            return True
    return False


def type_in_validator(params, value):
    mark = 0
    if isinstance(params, list):
        for each in params:
            if type(each).__name__ == "unicode":
                if type(each.encode("utf-8")).__name__ in value:
                    mark += 1
            else:
                if type(each).__name__ in value:
                    mark += 1
        if mark == len(params):
            return True
    else:
        if type(params).__name__ in value:
            return True
    return False


def between_validator(params, value):
    mark = 0
    if isinstance(params, list):
        for each in params:
            if not isinstance(params, int):
                return False
            if value[0] <= each <= value[1]:
                mark += 1
        if mark == len(params):
            return True
    else:
        if not isinstance(params, int):
            return False
        if value[0] <= params <= value[1]:
            return True
    return False


def values_validator(params, value):
    mark = 0
    if isinstance(params, list):
        for i in range(len(params)):
            if params[i] in value:
                mark += 1
        if mark == len(params):
            return True
    else:
        if params in value:
            return True
    return False


def len_list_validator(params, value):
    if isinstance(params, list):
        if len(params) == value:
            return True
    return False


def len_validator(params, value):
    mark = 0
    if isinstance(params, list):
        for each in params:
            if len(each) == len(value):
                mark += 1
        if len(params) == mark:
            return True
    else:
        if len(params) == len(value):
            return True
    return False


def equal_validator(params, value):
    try:
        if "*" in value or "/" in value or "+" in value or "-"  in value:
            value = eval(value)
    except Exception as e:
        pass
    if params == value:
        return True
    else:
        return False


def not_equal_validator(params, value):
    if params != value:
        return True
    else:
        return False


def string_in_validator(params, value):
    if value in params:
        return True
    else:
        return False


def in_validator(param, value):
    if isinstance(param, list):
        if value in param:
            # print "Find the value in index : %d" % value.index(param)
            return True
        else:
            return False
    elif isinstance(param, str):
        if param == value:
            return True
        else:
            return False


def greater_validator(params, value):
    if params >= eval(value):
        return True
    else:
        return False


def less_validator(params, value):
    if params <= eval(value):
        return True
    else:
        return False


def not_found_validator(params, value):
    if isinstance(params, list):
        if value not in params:
            return True
    elif isinstance(params, str):
        if value not in params:
            return True
    elif params != value:
        return True
    else:
        return False


def reg_validator(params, value):
    # print decode_str(params)
    mark = 0
    if isinstance(params, list):
        for each in params:
            # if type(each).__name__ == "unicode":
            #     each = each.encode("utf-8")
            try:
                val = re.match(value, each)
                if val.group(0):
                    mark += 1
            except Exception as e:
                print(e)
                print("Cannot find the regular pattern @ return: {}".format(each))
                return False
        if mark == len(params):
            return True
    else:
        try:
            if type(value).__name__ == "unicode":
                value = value.encode("utf-8")
            val = re.match(value, params)
            if val.group(0):
                return True
        except Exception as e:
            print(e)
            print("Cannot find the regular pattern @ return: {}".format(params))
            return False
    return False


class ValidatorRegistry(object):
    registry = {}

    @classmethod
    def register(cls, name, validate):
        cls.registry[name] = validate

    @classmethod
    def validate(cls, name, params, value):
        return cls.registry[name].validate(params, value)


def checker(typo, params, value):
    val = ValidatorRegistry()
    if typo == "TYPE":
        val.register("TYPE", type_validator(params, value))
    if typo == "type":
        val.register("type", type_validator(params, value))
    if typo == "LEN":
        val.register("LEN", len_validator(params, value))
    if typo == "len":
        val.register("len", len_validator(params, value))
    if typo == "LE":
        val.register("LE", less_validator(params, value))
    if typo == "le":
        val.register("le", less_validator(params, value))
    if typo == "BETWEEN":
        val.register("BETWEEN", between_validator(params, value))
    if typo == "between":
        val.register("between", between_validator(params, value))
    if typo == "EQ":
        val.register("EQ", equal_validator(params, value))
    if typo == "eq":
        val.register("eq", equal_validator(params, value))
    if typo == "IN":
        val.register("IN", in_validator(params, value))
    if typo == "in":
        val.register("in", in_validator(params, value))
    if typo == "GE":
        val.register("GE", greater_validator(params, value))
    if typo == "ge":
        val.register("ge", greater_validator(params, value))
    if typo == "RE":
        val.register("RE", reg_validator(params, value))
    if typo == "re":
        val.register("re", reg_validator(params, value))
    if typo == "ALLIN":
        val.register("ALLIN", values_validator(params, value))
    if typo == "allin":
        val.register("allin", values_validator(params, value))
    if typo == "TYPEIN":
        val.register("TYPEIN", type_in_validator(params, value))
    if typo == "typein":
        val.register("typein", type_in_validator(params, value))
    if typo == "NF":
        val.register("NF", not_found_validator(params, value))
    if typo == "nf":
        val.register("nf", not_found_validator(params, value))
    if typo == "NEQ":
        val.register("NEQ", not_equal_validator(params, value))
    if typo == "neq":
        val.register("neq", not_equal_validator(params, value))
    if typo == "LL":
        val.register("LL", len_list_validator(params, value))
    if typo == "ll":
        val.register("ll", len_list_validator(params, value))
    if typo == "STRIN":
        val.register("STRIN", string_in_validator(params, value))
    if typo == "strin":
        val.register("strin", string_in_validator(params, value))
    return val.registry[typo]

# if __name__=="__main__":
#     id = ["http://image.thy360.com/images/deal/20151225/D119698.jpg",
#           "http://172.16.6.213/images/deal/temp/7ff6f470-70b7-11e6-b1ce-080027f6b007.jpg",
#           "http://image.thy360.com/images/deal/20160216/D101814.jpg"]
#     print(checker("RE", id, "http//[]*"))
