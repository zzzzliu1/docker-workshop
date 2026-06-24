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


#### 插曲：与之前PostgreSQL容器断开连接之后需要重新启动两个任务
1. PostgreSQL容器
2. Jupter Notebook

建议用两个Terminal分别跑：

一、Terminal1: 重新启动PostgreSQL容器
``` bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```
保持这个terminal不要关。

二、Terminal2: 重新启动Jupter
```bash
cd /workspaces/docker-workshop/pipeline

uv run jupyter notebook --ip=0.0.0.0 --port=8888
```
然后重新打开浏览器里的Jupter地址：
```
http://127.0.0.1:8888
```

打开：
```
notebook.ipynb
```

三、Terminal3: 验证PostgreSQL 是否连接成功
```bash
cd /workspaces/docker-workshop/pipeline

uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

密码输入：
root

进入后执行：
``` sql
\dt
```

应该能看到之前的表：
``` bash
test
yellow_taxi_data
```

# 总结Chpater6- Ingesting NYC Taxi data into PostgreSQL


<img width="2560" height="1540" alt="image" src="https://github.com/user-attachments/assets/ee9b0d00-566d-4eda-80c2-14e43800ec59" />

<img width="2560" height="1540" alt="image" src="https://github.com/user-attachments/assets/0777b734-13be-47b0-9e9b-d25d1e70e2b0" />


整体流程图：
``` text
NYC Taxi CSV (.csv.gz)
          ↓
      Pandas
          ↓
   Data Cleaning
          ↓
 SQLAlchemy Engine
          ↓
 PostgreSQL Container
          ↓
 yellow_taxi_data
```

目标： 把NYC Taxi CSV 文件导入PostgreSQL 数据库

Step1: 创建Jupter 环境
Terminal：
进入项目：
``` bash
cd /workspaces/docker-workshop/pipeline
```

安装Jupter:
``` bash
uv add --dev jupyter
```

启动Notebook：
```bash
uv run jupyter notebook
```
作用：
启动notebook环境用于数据探索


Step2: 导入Pandas
Jupter
```
import pandas as pd
```

作用： 使用pandas 读取和处理数据

Step3: 下载NYC Taxi数据
Jupter:
``` python
prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"

url = f"{prefix}/yellow_tripdata_2021-01.csv.gz"
```

作用：构造NYC Taxi CSV 下载地址

Step4: 读取数据
``` python

df= pd.read_csv(url)
```
作用：把CSV加载到DataFrame

查看数据：
```python
df.head()
```

查看结构：
df.shape

查看类型：
df.dtypes


Step6: 处理DtypeWarning
问题：
读取大CSV时：
```bash
pd.read_csv(url)
```
可能报：
DtypeWarning:
Columns have mixed types

原因：
同一列中存在不同数据类型

解决方案：
显式指定类型：
```text
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
```

Step7: 解析时间字段
Jupter：
``` python
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]
```

作用：
字符串
↓
datetime

Step 8 创建 PostgreSQL 容器
TErminal：
```bash
docker run -it \
-e POSTGRES_USER=root \
-e POSTGRES_PASSWORD=root \
-e POSTGRES_DB=ny_taxi \
-v ny_taxi_postgres_data:/var/lib/postgresql \
-p 5432:5432 \
postgres:18
```

作用：启动PostgreSQL 数据库
```text
参数：
参数	作用
POSTGRES_USER	root
POSTGRES_PASSWORD	root
POSTGRES_DB	ny_taxi
-p 5432:5432	暴露数据库端口
-v	持久化数据库

```

Step9: 安装PostgreSQL Driver
Terminal：
```bash
uv add sqlalchemy "psycopg[binary,pool]"
```

作用：
```text
Pandas
↓
SQLAlchemy
↓
PostgreSQL

```

Step 10: 创建数据库连接
Jupter
``` python
from sqlalchemy import create_engine
```

创建engineer：
``` python
engine = create_engine(
    "postgresql+psycopg://root:root@localhost:5432/ny_taxi"
)
```

作用：连接PostgreSQL


Step11:查看生成的SQL
Jupter
```python
print(
    pd.io.sql.get_schema(
        df,
        name="yellow_taxi_data",
        con=engine
    )
)

```

作用：查看pandas 推断出的建表SQL
生成：
```bash
CREATE TABLE yellow_taxi_data (...)
```

Step12: 创建表结构
Jupter
```python
df.head(0).to_sql(
    name="yellow_taxi_data",
    con=engine,
    if_exists="replace"
)
```

作用：
只创建表
不插入数据

为什么用head(0)?  
返回： 0 rows 全部columns
因此： 得到Schema 不写数据


Step13: Chunk Reading
大文件：1.3 million rows 不能一次全部读入内存
创建Iterator
``` python
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)
```
作用： 每次读取100000行

Step14: 测试Iterator

```python
for df_chunk in df_iter:
    print(len(df_chunk))
```
输出：
100000
100000
100000
。。。

说明： CSV被拆成多个批次


Step15:插入一个 Chunk
``` python
df_chunk.to_sql(
    name="yellow_taxi_data",
    con=engine,
    if_exists="append"
)
```
作用： 追加写入数据库


Step16: 完整Ingestion
```python
first = True

for df_chunk in df_iter:

    if first:

        df_chunk.head(0).to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="replace"
        )

        first = False

    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )

    print(len(df_chunk))

```

流程：
```text
第一批：
    创建表

后续批次：
    插入数据
```


Step18: 添加进度条
Terminal
```bash
uv add tqdm
```

Jupter:
```python
from tqdm.auto import tqdm
```
创建Iterator
```python
for df_chunk in tqdm(df_iter):

    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )
```

Step19: 创建数据
Terminal
连接PostgreSQL
```
uv run pgcli \
-h localhost \
-p 5432 \
-u root \
-d ny_taxi
```

输入密码：root
查看表：\dt
结果：
test
yellow_taxi_data

Step20: 验证数据量
``` sql
SELECT count(1)
FROM yellow_taxi_data;
```

核心知识点：
```text
1. Docker 运行 PostgreSQL

2. Jupyter 数据探索

3. Pandas CSV 读取

4. dtype 指定

5. datetime 转换

6. SQLAlchemy Engine

7. DataFrame → SQL

8. head(0) 建表

9. chunk ingestion

10. tqdm 进度监控

11. pgcli 数据验证

12. PostgreSQL 数据仓库存储
```



# ==========================================
# Dockerizing the Ingestion Script: postgres:18+ taxi_ingest:v001
# ==========================================


<img width="2496" height="1472" alt="image" src="https://github.com/user-attachments/assets/48b0e3be-eb2d-4632-bc19-8ae6406b280b" />


## 当前阶段目标：

我们已经完成了：
1. 使用Docker启动 PostgreSQL数据库容器
2. 使用Jupter+Notebook 读取 NYC Taxi CSV 数据
3. 使用pandasSQLAlchemy将数据写入PostgreSQL
4. 将Notebook 逻辑整理成`ingest_data.py`
5. 使用`ingest_data.py` 成功创建多张表
6. 使用Dockerfile将`ingest_data.py` 打包成 Docker Image：`taxi_ingest:v001`


<img width="678" height="328" alt="image" src="https://github.com/user-attachments/assets/4ec57cf2-f70f-4ae5-85ce-2502b8b1ac6f" />
# 让一个Docker容器中的ingest_data.py 连接到另一个Dockr容器中的PostgreSQL

也就是：
```text
postgres:18 容器
        ↑
        |
taxi_ingest:v001 容器运行 ingest_data.py
```


图片中有两个独立容器：
Container 1:
Postgres：18

这个容器负责运行PostgreSQL数据库，内部端口是： 5432

另一个容器：
Container 2:
taxi_ingest：v001
这个容器运行：ingest_data.py

作用是读取NYC Taxi 数据, 然后写入PostgresQL


# 为什么这里很重要？
之前我们在宿主机terminal里运行：
```bash
uv run python ingest_data.py
```

这表示：
```text
宿主机python脚本
        ↓
连接localhosst：5432
        ↓
PostgreSQL Docker 容器
```


但是现在把脚本也打包成Docker 镜像：
```bash
docker build -t taxi_ingest:v001 .
```
之后运行：

```
docker run taxi_ingest:v001 ...
```


这时结构变成：
``` text
taxi_ingest:v001 容器
        ↓
连接数据库
        ↓
postgres:18 容器
```
这就进入了真正的多容器场景。

——————————————————————————————————————

# Step1: 启动PostgeSQL 容器
在一个terminal中运行，并保持它不要关闭：
```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

含义：
启动PostgreSQL 18
创建用户root
密码root
创建数据库 ny_taxi
把容器 5432 映射到宿主机 5432
使用Docker volume 保存数据

# Step2: 连接PostgreSQL
在另一个terminal中：
```bash
cd /workspaces/docker-workshop/pipeline

uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

输入密码：root
进入数据库后查看表： \dt
我们最终看到： 
test
yellow_taxi_data
yellow_taxi_trips
yellow_taxi_trips_2021_1

说明数据已经成功写入PostgresQL。

## Step3: 验证数据量
```sql
SELECT count(1)
FROM yellow_taxi_trips_2021_1;
```

结果： 1369765

## Ingest_Data.py的作用
`ingest_data.py` 是从 Jupyter Notebook 中整理出来的脚本。

它的核心作用是：
``` text
读取远程 CSV
        ↓
用 pandas 分块读取
        ↓
用 SQLAlchemy 连接 PostgreSQL
        ↓
创建表
        ↓
分批写入数据
```

## ngest_data.py 核心逻辑 
``` python
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

含义：
pandas       读取和处理 CSV
SQLAlchemy   连接 PostgreSQL
tqdm         显示进度条
click        处理命令行参数


## 定义字段类型：
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
    "congestion_surcharge": "float64",
}

目的：
CSV 是 schemaless 的，没有内置字段类型。
所以我们手动告诉 pandas 每一列应该是什么类型。


## 定义时间字段：
```python
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]
```
目的：把字符串时间转换成 datetime 类型。


## 使用click接受命令行参数
```
@click.command()
@click.option("--pg-user", default="root")
@click.option("--pg-pass", default="root")
@click.option("--pg-host", default="localhost")
@click.option("--pg-port", default=5432, type=int)
@click.option("--pg-db", default="ny_taxi")
@click.option("--year", default=2021, type=int)
@click.option("--month", default=1, type=int)
@click.option("--target-table", default="yellow_taxi_data")
@click.option("--chunksize", default=100000, type=int)
```
这些参数让脚本可以通过terminal灵活运行：

```bash
uv run python ingest_data.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --year=2021 \
  --month=1 \
  --target-table=yellow_taxi_trips_2021_1 \
  --chunksize=100000
```




## 构建 CSV 下载地址
``` python
prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"
url = f"{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz"
```


如果：
```
year=2021
month=1
```

那么url是：
yellow_tripdata_2021-01.csv.gz


##  创建数据库连接
```python
engine = create_engine(
    f"postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
)
```

例如： postgresql+psycopg://root:root@localhost:5432/ny_taxi

含义： 用root用户连接 localhost：5432 上的ny_taxi数据库


## 分块读取csv
```python
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=chunksize,
)
```

含义： 
不要一次性读取全部136万行
而是每次读取100000行


## 分块写入PostgreSQL
```bash
first = True

for df_chunk in tqdm(df_iter):
    if first:
        df_chunk.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists="replace",
            index=False,
        )
        first = False

    df_chunk.to_sql(
        name=target_table,
        con=engine,
        if_exists="append",
        index=False,
    )
    
```


逻辑：
```
第一批数据： 创建表结构
每一批数据：append写入PostgresQL
```


## Dockerfile的作用：
我们后来把 `ingest_data.py `打包成 Docker 镜像。

Dockerfile 大致是：
```
 #使用 Python 3.13.11 作为基础环境。
FROM python:3.13.11-slim

#把 uv 工具复制到镜像中。
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/  

# 设置容器内工作目录为 /code。
WORKDIR /code  

#让容器默认使用 uv 创建的虚拟环境。
ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./

#复制依赖配置文件。
RUN uv sync --locked

#根据 uv.lock 安装固定版本依赖。
COPY ingest_data.py .

#把 ingestion 脚本复制进容器。
ENTRYPOINT ["python", "ingest_data.py"]
```

容器启动时默认执行：python ingest_data.py




## 构建 Docker Image
在`pipeline` 目录下执行：
```bash
cd /workspaces/docker-workshop/pipeline

docker build -t taxi_ingest:v001 .
```

含义：
``` text
使用当前目录Dockerfile构建镜像
镜像名： taxi_ingest
标签： v001

构建成功后日志会显示：
naming to docker.io/library/taxi_ingest:v001

说明镜像已经创建成功。


##  当前图片下一步会做什么？
图片中显示两个容器：
postgres:18
taxi_ingest:v001

老师接下来要做的是：
运行 taxi_ingest:v001 容器
让它里面的 ingest_data.py 连接 postgres:18 容器
并把数据写入数据库

这一步的难点是：
容器内部的 localhost
不是宿主机的 localhost
```


<img width="613" height="467" alt="image" src="https://github.com/user-attachments/assets/b7d1157a-fc23-41a4-83b9-f7eadf2e5789" />



# put ingest_data.py from taxi_ingest:v001 -> postgres:18 container的portal：5432中？

即运行 taxi_ingest：v001 容器，让容器里的ingest_data.py连接到 postgre：18 容器的5432端口， 把数据写入PostgreSQL

## 创建一个Docker 内部网络， 让Postgres 容器和 taxi_ingest 容器加入同一个网络，然后它们可以用容器名互相访问

```bash
#创建一个Docker 网络
docker network create pg-network
```

后面会变成：
```text
postgres:18 container
        │
        │ same docker network: pg-network
        │
taxi_ingest:v001 container
```

之后，启动Postgres时加入这个网络，并命名：
```bash
docker run -it --rm \
  --network=pg-network \
  --name pg-database \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

运行Ingestion 容器时也加入同一网络：
```bash
docker run -it --rm \
  --network=pg-network \
  taxi_ingest:v001 \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=pg-database \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips_2021_1 \
  --year=2021 \
  --month=1 \
  --chunksize=100000
```
因为在Docker Network里，容器可以通过容器名互相访问。


<img width="1003" height="596" alt="image" src="https://github.com/user-attachments/assets/51061b92-7999-42da-b256-c0d6932cd272" />

升级成：

Docker Network (pg-network)
│
├── postgres:18 Container
│
└── taxi_ingest:v001 Container

第一部分：理解图1
图1本质上在表达：
┌─────────────────────────────┐
│        pg-network           │
│                             │
│  postgres:18               │
│      5432                  │
│                             │
│  taxi_ingest:v001          │
│      ingest_data.py        │
│            │               │
│            └──────►5432    │
└─────────────────────────────┘

意思： 
Postgres Container
里面运行： PostgreSQL Database 
监听：5432


taxi_ingest Container
里面运行： ingest_data.py
作用：
下载 CSV
↓
读取 CSV
↓
连接 PostgreSQL
↓
写入数据


pg-database就是Postgres 容器名字。-- 容器DNS名称。

## 容器之间如何通信
老师最终想达到：
ingest_data.py
        │
        ▼
postgresql://root:root
@pgdatabase:5432
/ny_taxi
        │
        ▼
Postgres Container

这里已经完全不需要：localhost了。

## Data Engineer面试中非常高频，可以用一句话总结：
Docker Network的作用是让多个容器处于同一个虚拟网络中， 通过容器名称（DNS）直接通信，而不依赖localhost或宿主机端口映射。 Postgres容器和ETL/Ingestion容器加入同一个Network后，
ingest_data.py 可以通过`postgresql://user:pass@container_name:5432/db` 直接写入数据库。

# 下一步： 在同一个Docker network：`pg-network` 里面再加入一个pgAdmin容器。
<img width="1225" height="638" alt="image" src="https://github.com/user-attachments/assets/9bee8a3b-c841-45e0-900e-5b7e5e7a6911" />

整体结构变成：
``` text
pg-network
├── pgdatabase        # PostgreSQL 容器，端口 5432
├── taxi_ingest:v001  # 数据导入容器，运行 ingest_data.py
└── pgadmin           # 数据库管理网页工具，浏览器访问 8085
```
pgAdmin 的作用时：用网页界面查看和管理PostgreSQL数据库，类似你之前用`pgcli`,但它是图形化界面。

现在要执行这一步：
``` bash
docker run -it --rm \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

它做的事情是：
1.启动 pgAdmin 容器
2.默认登录邮箱：admin@admin.com
3.默认登录密码：root
4.把容器内部 80 端口映射到本机 8085
5.加入 pg-network
6.容器名叫 pgadmin

具体操作步骤：

step1: 创建一个新的terminal
step2: 检查pg-network是否存在
先执行：
```
docker network ls
```

应该看到：
NETWORK ID     NAME
xxxxxxxxxx     pg-network

如果有：pg-network 说明创建成功

step3: 确认Postgres还活着
你之前应该有一个Terminal正在运行：
```bash
docker run -it --rm \
  --network=pg-network \
  --name pgdatabase \
  ...
```
不要关闭。

检查：
``` bash
docker ps
```

应该看到：
``` bash
postgres:18
```
以及：
```
pgdatabase
```

类似：
```
CONTAINER ID
IMAGE          postgres:18
NAMES          pgdatabase

```

step4: 启动pgAdmin
在新Terminal中执行：
```bash
docker run -it --rm \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

step5: 等待出现类似日志
最终应该看到：
```
Booting pgAdmin 4 server...
```
或者：
```
Starting pgAdmin...
```
不要关闭这个Terminal

step6: 打开浏览器
打开：
```bash
http://localhost:8085
```

step7: 登陆pgAdmin
输入：
```
Email:
admin@admin.com
```

```
Password:
root
```

step8: 添加PostgreSQL Server
<img width="623" height="510" alt="image" src="https://github.com/user-attachments/assets/a6fed651-0f80-483b-9aae-29ff6044c155" />

现在的容器关系应该是：
```text
pg-network
│
├── pgdatabase
│      PostgreSQL
│      port 5432
│
├── taxi_ingest:v001
│      ingest_data.py
│
└── pgadmin
       Web UI
       port 8085
```


# ==========================================
# Docker+PostgreSQL+Ingestion+PgAdmin 学习总结
# ==========================================

## 今日最终成果

今天最终完成了：

NYC Taxi CSV 数据
        ↓
ingest_data.py
        ↓
taxi_ingest:v001 Docker Image
        ↓
PostgreSQL Docker Container
        ↓
pgAdmin 图形化查看数据

最终在pgAdmin 中成功看到：
```
test
yellow_taxi_data
yellow_taxi_trips
yellow_taxi_trips_2021_1
```

并验证：
```bash
select count(1) from public.yellow_taxi_trips_2021_1;
```
结果： 1369765
说明： 2021年1月NYC Yellow Taxi数据已经成功导入PostgreSQL

运行步骤总结：
1. 启动PostgreSQL 容器
运行位置： Terminal1
```bash
docker run -it --rm \
  --network=pg-network \
  --name pgdatabase \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```
目的：启动一个PostgreSQL 18 数据库容器
<img width="614" height="402" alt="image" src="https://github.com/user-attachments/assets/ea4dbbae-cc6a-4adc-90a6-c042480d44cf" />

2. 创建Docker Network
运行位置：Terminal
```bash
docker network create pg-network
```
目的：创建一个Docker内部网络，让多个容器可以互相通信
pg-network
├── pgdatabase
├── taxi_ingest:v001
└── pgadmin
即：在同一个Docker Network中，容器之间可以通过容器名访问。
例如：
taxi_ingest 容器访问 pgdatabase:5432
pgAdmin 容器访问 pgdatabase:5432

3. 在jupter中探索数据

运行位置： Jupter Notebook
```python
import pandas as pd

prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"
url = f"{prefix}/yellow_tripdata_2021-01.csv.gz"

df = pd.read_csv(url, nrows=100)
df.head()
df.dtypes
df.shape
```

目的： 先用Notebook探索NYC Taxi CSV数据结构。

4. 定义数据类型和时间字段
运行位置： Jupter/ingest_data.py
代码：
```
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
    "congestion_surcharge": "float64",
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]
```

5. 创建SQLAlchemy连接
运行位置：Jupyter / ingest_data.py

代码：
```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://root:root@localhost:5432/ny_taxi"
)
```
目的： 让Python 可以连接PostgreSQL

6. 分块读取CSV并写入PostgreSQL
运行位置： Jupyter / ingest_data.py
```
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000,
)
```
目的： 不要一次性读取全部136万行，而是每次读取100000行。

写入数据库
```python
first = True

for df_chunk in tqdm(df_iter):
    if first:
        df_chunk.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists="replace",
            index=False,
        )
        first = False

    df_chunk.to_sql(
        name=target_table,
        con=engine,
        if_exists="append",
        index=False,
    )
```

目的：
第一批chunk：创建表结构
后续chunk： 追加写入数据


7. 整理成ingest_data.py
运行位置： VS Code编辑器
目的： 把Jupter Notebook中的实验代码整理成可重复执行的python脚本。
注意点：
从Notebook 转成.py时要删除：
```python
get_ipython().system(...)
```

因为这是Jupter专用语法，普通python脚本不能运行。

8. 使用Click 接收命令行参数
```python
`@click.command()
@click.option("--pg-user", default="root")
@click.option("--pg-pass", default="root")
@click.option("--pg-host", default="localhost")
@click.option("--pg-port", default=5432, type=int)
@click.option("--pg-db", default="ny_taxi")
@click.option("--year", default=2021, type=int)
@click.option("--month", default=1, type=int)
@click.option("--target-table", default="yellow_taxi_data")
@click.option("--chunksize", default=100000, type=int)
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize):
    ...
```
目的： 让脚本可以通过terminal传参运行。

9. 本地运行 ingest_data.py
运行位置： Terminal，pipeline目录

代码：
```bash
cd /workspaces/docker-workshop/pipeline

uv run python ingest_data.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --year=2021 \
  --month=1 \
  --target-table=yellow_taxi_trips \
  --chunksize=100000
```
目的： 从宿主机运行Python脚本，把数据写入 PostgreSQL容器。

10. 创建带年月的表名
```bash
uv run python ingest_data.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --year=2021 \
  --month=1 \
  --target-table=yellow_taxi_trips_2021_1 \
  --chunksize=100000
```

目的： 创建更规范的表明 yellow_taxi_trips_2021_1
代表： 2021年1月Yellow Taxi Trips数据

11. 用pgcli验证表
运行位置： Terminal
```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```
输入密码：root
查看表： \dt
查询行数：
```sql
select count(1) from yellow_taxi_trips_2021_1;
```
12. 构建ingestion Docker 镜像
运行位置： Terminal，pipeline目录

Dockerfile
``` dockerfile
FROM python:3.13.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./

RUN uv sync --locked

COPY ingest_data.py .

ENTRYPOINT ["python", "ingest_data.py"]
```

build 代码：
```bash
cd /workspaces/docker-workshop/pipeline

docker build -t taxi_ingest:v001 .
```

目的：
把`ingest_data.py` 和依赖打包成Docker Image
生成镜像：
taxi_ingest：v001

13.运行taxi_ingest容器
运行位置：Terminal
代码：
```bash
docker run -it --rm \
  --network=pg-network \
  taxi_ingest:v001 \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=pgdatabase \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips_2021_1 \
  --year=2021 \
  --month=1 \
  --chunksize=100000
```
目的：
让ingestion脚本在Docker 容器里运行，并连接PostgreSQL容器

14. 启动pgAdmin 容器
运行位置： 新的Terminal

代码：
``` bash
docker run -it --rm \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

目的：启动pgAdmin 图形化数据库管理工具
``` text
PGADMIN_DEFAULT_EMAIL
登录 pgAdmin 的邮箱

PGADMIN_DEFAULT_PASSWORD
登录 pgAdmin 的密码

-p 8085:80
把容器内部 80 端口映射到本机 8085

--network=pg-network
让 pgAdmin 加入同一个 Docker network

--name pgadmin
容器名叫 pgadmin
```

15. 浏览器打开pgAdmin
地址： http://127.0.0.1:8085/browser/
登录
Email: admin@admin.com
Password: root

16. pgAdmin中连接PostgreSQL
<img width="619" height="377" alt="image" src="https://github.com/user-attachments/assets/b88518b3-e1aa-4266-9453-408f6e8fc004" />

17. 在pgAdmin中查询数据
<img width="627" height="378" alt="image" src="https://github.com/user-attachments/assets/79dad9a3-c50e-4f40-b01a-1d9ccbcc2476" />

今日最终架构：
``` text
pg-network
│
├── pgdatabase
│   └── postgres:18
│       └── ny_taxi database
│
├── taxi_ingest:v001
│   └── ingest_data.py
│       └── CSV → PostgreSQL
│
└── pgadmin
    └── browser UI on localhost:8085
```

今日完成的核心能力：
1. 会用Docker启动PostgreSQL
2. 会用Docker volume持久化数据库
3. 会用Jupyter 探索CSV数据
4. 会用Pandas 分块读取大文件
5. 会用SQLAlchemy写入PostgreSQL
6. 会把Notebook 逻辑整理成python脚本
7. 会用Click便携命令行参数
8. 会用Dockerfile打包ingestion 脚本
9. 会创建Docker Network
10. 会让多个容器通过容器名通信
11. 会启动pgAdmin 图形化管理数据库
12. 会在pgAdmin 中查询PostgreSQL数据

最终：
<img width="2546" height="1528" alt="image" src="https://github.com/user-attachments/assets/51ef8a60-d4ef-4643-89ef-d3b872d41351" />

<img width="2548" height="1504" alt="image" src="https://github.com/user-attachments/assets/337120c1-c883-4e55-8d6c-ff65ab7ec534" />















