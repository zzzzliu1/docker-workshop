CREATE OR REPLACE TABLE
`project-feeaf819-de7f-4c20-897.ny_taxid.yellow_tripdata_partitioned`

PARTITION BY DATE(tpep_pickup_datetime)

AS

SELECT *

FROM
`project-feeaf819-de7f-4c20-897.ny_taxid.yellow_tripdata`;
