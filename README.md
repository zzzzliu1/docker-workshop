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


### 下面为Docker Volume（数据挂载）做准备
三个阶段：
1. 在宿主机创建测试文件
2. 用Python 脚本读取这些文件
3. 准备把宿主机目录挂载到Docker 容器

第一阶段：创建测试目录
你执行：
```bash
mkdir test
```

创建目录：
```text
/workspaces/docker-workshop/
└── test/
```

然后：
cd test
进入：
``` text
/workspaces/docker-workshop/test
```

第二阶段：创建文件
执行：
``` bash
touch file1.txt file2.txt file3.txt
```
`touch` 作用：
创建空文件

结果：
```text
test/
├── file1.txt
├── file2.txt
└── file3.txt
```

给file1写入内容：
执行：
``` bash
echo "Hello from host" > file1.txt
```
相当于： 把字符串写入文件
结果：
file1.text
内容变成： Hello from host
验证：
```bash
cat file1.txt
```
输出：
``` text
Hello from host
```


### Docker Volume 需要
``` text
宿主机目录
↓
挂载
↓
容器目录
```

例如：
```bash
-v /workspaces/docker-workshop/test:/app
```
意思：
``` text
宿主机:
/workspaces/docker-workshop/test

映射到

容器:
/app
```

### Docker Volume 的核心思想
前面你学到：
容器A 创建 file
退出

容器B 启动
file 消失
因为：
容器之间文件系统不共享

#### Volume解决的就是这个问题：
```text
宿主机目录
       │
       ▼
Volume挂载
       │
       ▼
容器
```
这样： Mac上的文件和Docker里的文件 实际上是同一份数据。

<img width="606" height="316" alt="image" src="https://github.com/user-attachments/assets/10f95efc-edc3-4f72-941d-e9a18d089cf0" />


```bash
mkdir test  # 创建测试目录，创建一个名为test的目录

cd test         # 进入目录

touch file1.txt file2.txt file3.txt       # 创建三个空文件

echo "Hello from host" > file1.txt       # 向file1.txt 写入内容

ls           # 查看目录内容

cat file1.txt     # 查看内容

cat file2.txt

python script.py

# 创建 script.py
from pathlib import Path

current_dir = Path.cwd()
current_file = Path(__file__).name

print(f"Files in {current_dir}:")

for filepath in current_dir.iterdir():
    if filepath.name == current_file:
        continue

    print(f"  - {filepath.name}")

    if filepath.is_file():
        content = filepath.read_text(encoding='utf-8')
        print(f"    Content: {content}")


python script.py      #再次运行python

cd ..             # 返回项目根目录

ls              #查看

pwd         # 查看当前路径

echo $(pwd)/test

docker run -it --entrypoint=bash -v $(pwd)/test:/app python:3.13.11-slim     # 尝试运行Docker

cd /app       # 查看挂载目录

ls

python script.py      # 运行脚本
```



# Building Pipeline
- Download CSV data from the web
- Transform and clean the data with pandas
- Load it into PostgreSQL for querying
- Process data in chunks to handle large files



```bash
import sys   # 导入python内置模块sys

print('hello pipeline')  # 向终端输出一段文本
```

在终端运行脚本：
```bash
ls      # 查看当前目录

cd pipeline/            # 进入pipeline目录

python ./pipeline.py          #运行python脚本

```


后面大概率会把这个文件放到容器里运行
例如：
``` bash
docker run \
-it \
-v $(pwd):/app \
python:3.13.11-slim \
python /app/pipeline/pipeline.py
```
此时流程会变成：
``` text
宿主机
│
├── pipeline.py
│
▼
挂载到容器
│
▼
容器中的 Python
│
▼
运行 pipeline.py
│
▼
输出 hello pipeline
```

这实际上就是数据工程里最常见的模式：
``` text
pipeline.py
      ↓
Docker Container
      ↓
Airflow 调度
      ↓
ETL Pipeline
```
<img width="650" height="329" alt="image" src="https://github.com/user-attachments/assets/3b7f3579-121d-41c2-b261-5593629c2e1a" />


* python+Docker+虚拟环境之间的隔离关系

<img width="989" height="512" alt="image" src="https://github.com/user-attachments/assets/451d5520-44c3-42ed-b6ec-e9cd09b13676" />

1. 左侧：本地环境（Linux Ubuntu 24.08）

左边虚线框表示你的本机环境：

Linux Ubuntu 24.08
上面运行着 Python
Python 里面还有一个 virtual environment（虚拟环境）
虚拟环境里有：
python ← pyarrow（说明安装了 pyarrow 这个库）
一个 test/ 文件夹

👉 这里的重点是：

Python 虚拟环境 ≠ 操作系统隔离
它只是 Python 依赖隔离，不是安全隔离。


2. 右侧：Docker 容器环境

右边大框是一个 Docker 容器：

Docker Image：python:3.13.11-slim
基于 Debian 系统
里面写了一个非常危险的命令：

rm -rf /

👉 这个命令的意思是：

删除根目录 / 下所有文件
在真实 Linux 机器上 = 系统直接被清空（非常危险）


3. 箭头关系：关键点（非常重要）

图里有两个箭头：

（1）Docker → Debian → rm -rf /

说明：

Docker 容器里可以执行 Linux 命令
容器内部是一个“完整的迷你系统”

（2）左下角 test/ → Docker

说明：

本地的 test/ 文件夹被“映射”或“访问”到了 Docker 中
这通常意味着：

👉 volume 挂载 / 文件共享


```text
-v ./test:/app/test
```

4. 这张图真正想表达的核心

核心结论：
（1） python 虚拟环境不能隔离系统风险
（2） Docker才是真正的系统级隔离




#  uv “隔离python版本+自动创建虚拟环境”

```bash

Initialized project `docker-workshop`   # 用uv 初始化一个项目，并指定python 3.13 作为项目的目标运行版本

> which python

/home/codespace/.python/current/bin/python       # 当前系统默认环境中的python位置

> python -V

Python 3.12.1      # 当前系统默认是python=3.12版本

> uv run python -V       # uv自己帮你下载/选择了python 3.13.14

Using CPython 3.13.14

Creating virtual environment at: .venv

Python 3.13.14

> uv run which python      #uv自动创建虚拟环境

/workspaces/docker-workshop/.venv/bin/python

> which python           

/home/codespace/.python/current/bin/python 并且结合之前我们图片中的内容再进行解释

```

<img width="1050" height="505" alt="image" src="https://github.com/user-attachments/assets/1b928e46-ece7-41ed-84d4-3daa77b05ecd" />



# 用uv的python 3.13 成功运行了`pipeline.py`,生成了`output_12.parquet`,然后把当前项目代码提交并推送到了Github
```bash
cd /workspaces/docker-workshop
uv run python pipeline/pipeline.py 12
```

代码成功创建了一个DataFrame 并生成了这个文件：
``` text
pipeline/output_12.parquet
```

** 把项目文件加入Git
```bash
git add .
git commit -m "Add uv python pipeline example"
```

这一步把资源管理器里的这些文件提交到了本地Git：
```text
.python-version
.vscode/settings.json
main.py
pipeline/pipeline.py
pipeline/output_12.parquet
pyproject.toml
test/file1.txt
test/file2.txt
test/file3.txt
test/script.py
uv.lock
.gitignore
```

其中比较核心的是：
```
pyproject.toml        uv 项目配置
uv.lock              uv 锁定依赖版本
.python-version      指定 Python 版本
pipeline/pipeline.py 你的 pipeline 脚本
test/                测试文件夹
```


## 一个正确的终端执行：用uv的python 3.13 成功运行了`pipeline.py`,生成了`output_12.parquet`,然后把当前项目代码提交并推送到了Github步骤

```bash

# 1. 进入项目Git 仓库
cd/ workspaces/docker-workshop

# 2. 确认uv使用python 3.13
uv run python -V

# 3. 运行pipeline，并传入参数12
uv run python pipeline/pipeline.py 12

# 4. 查看是否生成parquet文件
ls pipeline

# 5. 建议忽略parquet输出文件
echo "*.parquet" >> .gitignore

# 6. 如果parquet已经被Git跟踪，移除Git跟踪，但保留本地文件
git rm --cached pipeline/output_12.parquet

# 7. 查看 Git 状态
git status

# 8. 添加所有需要提交的文件
git add .

# 9. 提交到本地 Git
git commit -m "Add UV Python pipeline example"

# 10. 先同步 GitHub 最新代码
git pull --rebase origin main

# 11. 推送到 GitHub
git push origin main

```


整体流程是：
``` text
进入项目目录
↓
用 uv + Python 3.13 运行 pipeline.py
↓
传入参数 12
↓
生成 output_12.parquet
↓
忽略 parquet 结果文件
↓
git add
↓
git commit
↓
git pull --rebase
↓
git push
```



# 把它放进自己的Docker中，自己创建的Docker Image中
- 把`pipeline.py` 打包进Docker 镜像`test:pandas`, 然后进入Docker容器内部运行这个python pipeline，传入参数`12`, 最后在容器内部生成`output_12.parquet`

1. 查看项目结构

```bash
ls
```

你在项目根目录看到了：
``` text
README.md  main.py  pipeline  pyproject.toml  test  uv.lock
```

然后进入pipeline文件夹：
```bash
cd ./pipeline/
ls
```
看到：
```
Dockerfile  output_12.parquet  pipeline.py
```
说明Dockerfile现在放在：/workspaces/docker-workshop/pipeline/Dockerfile 中


2. 将参数12传进docker中

```bash
docker run --rm test:pandas 12
```

3. 构建Docker 镜像

```
docker build -t test:pandas .
```
意思是：
用当前pipeline文件夹里的Dockerfile构建一个镜像
镜像名叫test
标签叫pandas

这次成功构建了：
```bash
naming to docker.io/library/test:pandas
```
说明：镜像test：pandas 已经生成

4. Dockerfile文件里面内容

```text
FROM python:3.13.11-slim

RUN pip install pandas pyarrow

WORKDIR /code

COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]
```

这是正确的，因为Dockerfile和 `pipeline.py` 在同一个pipeline文件夹里。

5. 运行容器

```bash
docker run --rm test:pandas 12
```


6. 进入Docker 内部
你第一次写错了：
```bash
docker run -it --entrypoint=bash --rm test:pandas
```

成功进入容器内部，看到：
```text
root@7af5848b0577:/code#
```
这说明你已经在Docker容器里了。


7. 在容器内部查看文件
容器里执行：
```
ls
```
输出：
```
pipeline.py
```

说明Dockerfile里的这句成功了：
```bash
COPY pipeline.py .
```
也就是说，本地的`pipeline.py` 被复制到了容器的：
```
/code/pipeline.py
```

8. 在容器内部运行pipeline

第一次：
```bash
python pipeline.py
```

没有传参数，所以报错：
``` bash
IndexError: list index out of range
```
因为代码需要：
```
sys.argv[1]
```

第二次：
```
python pipeline.py 12
```

成功了：
```
arguments ['pipeline.py', '12']
```

说明参数12成功传入。
然后代码生成DataFrame：
``` text
day  num_passengers  month
0    1               3     12
1    2               4     12
```
最后生成：
output_12.parquet


9. 验证容器内部生成文件

执行：
```
ls
```

看到：
```
output_12.parquet  pipeline.py
```
说明： 你的pipeline在Docker 容器内部成功生成了parquet 文件。

10.退出容器
```
exit
```


最终完成的流程：
```text
本地 pipeline.py
↓
写 Dockerfile
↓
docker build -t test:pandas .
↓
生成 Docker 镜像 test:pandas
↓
docker run 运行容器
↓
进入容器 /code
↓
运行 python pipeline.py 12
↓
生成 output_12.parquet
↓
退出容器
```



# 用dockerfile 构建一个带uv的python 镜像，并通过 `docker run test:pandas 12 `成功运行pipeline。

## Docker+uv+Python Pipeline总结
本次练习的目标是： 把一个Python pipeline项目打包进Docker 镜像中，并使用uv管理依赖，最后通过Docker容器运行 `pipeline.py 12`

### Dockerfile 内容

```dockerfile
FROM python:3.13.11-slim          # 使用 Python 3.13.11 的轻量版镜像作为基础环境。

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/            # 从 uv 官方镜像中复制 uv 工具到当前镜像中。

WORKDIR /code                  # 设置容器内部工作目录为 /code。

COPY pyproject.toml .python-version uv.lock ./               # 复制 uv 项目的核心配置文件到容器中。

RUN uv sync --locked                   # 根据 uv.lock 安装固定版本的依赖，保证环境可复现。

COPY pipeline.py .                         # 把本地的 pipeline.py 复制到容器的 /code 目录。

ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
```

设置容器启动时默认执行：
```bash
uv run python pipeline.py
```
因此运行：
``` bash
docker run -it --rm test:pandas 12
```

就等价于在容器内部执行：
``` bash
uv run python pipeline.py 12
```

正确终端流程：
``` bash

# 进入pipeline目录
cd /workspaces/docker-workshop/pipeline

#使用Dockerfile构建镜像
docker build --no-cache -t test:pandas .

#检查镜像配置
docker inspect test:pandas

# 运行容器，并传入参数12
docker run -it --rm test:pandas 12

```

### 最终成功输出：
```bash
arguments ['pipeline.py', '12']

hello pipeline,month

   day  num_passengers  month
0    1               3     12
1    2               4     12

hello pipeline,month= 12
```

### 本次练习完成了什么？
``` text
本地 Python 项目
        ↓
Dockerfile 定义 Python 3.13.11 环境
        ↓
复制 uv 工具
        ↓
复制 pyproject.toml、uv.lock、.python-version
        ↓
uv sync --locked 安装依赖
        ↓
复制 pipeline.py
        ↓
构建 Docker Image: test:pandas
        ↓
docker run test:pandas 12
        ↓
容器内部执行 uv run python pipeline.py 12
        ↓
成功运行 pipeline
```

这次练习重点是：
1. Dockerfile用来定义可复现的运行环境
2. uv用来管理 Python依赖和虚拟环境
3. `uv.lock` 保证依赖版本固定
4. `ENTRYPOINT` 定义容器启动时默认执行的命令
5. `docker run test:pandas 12` 中的`12` 会作为参数传给`pipeline.py`
6. 最终实现了一个可容器化运行的python data pipeline





















