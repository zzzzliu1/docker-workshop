#!/usr/bin/env python
# coding: utf-8

# In[32]:
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


# In[33]:


pd.__file__


# In[34]:



url


# In[35]:


df = pd.read_csv(url)


# In[36]:


df.head()


# In[37]:


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

df = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[38]:


df.head()


# In[39]:


len(df)


# In[40]:


df['VendorID']


# In[41]:


df['tpep_pickup_datetime']


# In[42]:


get_ipython().system('uv add sqlalchemy')


# In[43]:


# In[44]:


df.head(0).to_sql(name='yellow_taxi_data',con=engine,if_exists='replace')


# In[45]:


df


# In[46]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[47]:


# Ingesting Data in Chunks
def run():
    pg_user='root'
    pg_pass='root'
    pg_host='localhost'
    pg_port=5432
    pg_db='ny_taxi'

    year=2021
    month=1
    
    target_table='yellow_taxi_data'
    chunksize= 100000
    
    prefix='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    url=f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')


    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000,
    )
    first = True
    for df_chunk in tqdm(df_iter):

        if first:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name= target_table,
                con=engine,
                if_exists="replace"
            )
            first = False    
        df_chunk.to_sql(name= target_table,con=engine,if_exists='append')


# In[48]:


if __name__ == '__main__':
    run()