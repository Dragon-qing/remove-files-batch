import os
import json
from smb.SMBConnection import SMBConnection
abspath = "\\"                              #文件目录
delfiletype=""                      #要删除的文件类型    
server_ip = ""                #共享目录主机IP地址
username = ""                             #本机用户名
password = ""                            #本机密码
my_name = ""                       #计算机属性中域名
remote_name = ""                 #远端共享文件夹计算机名
servername = ""                     #共享文件夹名
Dirlist = []
dellist = []
conn = None
smbflag = True              #是否启用smb连接

def get_del_files(server_ip, username, password, my_name, remote_name):
    if smbflag:
        sharelist = conn.listPath(servername,abspath)
        for i in sharelist:
            if i.filename[0] != '.':
                if i.isDirectory:
                    Dirlist.append(os.path.join(abspath,i.filename))
                elif str.endswith(i.filename, delfiletype):
                    dellist.append(os.path.join(abspath,i.filename))
    else:
        sharelist = os.listdir(abspath)
        for i in sharelist:
            temppath = os.path.join(abspath, i)
            if os.path.isdir(temppath):
                Dirlist.append(temppath)
            elif str.endswith(i,delfiletype):
                dellist.append(temppath)
    solveDir(servername)
    return dellist

def init():
    with open("setting.json", "r", encoding="utf-8") as f:
        setting = json.load(f)
    global abspath, delfiletype, server_ip, username, password,my_name,remote_name,servername,smbflag
    abspath = setting["abspath"]
    delfiletype = setting["delfiletype"]
    server_ip = setting["server_ip"]
    username = setting["username"]
    password = setting["password"]
    my_name = setting["my_name"]
    remote_name = setting["remote_name"]
    servername = setting["servername"]
    smbflag = setting["smb"]
    print(smbflag, type(smbflag))

def solveDir(servername):
    if len(Dirlist)==0:
        return
    else :
        tpath = Dirlist.pop()
        if smbflag:
            sharelist = conn.listPath(servername, tpath)
        else :
            sharelist = os.listdir(tpath)
        for i in sharelist:
            if smbflag:
                if i.filename[0] != '.':
                    if i.isDirectory:
                        Dirlist.append(os.path.join(tpath, i.filename))
                    elif str.endswith(i.filename, delfiletype):
                        dellist.append(os.path.join(tpath, i.filename))
            else:
                tempabspath = os.path.join(tpath, i)
                if os.path.isdir(tempabspath):
                    Dirlist.append(tempabspath)
                elif str.endswith(i, delfiletype):
                    dellist.append(tempabspath)                    
    solveDir(servername)
        
def delmethod():
    select = input("是否删除(y/n):")
    if str.lower(select) == "y":
        while len(dellist):
            path = dellist.pop()
            conn.deleteFiles(servername, path) if smbflag else os.remove(path)
        print("删除完毕！！")



def get_current_files_name():
    return os.listdir(abspath)


if __name__ == "__main__":
    init()
    if smbflag:
        conn = SMBConnection(username, password, "", "", use_ntlm_v2=True)    #is_direct_tcp=True,默认为当direct_tcp=True时，port需要445。当它是False时，端口应该是139
        assert conn.connect(server_ip, 445)
    filelist = get_del_files(server_ip, username, password, my_name, remote_name)
    for i in filelist:
        print(i)
    print(f"共{len(filelist)}个文件.")
    delmethod()
    if smbflag:
        conn.close()
    