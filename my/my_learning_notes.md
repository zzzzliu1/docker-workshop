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


# ==========================================
# PostgreSQL + pgcli Docker Demo
# ==========================================

```bash
# 1. 进入pipeline项目目录
cd /workspaces/docker-workshop/pipeline


# 2.激活当前项目的python虚拟环境
source .venv/bin/activate

# 3. 安装pgcli，作为PostgreSQL 命令行客户端
uv add --dev pgcli

# 4. 连接正在运行的PostgreSQL容器
# 参数说明：
# -h localhost      连接本机 localhost
# -p 5432           PostgreSQL 默认端口
# -u root           数据库用户名
# -d ny_taxi        数据库名称
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi

# 连接时输入密码：
# root
```

进入 pgcli 后执行：

``` text
-- 5. 查看当前数据库中的表
\dt

-- 6. 创建测试表
CREATE TABLE test (
    id INTEGER,
    name VARCHAR(50)
);

-- 7. 插入一条测试数据
INSERT INTO test VALUES (1, 'Hello Docker');

-- 8. 查询测试表内容
SELECT * FROM test;

-- 9. 再次查看数据库表
\dt
```


# 进入流程整体在做一件事：
``` text
进入pipeline项目
    ↓
激活python 虚拟环境
    ↓
使用uv 安装pgcli
    ↓
连接Docker中运行的PostgreSQL 数据库
    ↓
进入ny_taxi数据库
    ↓
创建test表
    ↓
插入Hello Docker 测试数据
    ↓
查询数据，验证PostgreSQL可用
```

最终验证：
* Docker PostgreSQL 容器正在运行
* pgcli 可以成功连接数据库
* SQL 可以正常创建表、插入数据、查询数据


# ==========================================
# Get the CSV data with the NewYork taxi trips dataset and put this inside Postgres
# ==========================================


<img width="2560" height="1540" alt="image" src="https://github.com/user-attachments/assets/940c3aa8-cb01-43e7-b139-3a90ded8fbbf" />

<img width="2456" height="1130" alt="image" src="https://github.com/user-attachments/assets/451f6bff-232f-45d2-9d25-c233583694a2" />



# csv is schemaless. Parquet already contains a schema inside the Parquet files. so in Parquet files, you know the types



# ==========================================
# Ingesting Data into Postgres
# ==========================================


In the Jupter notebook, we create code to :
1. Download the CSV file
2. Read it in chunks with pandas
3. Convert datetime columns
4. Insert data into PostgreSQL using SQLAlchemy


Database Created:
<img width="2560" height="1540" alt="image" src="https://github.com/user-attachments/assets/19f79319-d54a-4f94-86c1-6810c6ef8dfc" />


# ==========================================
# 整体总结： Docker+Jupyter+PostgreSQL： Ingest NYC Taxi CSV Data into Postgres
# ==========================================

```text
启动 PostgreSQL Docker 容器
        ↓
用pgcli验证数据库连接
        ↓
安装并启动Jupter Notebook
        ↓
在Jupter 中读取NYC Taxi CSV 数据
        ↓
用pandas 检查数据结构和字段类型
        ↓
用SQLAlchemy连接PostgreSQL
        ↓
创建yellow_taxi_data 表
        ↓
将CSV 数据导入PostgreSQL
        ↓
用pgcli验证表是否创建成功
```


1. Terminal: 启动PostgreSQL 容器
在一个单独的terminal中运行，并保持这个terminal不要关闭：

```bash
# 启动 PostgreSQL 18 容器
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

说明：
``` text
POSTGRES_USER="root"       创建数据库用户 root
POSTGRES_PASSWORD="root"   设置密码 root
POSTGRES_DB="ny_taxi"      创建数据库 ny_taxi
-v ny_taxi_postgres_data   使用 Docker volume 保存数据库数据
-p 5432:5432               将容器 5432 端口映射到本机 5432
postgres:18                使用 PostgreSQL 18 镜像
```

看到类似下面内容表示数据库启动成功：
``` text
database system is ready to accept connections
```


2. Terminal: 进入pipeline项目目录
在另一个terminal中运行：
``` bash
#进入pipeline项目目录
cd/ workspaces/docker-workshop/pipeline

#查看当前目录文件
ls
```

应该能看到：
``` text
Dockerfile
main.py
notebook.ipynb
pipeline.py
pyproject.toml
README.md
uv.lock
```


3. Terminal: 安装pgcli、jupter、SQLAlchemy相关依赖

```bash
# 安装PostgreSQL 命令行客户端
uv add --dev pgcli

# 安装Jupter Notebook
uv add --dev jupyter

# 安装SQLAlchemy 和 PostgreSQL driver
uv add sqlalchemy "psycopg[binary,pool]"

说明：
```text
pgcli       用来在 terminal 中连接 PostgreSQL
jupyter     用来打开 notebook.ipynb
sqlalchemy  用 Python 连接数据库
psycopg     PostgreSQL Python driver
```

4. Terminal: 用pgcli连接PostgreSQL

```bash
# 连接 PostgreSQL 数据库
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

输入密码：
root
成功后会进入：
```
root@localhost:ny_taxi>
```

查看当前数据库中的表：
```bash
\dt
```
退出 pgcli：
```bash
\q
```


5. Terminal: 启动Jupter Notebook

``` bash
# 在pipeline目录启动 Jupter
uv run jupter notebook
```
浏览器会打开 Jupyter 页面：
```
http://127.0.0.1:8888/tree
```

然后新建或打开：
```
notebook.ipynb
```

6. Jupter 读取NYC Taxi CSV 数据
在Jupter Notebook中运行：
```python
import pandas as pd
```

定义数据源地址：
``` bash
prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
url = prefix + "yellow_tripdata_2021-01.csv.gz"
url
```

读取前100行数据做测试：
``` bash
df = pd.read_csv(url, nrows=100)
df.head()
```

查看字段类型：
``` bash
df.dtypes
```

查看数据规模：
```bash

df.shape
```

说明：
- nrows=100 表示只读取前 100 行，用于快速测试。
- CSV 是 schemaless 的，也就是 CSV 本身不保存字段类型。
- Parquet 文件内部包含 schema，所以 Parquet 能保存字段类型信息。


7. Jupter: 指定字段类型和时间字段

为了避免CSV 中字段类型混乱， 可以显示指定dtype：

``` bash
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]
```

重新读取数据：
```bash
df = pd.read_csv(
    url,
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)

df.head()
```

8. Jupter: 创建PostgreSQL连接
```bash
from sqlalchemy import create_engine
```

创建数据库连接： 
``` bash
engine = create_engine(
    "postgresql+psycopg://root:root@localhost:5432/ny_taxi"
)
```

说明：
``` text
root:root        用户名和密码
localhost:5432   PostgreSQL 地址和端口
ny_taxi          数据库名称
```

9. Jupter: 生成SQL 建表语句

```bash
print(pd.io.sql.get_schema(df, name="yellow_taxi_data", con=engine))
```

作用：
```
根据 pandas DataFrame 的字段和类型，生成 PostgreSQL 建表语句。
```

10. Jupter: 创建yellow_taxi_data表
```
df.head(n=0).to_sql(
    name="yellow_taxi_data",
    con=engine,
    if_exists="replace",
    index=False
)
```

说明：
``` text
df.head(n=0)      只保留表结构，不写入数据
to_sql            将 DataFrame 写入 PostgreSQL
if_exists=replace 如果表已存在，就替换
index=False       不把 pandas index 写入数据库
```

这一步只创建表：
yellow_taxi_data
还没有真正插入完整数据。


11. Jupyter：分块读取 CSV 并写入 PostgreSQL

完整数据比较大，所以使用 chunksize 分批读取：
``` bash
df_iter = pd.read_csv(
    url,
    iterator=True,
    chunksize=100000,
    dtype=dtype,
    parse_dates=parse_dates
)
```

先读取第一块数据：
```bash
df = next(df_iter)
df.shape
```

创建表并写入第一批数据：
```
df.head(n=0).to_sql(
    name="yellow_taxi_data",
    con=engine,
    if_exists="replace",
    index=False
)

df.to_sql(
    name="yellow_taxi_data",
    con=engine,
    if_exists="append",
    index=False
)
```

继续写入剩余数据：
``` bash
from time import time

while True:
    try:
        t_start = time()

        df = next(df_iter)

        df.to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="append",
            index=False
        )

        t_end = time()

        print(f"Inserted another chunk, took {t_end - t_start:.3f} seconds")

    except StopIteration:
        print("Finished ingesting data into PostgreSQL")
        break

```

说明： 
```text
iterator=True      开启迭代读取
chunksize=100000   每次读取 100000 行
to_sql append      每次把一个 chunk 追加写入 PostgreSQL
StopIteration      表示 CSV 已经读取完毕
```

12. Terminal：用 pgcli 验证数据表是否创建成功

回到 terminal，连接数据库：
```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

输入密码：
root

查看数据库表：
\dt

成功后应该看到：
``` bash
public | test             | table | root
public | yellow_taxi_data | table | root
```

查询数据：
``` bash
SELECT COUNT(*) FROM yellow_taxi_data;
```

查看前5行：
``` bash
SELECT * FROM yellow_taxi_data LIMIT 5;
```

退出：
``` bash
\q
```

本章完成了一个完整的数据工程Ingestion workflow：
``` text
NYC Taxi CSV 数据源
        ↓
Jupyter Notebook
        ↓
pandas read_csv
        ↓
dtype + parse_dates 数据类型处理
        ↓
SQLAlchemy create_engine
        ↓
PostgreSQL Docker container
        ↓
to_sql 创建表
        ↓
chunksize 分批写入数据
        ↓
pgcli 验证数据库表
```

核心命令总结： 
``` text
# 启动 PostgreSQL
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

# 进入项目
cd /workspaces/docker-workshop/pipeline

# 安装依赖
uv add --dev pgcli
uv add --dev jupyter
uv add sqlalchemy "psycopg[binary,pool]"

# 启动 Jupyter
uv run jupyter notebook

# 连接 PostgreSQL
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```









