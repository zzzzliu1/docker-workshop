{% snapshot customer_snapshot %}


{{
    config(
        target_schema='taxi_rides_ny',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at'
    )
}}


select

    customer_id,

    customer_name,

    status,

    current_timestamp() as updated_at


from {{ ref('customers') }}


{% endsnapshot %}