# remove-files-batch
批量删除本地或smb共享的文件
(使用python实现)
python >= 3.6

依赖包：
`pysmb`，`os`，`json`

# 使用方法
修改**setting.json**配置文件在运行.py文件

# setting.json文件
```
{
    "abspath" : "\\",       #文件主目录
	  "smb": false,           #是否为smb共享文件
    "delfiletype":".torrent",   #要删除的文件后缀
    "server_ip" : "",           #smb共享主机ip地址
    "username" : "",            #用户名                
    "password" : "" ,           #密码                
    "my_name" : "" ,            #本机名              
    "remote_name" : "" ,        #远程主机名        
    "servername" : ""           #共享的根文件夹名
}
```
>本地文件只需修改abspath和smb参数
