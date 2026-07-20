# NYC Taxi Analytics Engineering Pipeline

An end-to-end analytics engineering project built with dbt and BigQuery.

The project demonstrates modern analytics engineering practices including:

- ELT pipeline development
- Dimensional modeling
- Data quality testing
- Source freshness monitoring
- SCD Type 2 historical tracking
- Automated documentation


# Architecture Diagram
``` text
Source
 |
BigQuery
 |
dbt
 |
Staging
 |
Intermediate
 |
Marts
 |
BI Analytics
```


# Tech Stack
``` markdown
## Tech Stack

- SQL
- dbt Core
- BigQuery
- Python
- uv
- Git
- Docker
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
![Uploading image.png…]()









