![icon](./Readme.assets/icon.jpeg)

# 什么是 Open Handshake Version 0.0.1

Open Handshake 是一个用 Python 编写的、包含客户端与服务端的、简易的认证与绑定程序。服务端程序基于 Flask 框架开发，客户端可以调用服务端的接口以完成客户端与服务端的绑定，让服务器专门为特定的、处于局域网内的客户端服务。

![how_to_work](./Readme.assets/how_to_work.jpeg)

**此版本的 Open Handshake Version 0.0.1 可以完成以下的功能：**

- 同一局域网内，客户端可查询服务器；
- 同一局域网内，服务器校验客户端合法性；
- 同一局域网内，客户端查询并绑定服务器；
- 解绑程序
- 说明：当前版本一个局域网内只能有一台服务端 Level，若您想在一局域网内安装多台服务端 Level，请同时修改 Level 服务器端口和 Base 客户端请求端口。



# 名词解释

因为开发的时候看 后室 Backroom 有些上瘾，所以一部分参数命名就使用后室里面的命名了。

- Base: 基地，也就是所谓的客户端；
- Level: 层级，也就是所谓的服务端，服务器；
- Outpost: 前哨，也就是应用程序接口，API；
- Community: 社区，也就是最终处理任务的程序，应用程序；
- level_entrance_room: 可以切入层级的房间，也就是服务器的 IP 地址；
- level_entrance_door: 具体切入层级的大门，也就是服务器的端口 Port；



# Part 1 查询

这个方法由 “基地” 发起，下面是样例程序

```python
import  level_binding

level_binding.LevelBinding().Find_Level()
```

调用这段程序可以获得字符串形式的服务器地址。

例如：

```python
import  level_binding

# 程序部分
print(level_binding.LevelBinding().Find_Level())

# 控制台输出
192.168.31.85
```



# Part 2 校验与绑定

## 2.1 参数说明

### 2.1.1 服务器端 config.ini

```ini
# -*- coding: utf-8 -*-

[DEFAULT_GROUP]
# 层级名称
level_name = 11_The_Endless_City
# 层级切入地址，此地址表示 'Running on all addresses' 意味着 Level 可以存在于动态 IP 地址的网络环境中
level_entrance_room = 0.0.0.0
# 层级切入方法，端口号，要与基地 Base 的请求端口号一致
level_entrance_door = 33550
# 层级软件版本
level_version = 0.0.1

[REGISTER_GROUP]
# 0 表示层级并未被注册，1 表示层级被注册过
regist_state = 0
# 0 表示层级不可以注册，1 表示层级可以注册
could_regist = 1

[BASE_GROUP]
# 基地名称
base_name =
# 基地 SN 码
base_sn =
# 基地 token 令牌
base_token =
# 基地软件版本
base_version =
# 基地注册状态，1 表示基地已将层级注册，0 表示基地未将层级注册
base_regist_state =

[BASE_TEMP]
# 基地名称临时信息
base_name_temp =
# 基地 SN 码临时信息
base_sn_temp =
# 基地令牌临时信息
base_token_temp = 

```

### 2.1.2 客户端 config.ini

```ini
# -*- coding: utf-8 -*-
[DEFAULT_GROUP]
# 基地名称
base_name = MEG
# 基地 SN 码
base_sn = 
# 基地令牌
base_token = 
# 基地软件版本
base_version = 0.0.1
# 基地注册状态，2 表示请求 Level 将基地注册，1 表示基地已将 Level 注册
base_regist_state = 2

[LEVEL]
# 层级名称
level_name =
# 层级切入地址
level_entrance_room =
# 层级切入方法，端口号，要与层级配置文件一致
level_entrance_door = 33550
# 层级软件版本
level_version =
# 层级 MAC 地址
level_mac_addr =

[LEVEL_TEMP]
# 层级名称临时信息
level_name =
# 层级切入地点临时信息
level_entrance_room =
# 层级软件版本临时信息
level_version =
```

## 2.2 使用方法

程序分为客户端 Base 和服务端 Level，将 Level 程序部署至服务器上。

客户端使用下面的程序调用绑定方法

```python
import  level_binding

level_binding.LevelBinding().Binding_New_Level()
```

返回 True 或 False

返回 True 可以在 `config.ini` 中看到 Level 的信息

返回 False 可以在控制台看到具体的错误信息



# Part 3 解绑

客户端调用下面的程序以完成解绑

```python
import  level_binding

level_binding.LevelBinding().Untie_Level()
```

返回 True 可以发现在 `config.ini` 中除端口号之外的其他 Level 信息都会消失

返回 False 可以在控制台看到具体的错误信息



# Part 4 说明

客户端 Base 的名称由开发者自定，但只能是英文字符，目前不兼容其他语言。

客户端 Base 的 SN 码，SN 总长度为 32 位，其中前 6 位为大写字母、后 4 位是数字、中间 22 位为大小写字母与数字的组合。

客户端 Base 的 Token 令牌，总长度 32 位，为大小写字母和数字的组合。

测试码如下：

```
SN = XKVFQA2XQA2xKVFQA2XKVFQA21234567
Token = ot20pLAhCnISPNNdwWy1XYs1Owkb6env
```

目前由于一些原因限制，服务端暂时不能部署在 OS X 或 macOS 系统之上，可能会导致部分参数不正确。



无论客户端 Base 还是服务端 Level 的程序文件需放置与运行程序的最高层目录 `./`之下，客户端 Base 的调用需要导入 `level_binding.py` ，服务端则继续在 `main.py` 里添加路由。



客户端 Base 程序需要以下依赖 `requirements.txt`

```
certifi==2022.12.7
charset-normalizer==2.1.1
idna==3.4
psutil==5.9.4
requests==2.28.1
urllib3==1.26.13
```



服务端 Level 程序需要以下依赖 `requirements.txt`

```
click==8.1.3
Flask==2.2.2
importlib-metadata==5.2.0
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
psutil==5.9.4
Werkzeug==2.2.2
zipp==3.11.0
```



其它问题欢迎进群交流：913211989 ( 小猫不要摸鱼 )

进群令牌：FromGithub







