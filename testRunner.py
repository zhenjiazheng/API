# -*- coding: utf-8 -*-
"""
Author: Zheng.zhenjia
"""

from unittest import TestSuite

from HTMLTestRunner import HTMLTestRunner as Tr
from testReport import TestReport
from Config import config
# from Common.sendEmail import send_email
import platform


def test_suite():
    # moduleNames=build_test_suite()
    if "Windows" in platform.platform():
        module_names = ["API"]
    else:
        module_names = ["API"]
    t_suite = TestSuite()

    for module_name in module_names:
        # print module_name
        import importlib
        m = importlib.import_module(module_name)
        # modules=map(__import__,moduleNames)
        t_suite.addTest(m.suite())
        # suite.addTest(element(module.suite()))
    return t_suite


def main():
    global report_file, runner, fp, report_title
    report_file = TestReport.generate_report("Report")
    runner = Tr()
    fp = open(report_file, 'wb')
    # print test_suite.__name__
    report_title = "Report" + "_" + test_suite.__name__
    runner = Tr(stream=fp, verbosity=2, title=report_title, description=report_file)
    runner.run(test_suite())
    fp.close()
    # send_email(report_file, config.email_receiver)

if __name__ == '__main__':
    main()
