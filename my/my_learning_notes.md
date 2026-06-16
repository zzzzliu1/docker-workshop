# ==========================================
# Docker Data Pipeline Demo
# ==========================================

# 进入项目目录
cd /workspaces/docker-workshop

# 查看项目结构
ls

# 进入 pipeline 目录（Dockerfile 所在位置）
cd pipeline

# 查看当前文件
ls

# 查看 Dockerfile 内容
cat Dockerfile

# Dockerfile
* FROM python:3.13.11-slim
* RUN pip install pandas pyarrow
* WORKDIR /code
* COPY pipeline.py .
* ENTRYPOINT ["python", "pipeline.py"]

# 构建 Docker Image
docker build -t test:pandas .

# 查看本地镜像
docker images

# 启动容器并进入 Bash
docker run -it --entrypoint bash --rm test:pandas

# ==========================================
# 以下命令在 Docker Container 内执行
# ==========================================

# 查看当前工作目录
pwd

# 查看容器中的文件
ls

# 查看 Python 版本
python -V

# 查看 Python 路径
which python

# 运行 Pipeline（传入月份参数）
python pipeline.py 12

# 查看生成的 parquet 文件
ls

# 应该看到：
* output_12.parquet
* pipeline.py

# 退出容器
exit

# ==========================================
# 直接运行容器（无需进入 Bash）
# ==========================================

# 等价于： python pipeline.py 12

docker run --rm test:pandas 12

# ==========================================
# Git 提交代码
# ==========================================

cd /workspaces/docker-workshop

# 查看状态
git status

# 添加文件
git add .

# 提交
git commit -m "Add dockerized pipeline example"

# 同步远程仓库
git pull --rebase origin main

# 推送到 GitHub
git push origin main


# ==========================================
# 构建一个支持uv的python Docker环境，为后续在容器中安装依赖、运行项目代码做准备
# ==========================================

``` text
本地项目根目录
        ↓
使用 pipeline/Dockerfile 构建 Docker 镜像
        ↓
基于 Python 3.13.11 slim 创建容器环境
        ↓
从 uv 官方镜像复制 uv 工具
        ↓
把 pyproject.toml、.python-version、uv.lock 复制进容器
        ↓
进入容器 /code 目录
        ↓
验证 uv 项目配置文件是否存在

```

## Docker + uv 构建环境理解

这一步主要是在 Docker 容器中准备一个基于 Python 3.13.11 和 uv 的项目运行环境。

### Dockerfile 内容

```dockerfile
FROM python:3.13.11-slim                                # 这个Docker镜像基于官方python3.13.11 slim镜像构建

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/         # 表示从uv 官方镜像中复制uv

WORKDIR /code

COPY pyproject.toml .python-version uv.lock ./
```


### 这段Docker 在做什么？
``` bash
# 表示这个Docker 镜像基于官方python3.13.11 slim镜像构建。
FROM python:3.13.11-slim

```

``` bash
# 表示从当前uv官方镜像中复制uv 命令到当前镜像的 /bin/ 目录中
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
```
这样容器内部就可以使用：
``` bash
uv
```

```dockerfile
WORKDIR /code
```

表示设置容器内部的工作目录为：
```bash
/code
```
后续命令都会在`/code` 目录下执行。
```bash
COPY pyproject.toml .python-version uv.lock ./
```

表示把宿主机项目根目录中的以下文件复制到容器内部`/code`目录：
``` text
pyproject.toml  # 项目配置文件
.python-version   # 指定python版本
uv.lock              # 锁定依赖版本
```


Build命令：
```
因为Dockerfile 放在`pipeline/` 文件夹里，但`pyproject.toml`、 `.python-version` 和 `uv.lock` 在 项目根目录，所以需要在项目根目录执行：

```bash
cd/workspaces/ docker-workshop
docker build -t test: pandas -f pipeline/Dockerfile
```

含义：
```
docker build
```

构建Docker 镜像
```
-t test:pandas      #给镜像命名为：test：pandas
```

因此Docker可以找到：
``` text
pyproject.toml
.python-version
uv.lock
pipeline/Dockerfile
```


##  进入容器
```
docker run -it --rm --entrypoint=bash test:pandas
```

- docker run: 启动一个容器
- it： 进入交互模式
- rm： 退出后自动删除这个临时容器
-- entrypoint= bash：覆盖Dockerfile默认入口，直接进入bash
- test：pandas： 使用刚刚构建好的镜像


#在容器中验证文件：

进入容器后：
```
ls
```
输出： pyproject.toml uv.lock

此时没有看到`.python-version`,是因为以`.` 开头的文件是隐藏文件。

使用：
```
ls -a
```

输出：
```
.  ..  .python-version  pyproject.toml  uv.lock
```
说明这三个文件已经成功复制进Docker容器的 `/code` 目录











