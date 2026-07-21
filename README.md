# NYC Taxi Data Engineering Pipeline 🚕


## Project Overview

This project implements an end-to-end modern data engineering pipeline using the Google Cloud data stack.

The goal is to build a scalable pipeline that ingests NYC Taxi trip data, processes raw data into analytics-ready datasets, applies data transformation using dbt, and automatically validates changes through CI/CD.


The project demonstrates a complete Data Engineering workflow:

- ELT pipeline development
- Dimensional modeling
- Data quality testing
- Source freshness monitoring
- SCD Type 2 historical tracking
- Automated documentation


## Architecture Overview
``` text
NYC Taxi API
        |
        |
        v

01-data-ingestion-airflow

(Python + Docker + Airflow)

        |
        |
        v

Parquet Files

        |
        |
        v

02-data-warehouse-bigquery

(BigQuery)

        |
        |
        v

03-data-transformation-dbt

(dbt + BigQuery)

        |
        |
        v

Analytics Layer

        |
        |
        v

GitHub Actions CI/CD
```


## Tech Stack
``` markdown
# Technology Stack


## Data Engineering

| Category | Technology |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas |
| Package Management | uv |
| Containerization | Docker |
| Workflow Orchestration | Apache Airflow |


## Cloud Data Platform

| Category | Technology |
|---|---|
| Cloud Provider | Google Cloud Platform |
| Data Warehouse | BigQuery |
| Storage | Google Cloud Storage |


## Analytics Engineering

| Category | Technology |
|---|---|
| Transformation Framework | dbt Core |
| Modeling Language | SQL |
| Data Modeling | Staging / Intermediate / Mart Layers |


## DevOps

| Category | Technology |
|---|---|
| Version Control | Git / GitHub |
| CI/CD | GitHub Actions |
| Environment Management | GitHub Secrets |


---

# Repository Structure

```

# dbt Features
## Data Modeling
``` text
staging
intermediate
marts
```

## Testing
``` text
8 automated tests:

- not_null
- accepted_values
```

## Freshness
```text
dbt source freshness

warn:
24 hours

error:
48 hours
```


## SCD Type 2
```text
Implemented dbt snapshot strategy:

strategy = timestamp

Tracking:

dbt_valid_from
dbt_valid_to
```

# Documentation
<img width="1264" height="540" alt="image" src="https://github.com/user-attachments/assets/d8a1f061-d646-495a-899b-14c46c11691f" />

# PROJECT STRUCTURE
``` text
docker-workshop


├── pipeline-01-data-ingestion
│
│   Extract and load data pipeline
│
│   ├── Python ingestion scripts
│   ├── Docker environment
│   ├── Airflow DAGs
│   ├── Parquet generation
│
│
├── pipeline-02-data-warehouse
│
│   Cloud warehouse implementation
│
│   ├── BigQuery partitioning
│   ├── BigQuery clustering
│   ├── Warehouse optimization SQL
│
│
├── pipeline-03-analytics-engineering
│
│   dbt transformation layer
│
│   └── taxi_rides_ny
│
│       ├── models
│       ├── tests
│       ├── sources.yml
│       └── dbt_project.yml
│
│
├── pipeline-04-testing-cicd
│
│   Data quality and automation
│
│   └── GitHub Actions workflow
│
│
├── .github
│
│   └── workflows
│
│       └── dbt-ci.yml
│
│
└── README.md
```

# Pipeline Workflow


# Pipeline 01 - Data Ingestion


## Purpose

Extract NYC Taxi trip data and prepare raw datasets for downstream analytics processing.


## Workflow


```
NYC Taxi Dataset

        |

        v

Python Data Pipeline

        |

        v

Parquet Files

        |

        v

Cloud Storage / Warehouse Loading

```


## Tools

- Python
- Docker
- uv
- Apache Airflow


## Main Components


```
pipeline.py

ingest_data.py

Dockerfile

docker-compose.yaml

Airflow DAG

```

---

# Pipeline 02 - Data Warehouse


## Purpose

Design and optimize the cloud data warehouse layer using BigQuery.


## Data Warehouse Architecture


```
Raw Data

   |

   v

BigQuery Dataset

   |

   v

Partitioned Tables

   |

   v

Clustered Tables

```


## Implementations


### Partitioning

Optimize query performance by partitioning large datasets based on date fields.


### Clustering

Improve analytical query performance by clustering frequently filtered columns.


## Tools

- Google BigQuery
- SQL


---

# Pipeline 03 - Analytics Engineering


## Purpose

Transform raw warehouse data into analytics-ready datasets using dbt.


## dbt Layer Architecture


```
                 Raw Layer

                     |

                     v


              Staging Layer

          stg_yellow_tripdata


                     |

                     v


          Intermediate Layer

              int_trips


                     |

                     v


              Mart Layer

             fact_trips

```


---

# dbt Implementation


## dbt Models


Example structure:


```
taxi_rides_ny

├── models

│
├── staging

│   └── stg_yellow_tripdata.sql

│
├── intermediate

│   └── int_trips.sql

│
└── marts

    └── fact_trips.sql

```


---

# Data Quality Testing


Implemented dbt tests:


- not_null tests
- schema validation
- source validation


Example:


```
dbt build

```

runs:

```
dbt run

+

dbt test

```

automatically.


---

# Pipeline 04 - Testing & CI/CD


## Purpose

Automatically validate every code change before merging into the main branch.


## CI/CD Workflow


```
Developer Commit

        |

        v


GitHub Pull Request

        |

        v


GitHub Actions Trigger

        |

        v


Install Python Environment

        |

        v


Install dbt-bigquery

        |

        v


Authenticate Google Cloud

        |

        v


Generate dbt Profile

        |

        v


Run dbt Build

        |

        v


Run dbt Tests

        |

        v


Merge Ready

```


---

# GitHub Actions


Workflow file:


```
.github/workflows/dbt-ci.yml

```


The CI pipeline performs:


1. Checkout repository

2. Setup Python environment

3. Install dbt-bigquery

4. Authenticate GCP service account

5. Create dbt profiles.yml

6. Execute:

```
dbt deps

dbt build

```


---

# Running the Project Locally


## Step 1 - Clone Repository


```bash
git clone https://github.com/zzzzliu1/Data-Engineer-Project.git

cd docker-workshop
```


---

# Step 2 - Run Data Pipeline


Navigate:


```bash
cd pipeline-01-data-ingestion
```


Install dependencies:


```bash
uv sync
```


Run ingestion:


```bash
python pipeline.py
```


---

# Step 3 - Run dbt Transformation


Navigate:


```bash
cd pipeline-03-analytics-engineering/taxi_rides_ny
```


Install dbt:


```bash
pip install dbt-bigquery
```


Run:


```bash
dbt deps

dbt build

```


---

# Data Modeling


## Fact Table


```
fact_trips

```


Contains:

- Trip information
- Revenue metrics
- Passenger information
- Time-based analysis


---

## Analytics Summary


Example:


```
daily_trip_summary

```


Contains:

- Daily trip volume
- Revenue aggregation
- Usage trends


---

# Engineering Practices Demonstrated


This project demonstrates:


✅ End-to-end ETL pipeline development

✅ Data ingestion automation

✅ Cloud data warehouse implementation

✅ BigQuery optimization

✅ Analytics engineering with dbt

✅ SQL-based data modeling

✅ Docker containerization

✅ Airflow orchestration

✅ Automated testing

✅ CI/CD implementation


---

# Future Improvements


Potential production enhancements:


- Deploy Airflow to managed environment

- Add Terraform infrastructure as code

- Add dbt documentation deployment

- Add data visualization dashboard

- Add automated data quality monitoring

- Implement production DataOps workflow


---

# Author


## Zixuan Liu


Data Engineer | Analytics Engineer






