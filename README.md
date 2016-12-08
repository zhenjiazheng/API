工程项目运行方法：

cd到对应的存放路径

在根部目录下运行命令行：

python main.py -F arg1 -N arg2 -S arg3 -P args4 -DB args5 -CL args6

例子：
python main.py -F "Projects/JiHe" -N 1 -S 1 -P "Projects／JiHePre" -DB "waiwang" -CL "1,2,4,7,9"

如果想运行几何金融项目的1，2，4，7，9：
python main.py -F "Projects/JiHe" -DB "waiwang" -CL "1,2,4,7,9"

支持多文件夹用例执行：
python main.py -F "Projects/JiHe/UserInterface; Projects/JiHe/account; Projects/JiHe/public"
此命令执行的用例为UserInterface; account; public三个文件夹的所有用例，适合用于一个项目中有多个模块用例
特别注意：-F 后面所带的多个文件夹必须用"; "隔开；

-F M-必选
-N 可选，默认0（全部用例）
-S 可选 默认0 （延时表示）
-P 可选 默认 None（预设置公共步骤）如无不需要带
-DB 可选 默认"waiwang"--几何金融的数据库 （ 由于每个项目使用的数据库不一样，这部分单独参数化 ，如在测试步骤中不需要对数据库操作无需
                                        理会）
-CL 可选 默认"" --此参数与-N互斥，优先-N。

做API接口测试的相关人员对于写json的用例熟悉。
范例:
{
	"input":{
			"method": "POST",
			"url":"http://release.thy360.com/",
			"rest": "py/dealer/backend/v5/seller/login/",
			"headers": null,
			"param":{
				"phoneNumber":"13924595452", "password": "123456"
			}
	},
  "output":{ "msg": {"EQ":"【成功】"}, "dealer_token": {"TYPE":"str"}, "business_type_id": {"EQ":4}
      },
  "key": ["dealer_token"] 或者 "key": {key: value}
}

SQL范例：
{
	"sql":[
		"delete from users where id = {{key.uid}}",
		"delete from users_verified where user_id = {{key.uid}}",
		"delete from users_extend where user_id = {{key.uid}}",
		"delete from account_invest where user_id = {{key.uid}}",
		"delete from account_invest_record where user_id = {{key.uid}}"
	]
}
如果有select出现需要保存数据时，范例：
{
	"sql":[
		"select id from users where mobile = {{pre.User1}}"
	],
	"key": ["id"]
}
 redis范例：
 {
	"redis":{
		"delete":"key1",
		"set":{ "key2": "value2","key3": "value3"},
		"flushall":null,
		"size": null,
		"get":["name","name1"]
	}，
	"key": ["name","name1"]
}
其中input是接口请求的部分,包括请求的地址(url+rest), headers在这里是会带上用户或商户登录后产生的token。
param为请求报文。

output这里是为了检查每个返回值的类型/具体值/或者其他定义的校验值。如不需要校验可以不带或为空对象
可以直接具体到每个值，例如：
{
	"input":{
			"method": "GET",
			"url":"{{pre.jh_url}}",
			"rest": "ja/v1/test/sms/regist?",
			"headers":{"client": "lj_android",
                        "Content-Type": "application/json"
				},
			"param":{
				"phone":"{{pre.User1}}", "code": "1234"
			}
	},
  "output":{"code": {"ALLIN":[0,"1234"]},"msg":{"TYPE":"str"}, "data":{"TYPE":"dict"}，"data.code":{"EQ":"1234"} },
  "key":{"code":"data.code"}   # 将data.code返回保存为key值为code
}

key为在当前步骤需要保存的某个返回key值对应的value, 如果保存之前已经有当前key值存在,当前的key,value对会被更新替换。如不需要保存key可以
不带此健或为空。
