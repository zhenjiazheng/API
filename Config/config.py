# __author__ = 'zhengandy'

import os
from Common.util import md5_s
method = "DEBUG"

db = os.environ.get('DATABASE', "waiwang")

project = os.environ.get("CASE_FOLDER", "Projects/ZZKGUser")
if "JiHe" in project:
    host = "120.24.169.76"
    user = "dev"
    psw = "ZP0wEuGG8Mxk"
    dbname = "waiwang"
else:
    host = "172.16.0.71"
    user = "root"
    psw = "root"
    dbname = "o2"

redis_host = "localhost"
redis_port = 6379
redis_db = 0


rmquser = ""
rmqpass = ""
rmqhost = "localhost"
rmqport = 5672
# 172.16.4.203/ zzkgurl
# test_zzkg_user = "http://testauto.thy360.com/"
# "zzkg_merchant_url": "http://127.16.0.207/"
# "zzkg_merchant_release_url": "http://release-console.thy360.com/",
preData = {
    "zzkg_merchant_release_url": "http://testauto.thy360.com/",
    "jh_url": "https://dev-m.jihe365.cn/",
    "zzkg_admin_url": "http://172.16.6.213/",
    "zzkg_url": "http://testauto.thy360.com/",
    "zzkg_merchant_url": "http://release-console.thy360.com/",
    "xsd_user_url": "http://172.16.0.70/",
    "xsd_user_release": "http://xsd-release.thy360.com/",

    "sqwm_url": "http://172.16.0.207/",
    "sqwm_user1": "15507554489",

    "BDCRMUser": "joedu",
    "BDCRMPassword": "root@01",
    "ZZKGAdminUser1": "leoli",
    "ZZKGAdminUser1Pass": "123456",
    "zzkg_test_user": "15814982521",
    "User1": "17711111022",
    "User2": "17711111010",
    "User3": "13664321001",
    "User4": "15215123525",
    "User": "13500044444",
    "MUser1": "13798765888",
    "MUser2": "13898765999",
    "JRUser": "13692159330",
    "123456": md5_s("123456"),
    # Belowe is the secret key for each sub system for Public API.
    "SK_ErShouHuo": "nvikc1ic74soaqucn6h1gzjydikkum6s",
    "SK_HuiYuanBao": "ngkb4us617j534ttplzj3gp059vf6v7j",
    "SK_UserServerAPI": "39htfdynqu43mnjd8gxuhc6evin2p2eo",
    "SK_ShangJiaBan": "rpm8vnejyxo9tdbdazt03zeew9mimkdh",
    "SK_PeiSongBan": "t76esrmgmltdx89o800oe6z12cdu5enx",
    "SK_BDBan": "0kr3iife9fnsqy7ztafroimzczq3h6xc",
    "SK_ShenQiWaiMai": "6fbc8b59cac04d1b997ec5ccc4e552cc",
    # Below is the APPID for each sub system:
    "APPID_ErShouHuo": "appidzzerhuo0vyokl",
    "APPID_HuiYuanBao": "appidhuiyuanbaovdt964",
    "APPID_UserServerAPI": "appidserverapie4ki8k",
    "APPID_ShangJiaBan": "appidbossut5hn5",
    "APPID_PeiSongBan": "appidps1wey3d",
    "APPID_BDBan": "appidbdr102h0",
    "APPID_ShenQiWaiMai": "appidsqwmf41s",
    "Admin": "13511111111",
    "Admin2": "13522222222",
    "Admin3": "13533333333"}
if "JiHe" in project:
    filename = "uploadedFile"
else:
    filename = "fileName"

# Below is the host, username, password and database for SQL connection.
# JiHe Finance
port = "3306"

btool = '/usr/local/mysql/bin/mysqldump'
rtool = '/usr/local/mysql/bin/mysql'


user_win = "root"
psw_win = "111111"
dbname_win = "ppw"
port_win = "3306"
btool_win = 'E:/mysql-5.6.17-winx64/bin/mysqldump'
rtool_win = 'E:/mysql-5.6.17-winx64/bin/mysql'


email_sender = "andy.zheng@hey900.com"
email_sender_password = "####"
smtp_sever = "smtp.exmail.qq.com"
email_receiver = ["andy.zheng@hey900.com", "clark.li@hey900.com"]
