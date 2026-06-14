# docker-workshop
Workshop Codespaces


<img width="2548" height="1482" alt="image" src="https://github.com/user-attachments/assets/4d3388f6-0b3f-4b69-91f8-5118d9bfa15d" />


## 从Docker 镜像（Image）创建并运行容器（Container）的完整过程。
第一部分： 运行hello-world


```bash 
docker run hello-world
```
这条命令相当于：
docker run <image_name>
其中：
image_name= hello-world

Docker 的逻辑是：
1. 本地找镜像
2. 找不到则去Docker Hub 下载
3. 根据镜像创建容器
4. 启动容器
5. 显示容器输出

第二部分： 运行Ubuntu
``` bash
docker run ubuntu
```

下载Ubuntu 镜像
输出：Unable to find image 'ubuntu:latest' locally
说明： 本地没有ubuntu镜像

Docker 去 Docker Hub下载：
<img width="674" height="455" alt="image" src="https://github.com/user-attachments/assets/ddb1b459-6fd4-4376-8aa3-6dcf36a560ba" />



第三部分： 进入Ubuntu容器
执行：
```bash
docker run -it ubuntu
```
<img width="652" height="458" alt="image" src="https://github.com/user-attachments/assets/98a92f79-fd0d-4e64-8cf3-3ad1abeb4834" />
<img width="654" height="227" alt="image" src="https://github.com/user-attachments/assets/f63d02ff-0da0-43f1-a060-e5d2f93562c1" />


## Docker 的核心概念：
1. 镜像（Image）
2. 容器（Container）
3. 默认启动命令（ENTRYPOINT/CMD）
4. 容器文件系统
5. 容器生命周期
6. 为什么容器里的文件会“消失”

我按照执行顺序给你解释。

第一部分： 启动python容器
执行：
```bash
docker run -it python:3.13.11-slim
```
Docker 做了什么？
Step1: 发现本地没有镜像
```text
Unable to find image 'python:3.13.11-slim'locally
```
意思： 本地没有这个python镜像

Step2: 从Docker Hub下载镜像
```
Pulling from library/python

下载多个layer：
镜像结构类似：
``` text
Debian Linux
    ↓
Python 3.13
    ↓
配置文件
```
每层都是一个Layer。

Step3: 启动容器
下载完成：
``` text
Status: Downloaded newer image for python:3.13.11-slim
```

Docker 根据镜像创建容器。
可以理解为：
``` text
镜像(Image)
      ↓
实例化
      ↓
容器(Container)
```

类似：
```
Class
 ↓
Object

```

Step4: 自动启动Python
<img width="629" height="474" alt="image" src="https://github.com/user-attachments/assets/c26fd0d6-0603-447f-bc9f-4b78c120f5c6" />



第二部分： 查看环境变量
``` bash
>>> import os
>>> os.getenv('bla')
```

意思：读取环境变量bla



```bash
> docker run -it --entrypoint=bash python:3.13.11-slim
root@c028bba45bd3:/# ls
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
root@c028bba45bd3:/# python -V
Python 3.13.11
root@c028bba45bd3:/# echo 123 > file
root@c028bba45bd3:/# ls
bin   dev  file  lib    media  opt   root  sbin  sys  usr
boot  etc  home  lib64  mnt    proc  run   srv   tmp  var
root@c028bba45bd3:/# cat file
123
root@c028bba45bd3:/# exit
exit
> docker run -it --entrypoint=bash python:3.13.11-slim
root@7cc2e6c36d16:/# ls
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
root@7cc2e6c36d16:/# cat file
cat: file: No such file or directory
root@7cc2e6c36d16:/#
```

### 为什么file不见了？
原因：
file 创建在第一个容器里，而第二次run创建的是：全新的容器。 可以理解成： 
第一次：
python镜像 -> 容器A。你在里面创建file

第二次：
python镜像 -> 容器B，这是新的实例。 容器B不知道容器A里面发生过什么。
类似：
windows 安装镜像 -> 虚拟机A -> 创建file.txt
然后：
windows 安装镜像 -> 虚拟机B
B里面不会有A的文件


### Docker 核心概念
Image（镜像）： 类似模版：python镜像 （只读）
Container（容器）：
镜像运行后的实例：
``` text
Python镜像
     ↓
容器1

Python镜像
     ↓
容器2
```
每个容器独立。


### 如果想找回第一个容器呢？
执行：
``` bash
docker ps -a
```
可以看到：
```
CONTAINER ID
c028bba45bd3
7cc2e6c36d16
```

第一个容器还存在，只是停止了。
可以重新启动：
```text
docker start -i c028bba45bd3
```

或者：
```text
docker start -ai c028bba45bd3
```
回到原来的容器。

此时：
``` bash
cat file
```

仍然能看到：123
因为那个文件一直在容器A里。

这正是Docker最核心的设计思路之一：镜像是模版，`docker run`每次都会基于模版创建一个新的容器实例；容器之间默认互不共享文件系统。





