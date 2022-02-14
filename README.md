<!--
 * @Author: LetMeFly
 * @Date: 2022-01-27 22:13:45
 * @LastEditors: LetMeFly
 * @LastEditTime: 2022-02-14 16:28:02
-->
# Calendar

微信小程序——默默无闻的日历罢了

## 配置说明

### 环境准备

完全使用该项目之前，请具备以下条件

1. 服务器
   >
   > 1. 拥有一台服务器
   >
   > 2. 拥有公网ip
   >
   > 3. 完成备案
   >
   > 4. 开启了https（微信小程序的限制）

2. MySQL
   >
   > 1. 配置好了MySQL环境
   >
   > 2. 为该项目创建了一个database
   >
   > 3. 为该项目创建了一个用户，且该用户只具有操作此库的权限（减小可能的SQL注入造成的损失）

3. python
   > 
   > 1. 配置好了python环境
   >
   > 2. 安装了django（pip install django）、requests

### 使用方法

1. 将项目克隆到本地```git clone git@github.com:LetMeFly666/Calendar.git```

2. 将```.\Front\```作为微信小程序的前端文件夹，将其上传至微信小程序开发平台，审核发布或设为体验

3. 在微信小程序管理平台设置好图标、名称等信息，配置服务器中添加自己的服务器

4. 在微信小程序管理平台选择“功能 -> 订阅消息”，在“公共模板库”中找到“日程提醒”并选用，选择三个“关键词”(“日程时间”、“提醒内容”、“备注”)，“提交”并在“我的模板”中Copy“模板ID”

5. 进入```.\Back\```，创建Secrets.py，在Secrets.py中，配置以下信息
   > SECRET_KEY = 'django-insecure-jafljalfsf*@46s' # 一串随机字符
   >
   > DATABASE_DBNAME = '数据库名称'
   >
   > DATABASE_USER = '数据库用户名'
   >
   > DATABASE_PASSWORD = '数据库密码'
   >
   > DATABASE_HOST = '数据库服务主机'
   >
   > DATABASE_PORT = '数据库端口'
   >
   > APP_ID = '微信小程序的AppID'
   >
   > APP_SECRET = '微信小程序的AppSecret'
   >
   > TEMPLATE_ID = '微信消息订阅模板id'

5. （启动mysql服务并)进行初始化```python manage.py makemigrations```、```python manage.py migrate```，之后运行即可(```python manage.py runserver```)

<font color="#f47920">喜欢了别忘了给个star哦</font>

## Docs

项目文档、笔记等

## Front

前端代码，即在微信小程序开发工具中的那一套

前端全局配置笔记：[https://letmefly.xyz/Notes/WXminiProgram/](https://letmefly.xyz/Notes/WXminiProgram/)

### 前端函数

<small><u>“前端函数”中的介绍以 .\Front\ 作为根目录</u></small>

#### formatTime

**位置：** utils/util.js

**功能：** 将javascript的Date转化为“yyyy-MM-dd hh:mm:ss”格式的字符串

**示例：**

```javascript
const dateNow = new Date();
console.log(formatTime(dateNow));

// 2022-02-13 17:18:54
```

#### LetMeFly_request

**位置：** utils/util.js

**功能：** （微信小程序不支持cookie），此函数为二次封装的wx.request，使请求自动带上Storage中的session

**示例：**

```javascript
LetMeFly_request({
    url: 'https://diary.letmefly.xyz/GetAllDiaries/',
    success: function(msg) {
        const { diaries } = msg.data;
        console.log(diaries);
    }
});

// ["第一个日记", "第二个日记", "66666"]
```

**注释：** 服务器接收到微信小程序中的sessionid后，就可以取出session中保存的信息

## Back

后端代码，即后端逻辑，采用python的django实现。

### 后端函数接口

#### login

**url：** /login/

**函数：** Apps.Functions.User.login

```
登录函数，实现微信小程序的登陆功能
函数根据登陆请求中的code向微信服务器索要用户openid和session_key
    openid - 每个用户独一无二，唯一不变，用来唯一标识每个用户
    session_key - 用来“数据签名校验”、“数据加密解密”等，会过期(但此次登陆结束之前不会过期)

Parameters:
    request - http request
        request.GET - {"code": (wx.login -> msg) msg.code}
    
Returns:
    JsonResponse - {"code": 0}
```

#### add1diary

**url：** /AddADiary/

**函数：** Apps.Functions.User.add1diary

```
添加一个日记

Parameters:
    request - http request
        request.session - 包含登录时保存到小程序Storage中的sessionid，由此来获取用户的userid
        json.loads(request.body) - {"content": 要添加的日记的内容}

Returns:
    JsonResponse - {"code": 0}
```

#### getAllDiaries

**url：** /AddADiary/

**函数：** Apps.Functions.User.getAllDiaries

```
获取所有日记

Parameters:
    request - http request
        request.session - 包含登录时保存到小程序Storage中的sessionid，由此来获取用户的userid

Returns:
    JsonResponse - {"code": 0, "diaries": diaries}
        diaries - [日记1, 日记2, 日记3, ...]
```

#### getAccessToken

**url：** 无

**函数：** Apps.Functions.Server.getAccessToken

```
获取小程序全局唯一后台接口调用凭据（access_token）

Returns:
    json - 调用结果
        正常调用 - {"access_token": "ACCESS_TOKEN", "expires_in": 7200} (过期时间当前为2h，后期可能会有所调整)
        系统繁忙 - {"errcode": 40001, "errmsg": ...}
```

#### sendAMessage

**url：** 无

**函数：** Apps.Functions.Server.sendAMessage

```
TODO:
```

### 后端数据库

#### 用户

```python
class user(models.Model):
    userid = models.CharField(verbose_name="openid", max_length=40, unique=True)
    session_key = models.CharField(verbose_name="session_key", max_length=40)
    remark = models.CharField(verbose_name="备注", max_length=50, null=True)
```

#### 日记

```python
class diaries(models.Model):
    userid = models.CharField(verbose_name="openid", max_length=40)
    content = models.CharField(verbose_name="日记内容", max_length=1024)
```

