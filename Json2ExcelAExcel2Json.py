# coding=UTF-8

from xlrd import open_workbook
import xlwt
from xlutils.copy import copy
import os
import sys
import codecs
import re
from ConvertCaseName import case_number
from imp import reload
reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable


def get_dirs(path_dir):
    for root, dirs, files in os.walk(path_dir):
        cases = dirs
        return cases


def get_steps(path_d):
    for root, dirs, files in os.walk(path_d):
        steps = files
        return steps


class Json2excel2json(object):
    def __init__(self):
        pass

    @staticmethod
    def json2excel(project, excel):
        milestone_folder = os.path.join(os.path.dirname(__file__), project)
        excel_file = os.path.join(os.path.dirname(__file__), excel)
        cases = get_dirs(milestone_folder)
        if os.path.exists(excel_file):
            os.remove(excel_file)
        filename = xlwt.Workbook()
        sheet = filename.add_sheet("sheet")
        filename.save(excel_file)
        rb = open_workbook(excel_file)
        wb = copy(rb)
        ws = wb.get_sheet(0)
        ws.write(0, 0, "ID".decode("utf-8"))
        ws.write(0, 1, "CaseName".decode("utf-8"))
        ws.write(0, 2, "CaseStep".decode("utf-8"))
        for i, each in enumerate(cases, 1):
            ws.write(i, 0, i)
            ws.write(i, 1, each.decode("utf-8"))
            pathcase = os.path.join(milestone_folder, each)
            case_content_list = []
            for item in get_steps(pathcase):
                item_path = os.path.join(pathcase, item)
                fd = codecs.open(item_path, "r", "utf-8")
                txt = fd.readlines()
                case_content_list.append("".join(txt))
            print("".join(case_content_list))
            ws.write(i, 2, "\n\n".join(case_content_list).decode("utf-8"))
        wb.save(excel_file)

    @staticmethod
    def excel2json(excel, project):
        project_folder = os.path.join(os.path.dirname(__file__), project)
        # print(project_folder)
        if os.path.exists(project_folder):
            import shutil
            shutil.rmtree(project_folder)
        os.mkdir(project_folder)
        excel_file = os.path.join(os.path.dirname(__file__), excel)
        # print(excel_file)
        wb = open_workbook(excel_file)
        worksheet = wb.sheet_by_index(0)
        # print(worksheet.nrows)
        # print(worksheet.get_rows())
        num_rows = worksheet.nrows
        for curr_row in range(1, num_rows):
            row = worksheet.row_values(curr_row)
            # print('row%s is %s' % (curr_row, row))
            case_folder = os.path.join(project_folder, row[1])
            if not os.path.exists(case_folder):
                os.mkdir(case_folder)
            keys_split = re.split('[\d]+. ', row[2])
            steps_split = re.split('Step[\d]+: ', row[3])
            expects_split = re.split('[\d]+. ', row[4])
            steps = steps_split[1:]
            expects = expects_split[1:]
            keys = keys_split[1:]
            # print(steps)
            for i, each in enumerate(steps):
                if "None" in keys[i]:
                    if "sql" in each or "redis" in each:
                        strin = "{ %s }" % each
                    else:
                        strin = "{ \"input\": %s," % each + "\n" + "\"output\": %s }" % expects[i]
                else:
                    if "sql" in each or "redis" in each:
                        strin = "{ %s, \"key\":%s , \"output\":%s}" % (each, keys[i], expects[i])
                    else:
                        strin = "{ \"input\": %s ," % each + "\n" + "\"output\": %s," % expects[i] + "\n" \
                            + "\"key\": %s }" % keys[i]
                if i + 1 > 99:
                    fd = open("%s/%d.json" % (case_folder, i + 1), "a")
                if 9 < i + 1 <= 99:
                    fd = open("%s/0%d.json" % (case_folder, i + 1), "a")
                if i + 1 <= 9:
                    fd = open("%s/00%d.json" % (case_folder, i + 1), "a")
                fd.write(strin)
                fd.close()
        case_number(project, 1)


if __name__ == "__main__":
    transfer = Json2excel2json()
    transfer.json2excel("Projects/ZZKGMerchant", "Excel/MS3.xls")
#     transfer.excel2json("Excel/MS2.xls", "Projects/Test")
