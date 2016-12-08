import pymysql
import platform
from Config import config
import os

if "Windows" in platform.platform():
    backup_tool = config.btool_win
    restore_tool = config.rtool_win
    user = config.user_win
    psw = config.psw_win
    db_name = config.dbname_win
elif "Darwin" in platform.platform():
    backup_tool = config.btool
    restore_tool = config.rtool
    user = config.user
    psw = config.psw
    db_name = config.dbname


def backup_db(target):
    """
    :param target:  target for backup the database
    :return: null
    """
    command = '%s -h%s -u%s -p%s %s > %s' % (backup_tool, config.host, user, psw, db_name, target)
    try:
        os.system(command)
    except Exception as e:
        print(e)


def restore_db(source):
    """
    :param source:  the source for restore the sql data from specified location to the destination database.
    :return: null
    """
    command = '%s -h%s -u%s -p%s -P3306 %s < %s' % (restore_tool, config.host, user, psw, db_name, source)
    try:
        os.system(command)
    except Exception as e:
        print(e)


def exec_sql(sql):
    """
    :param sql: sql language for query / update / add /delete for the test.
    :return:  data for query , null for update/delete and id or other key for add.
    """
    try:
        conn = pymysql.connect(host=config.host, user=user, passwd=psw, db=db_name, charset='utf8')
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        r = cur.fetchall()
        cur.close()
        conn.close()
        return r
    except Exception as e:
        print('Mysql Error %d: %s' % (e.args[0], e.args[1]))


# if __name__ == "__main__":
    # fd = os.path.join(os.path.dirname(__file__), "backup.sql")
    # restore_db(fd)
    # print exec_sql("select id from certification where user_id=1 and category = 5")
    # restore_db("backup.sql")
