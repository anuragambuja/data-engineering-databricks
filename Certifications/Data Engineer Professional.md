[Databricks Certified Data Engineer Professional](https://www.databricks.com/learn/certification/data-engineer-professional)

```
1. A data engineer wants to pass multiple parameters from a Databricks Job to a notebook. They already configured the key and value of each parameter in the configurations of the job. Which of the following utilities can the data engineer use to read the passed parameters inside the notebook ?
  A. dbutils.secrets
  B. dbutils.library
  C. dbutils.fs
  D. dbutils.notebook
  E. dbutils.widgets
 
Ans:  dbutils.widgets.
 Example: Adding a parameter named ‘param1’
    ​​dbutils.widgets.text("param1", "default")
    param1 = dbutils.widgets.get("param1")
```

```
2. Which of the following describes the minimal permissions a data engineer needs to view the metrics and Spark UI of an existing cluster ?
  A. “Can Attach To” privilege on the cluster
  B. “Can Restart” privilege on the cluster
  C. “Can Manage” privilege on the cluster
  D. Cluster creation allowed + “Can Attach To” privileges on the cluster
  E. Cluster creation allowed + “Can Restart” privileges on the cluster

Ans: A.
You can configure two types of cluster permissions:
1- The ‘Allow cluster creation’ entitlement controls your ability to create clusters.
2- Cluster-level permissions control your ability to use and modify a specific cluster. There are four permission levels for a cluster: No Permissions, Can Attach To, Can Restart, and Can Manage. The table lists the abilities for each permission:

Reference: https://docs.databricks.com/security/auth-authz/access-control/cluster-acl.html
```
```
3. For production Databricks jobs, which of the following cluster types is recommended to use?
  A. All-purpose clusters
  B. Production clusters
  C. Job clusters
  D. On-premises clusters
  E. Serverless clusters

Ans: C.
Job Clusters are dedicated clusters for a job or task run. A job cluster auto terminates once the job is completed, which saves cost compared to all-purpose clusters.

In addition, Databricks recommends using job clusters in production so that each job runs in a fully isolated environment.

Reference: https://docs.databricks.com/workflows/jobs/jobs.html#choose-the-correct-cluster-type-for-your-job
```
```
4. The data engineering team has a Delta Lake table created with following query:
  CREATE TABLE target
  AS SELECT * FROM source

A data engineer wants to drop the source table with the following query:
  DROP TABLE source

Which statement describes the result of running this drop command ?

  A. An error will occur indicating that other tables are based on this source table
  B. Both the target and source tables will be dropped
  C. No table will be dropped until CASCADE keyword is added to the command
  D. Only the source table will be dropped, but the target table will be no more queryable
  E. Only the source table will be dropped, while the target table will not be affected

Ans: E.
CREATE TABLE AS SELECT statements, or CTAS statements create new Delta tables and populate them using the output of a SELECT query. So, when dropping the source table, the target table will not be affected.

Reference: (cf. AS query clause): https://docs.databricks.com/sql/language-manual/sql-ref-syntax-ddl-create-table-using.html
```
```
5. Which of the following describes the minimal permissions a data engineer needs to start and terminate an existing cluster ?
  A. “Can Attach To” privilege on the cluster
  B. Cluster creation allowed + “Can Restart” privileges on the cluster
  C. Can Restart” privilege on the cluster
  D. “Can Manage” privilege on the cluster
  E. Cluster creation allowed + “Can Attach To” privileges on the cluster

Ans:  C.
```
```
6. The data engineering team has a Delta Lake table created with following query:
  CREATE TABLE customers_clone
  LOCATION 'dbfs:/mnt/backup'
  AS SELECT * FROM customers

A data engineer wants to drop the table with the following query:
  DROP TABLE customers_clone

Which statement describes the result of running this drop command ?

  A. An error will occur as the table is deep cloned from the customers table
  B. An error will occur as the table is shallowly cloned from the customers table
  C. Only the table's metadata will be deleted from the catalog, while the data files will be kept in the storage
  D. Both the table's metadata and the data files will be deleted
  E. The table will not be dropped until VACUUM command is run

Ans: C.
External (unmanaged) tables are tables whose data is stored in an external storage path by using a LOCATION clause.

When you run DROP TABLE on an external table, only the table's metadata is deleted, while the underlying data files are kept.
```
```
7. Which of the following describes the minimal permissions a data engineer needs to edit the configurations of an existing cluster ?
  A. “Can Restart” privilege on the cluster
  B. “Can Manage” privilege on the cluster
  C. Cluster creation allowed + “Can Restart” privileges on the cluster
  D. Cluster creation allowed + “Can Manage” privileges on the cluster
  E. Only administrators can edit the configurations on existing clusters

Ans: B.
You can configure two types of cluster permissions:
1- The ‘Allow cluster creation’ entitlement controls your ability to create clusters.
2- Cluster-level permissions control your ability to use and modify a specific cluster. There are four permission levels for a cluster: No Permissions, Can Attach To, Can Restart, and Can Manage. The table lists the abilities for each permission:
```
```
8 . Given the following code block in a notebook
  db_password = dbutils.secrets.get(scope="dev", key="database_password")
   print (db_password)

Which statement describes what will happen when the above code is executed?

  A. An interactive input box will appear in the notebook
  B. The string "REDACTED" will be printed.
  C. The error message “Secrets can not be printed” will be shown
  D. The string value of the password will be printed in plain text.
  E. If the user has “Can Read” permission, the string value of the password will be printed in plain text. Otherwise, the string "REDACTED" will be printed.

Ans: B.
Databricks Secrets allows you to securely store your credentials and reference them in notebooks and jobs.
To prevent accidentally printing a secret to standard output buffers or displaying the value during variable assignment, Databricks redacts secret values that are read using dbutils.secrets.get().
When displayed in notebook cell output, the secret values are replaced with [REDACTED] string.
```
```
9. A junior data engineer is using the %sh magic command to run some legacy code. A senior data engineer has recommended refactoring the code instead.
  Which of the following could explain why a data engineer may need to avoid using the %sh magic command ?

  A. %sh restarts the Python interpreter. This clears all the variables declared in the notebook
  B. %sh executes shell code only on the local driver machine which leads to significant performance overhead.
  C. %sh can not access storage to persist the output
  D. All the above reasons explain why %sh may need to be avoided
  E. None of these reasons correctly describe why %sh may need to be avoided

Ans: B.
Databricks support the %sh auxiliary magic command to run shell code in notebooks. This command runs only on the Apache Spark driver, and not on the worker nodes.
```
```
10. Given a Delta table ‘products’ with the following schema:
  name STRING, category STRING, expiration_date DATE,  price FLOAT

When executing the below query:
  SELECT * FROM products
  WHERE price > 30.5

Which of the following will be leveraged by the query optimizer to identify the data files to load?

  A. Columns statistics in the Hive metastore
  B. Columns statistics in the metadata of Parquet files
  C. Files statistics in the Delta transaction log
  D. Files statistics in the in the Hive metastore
  E. None of the above. All data files are fully scanned to identify the ones to load

Ans: C.
In the Transaction log, Delta Lake captures statistics for each data file of the table. These statistics indicate per file:
  Total number of records
  Minimum value in each column of the first 32 columns of the table
  Maximum value in each column of the first 32 columns of the table
  Null value counts for in each column of the first 32 columns of the table

When a query with a selective filter is executed against the table, the query optimizer uses these statistics to generate the query result. it leverages them to identify data files that may contain records matching the conditional filter.
For the SELECT query in the question, The transaction log is scanned for min and max statistics for the price column.
```
```
11. The data engineering team has a table ‘orders_backup’ that was created using Delta Lake’s SHALLOW CLONE functionality from the table ‘orders’. Recently, the team started getting an error when querying the ‘orders_backup’ table indicating that some data files are no longer present.
Which of the following correctly explains this error ?

  A. The VACUUM command was run on the orders table
  B. The VACUUM command was run on the orders_backup table
  C. The OPTIMIZE command was run on the orders table
  D. The OPTIMIZE command was run on the orders_backup table
  E. The REFRESH command was run on the orders_backup table

Ans: A.
With Shallow Clone, you create a copy of a table by just copying the Delta transaction logs.
That means that there is no data moving during Shallow Cloning.
Running the VACUUM command on the source table may purge data files referenced in the transaction log of the clone. In this case, you will get an error when querying the clone indicating that some data files are no longer present.

Reference: https://docs.databricks.com/delta/clone.html
```
```
12. A data engineer has a Delta Lake table named ‘orders_archive’ created using the following command:
  CREATE TABLE orders_archive
  DEEP CLONE orders
They want to sync up the new changes in the orders table to the clone.
Which of the following commands can be run to achieve this task ?

  A. REFRESH orders_archive
  B. SYNC orders_archive
  C. INSERT OVERWRITE orders_archive
     SELECT * FROM orders
  D. CREATE OR REPLACE TABLE orders_archive
     DEEP CLONE orders
  E. DROP TABLE orders_archive;
     CREATE TABLE orders_archive
     DEEP CLONE orders

Ans: D.
Cloning can occur incrementally. Executing the CREATE OR REPLACE TABLE command can sync changes from the source to the target location.
Now, If you run DESCRIBE HISTORY orders_archive, you will see a new version of CLONE operation occurred on the table.
* The last choice in the question is incorrect since dropping the table will lead to removing all the table's history.
```
```
13. The data engineering team has a Delta Lake table named ‘daily_activities’ that is completely overwritten each night with new data received from the source system.
For auditing purposes, the team wants to set up a post-processing task that uses Delta Lake Time Travel functionality to determine the difference between the new version and the previous version of the table. They start by getting the current table version via this code:
  current_version = spark.sql("SELECT max(version) FROM (DESCRIBE HISTORY daily_activities)").collect()[0][0]

Which of the following queries can be used by the team to complete this task ?

  A. SELECT * FROM daily_activities
     UNION
     SELECT * FROM daily_activities AS VERSION = {current_version-1}
  B. SELECT * FROM daily_activities
     UNION ALL
     SELECT * FROM daily_activities@v{current_version-1}
  C. SELECT * FROM daily_activities
     INTERSECT
     SELECT * FROM daily_activities AS VERSION = {current_version-1}
  D. SELECT * FROM daily_activities
     EXCEPT
     SELECT * FROM daily_activities@v{current_version-1}
  E. SELECT * FROM daily_activities
     MINUS
     SELECT * FROM daily_activities AS VERSION = {current_version-1}

Ans: D. 
Each operation that modifies a Delta Lake table creates a new table version. You can use history information to audit operations or query a table at a specific point in time using:
Version number:
  SELECT * FROM my_table@v36
  SELECT * FROM my_table VERSION AS OF 36
Timestamp:
  SELECT * FROM my_table TIMESTAMP AS OF "2019-01-01"
Using the EXCEPT set operator, you can get the difference between the new version and the previous version of the table
```
```
14. The data engineering team wants to build a pipeline that receives customers data as change data capture (CDC) feed from a source system. The CDC events logged at the source contain the data of the records along with metadata information. This metadata indicates whether the specified record was inserted, updated, or deleted. In addition to a timestamp column identified by the field update_time indicating the order in which the changes happened. Each record has a primary key identified by the field customer_id.

In the same batch, multiple changes for the same customer could be received with different update_time. The team wants to store only the most recent information for each customer in the target Delta Lake table.

Which of the following solutions meets these requirements?

  A. Enable Delta Lake's Change Data Feed (CDF) on the target table to automatically merge the received CDC feed
  B. Use MERGE INTO to upsert the most recent entry for each customer_id into the table
  C. Use MERGE INTO with SEQUENCE BY clause on the update_time for ordering how operations should be applied
  D. Use dropDuplicates function to remove duplicates by customer_id, then merge the duplicate records into the table.
  E. Use the option mergeSchema when writing the CDC data into the table to automatically merge the changed data with its most recent schema.

Ans: B.
MERGE INTO command allows you to upsert data from a source table, view, or DataFrame into a target Delta table. Delta Lake supports inserts, updates, and deletes in merge operations.
```
```
15. A data engineer is using a foreachBatch logic to upsert data in a target Delta table.
The function to be called at each new microbatch processing is displayed below with a blank:

  def upsert_data(microBatchDF, batch_id):
      microBatchDF.createOrReplaceTempView("sales_microbatch")
   
      sql_query = """
                  MERGE INTO sales_silver a
                  USING sales_microbatch b
                  ON a.item_id=b.item_id
                      AND a.item_timestamp=b.item_timestamp
                  WHEN NOT MATCHED THEN INSERT *
                  """
      ------------------

Which option correctly fills in the blank to execute the sql query in the function on a cluster with Databricks Runtime below 10.5 ?

  A. spark.sql(sql_query)
  B. batch_id.sql(sql_query)
  C. microBatchDF.sql(sql_query)
  D. microBatchDF.sparkSession.sql(sql_query)
  E. microBatchDF._jdf.sparkSession().sql(sql_query)

Ans: E. 
Usually, we use spark.sq() function to run SQL queries. However, in this particular case, the spark session can not be accessed from within the microbatch process. Instead, we can access the local spark session from the microbatch dataframe.
For clusters with Databricks Runtime version below 10.5, the syntax to access the local spark session is: microBatchDF._jdf.sparkSession().sql(sql_query)
```
```
16. The data engineering team has a singleplex bronze table called ‘orders_raw’ where new orders data is appended every night. They created a new Silver table called ‘orders_cleaned’ in order to provide a more refined view of the orders data.
The team wants to create a batch processing pipeline to process all new records inserted in the orders_raw table and propagate them to the orders_cleaned table.
Which solution minimizes the compute costs to propagate this batch of data?

  A. Use time travel capabilities in Delta Lake to compare the latest version of orders_raw with one version prior, then write the difference to the orders_cleaned table.
  B. Use Spark Structured Streaming to process the new records from orders_raw in batch mode using the trigger availableNow option
  C. Use Spark Structured Streaming's foreachBatch logic to process the new records from orders_raw using trigger(processingTime=”24 hours")
  D. Use batch overwrite logic to reprocess all records in orders_raw and overwrite the orders_cleaned table
  E. Use insert-only merge into the orders_cleaned table using orders_raw data based on a composite key

Ans: B.
Databricks supports trigger(availableNow=True) for Delta Lake and Auto Loader sources. This functionality consumes all available records in an incremental batch.
There is also the trigger(once=True) option for incremental batch processing. However, this setting is now deprecated in the newer Databricks Runtime versions.
NOTE: You may still see this option in the current certification exam version. However, Databricks recommends you use trigger(availableNow=True) for all future incremental batch processing workloads.
```
```
17. The data engineering team has a Silver table called ‘sales_cleaned’ where new sales data is appended in near real-time.
They want to create a new Gold-layer entity against the ‘sales_cleaned’ table to calculate the year-to-date (YTD) of the sales amount. The new entity will have the following schema:
country_code STRING, category STRING, ytd_total_sales FLOAT, updated TIMESTAMP
It’s enough for these metrics to be recalculated once daily. But since they will be queried very frequently by several business teams, the data engineering team wants to cut down the potential costs and latency associated with materializing the results.
Which of the following solutions meets these requirements?

  A. Define the new entity as a view to avoid persisting the results each time the metrics are recalculated
  B. Define the new entity as a global temporary view since it can be shared between notebooks or jobs that share computing resources.
  C. Configuring a nightly batch job to recalculate the metrics and store them as a table overwritten with each update.
  D. Create multiple tables, one per business team so the metrics can be queried quickly and efficiently.
  E. All the above solutions meet the required requirements since Databricks uses the Delta Caching feature

Ans: C.
Data engineers must understand how materializing results is different between views and tables on Databricks, and how to reduce total compute and storage cost associated with each materialization depending on the scenario.
Consider using a view when:
  - Your query is not complex. Because views are computed on demand, the view is re-computed every time the view is queried. So, frequently querying complex queries with joins and subqueries increases compute costs
  - You want to reduce storage costs. Views do not require additional storage resources.
Consider using a gold table when:
  - Multiple downstream queries consume the table, so you want to avoid re-computing complex ad-hoc queries every time.
  - Query results should be computed incrementally from a data source that is continuously or incrementally growing.
```
```
18. A data engineer wants to calculate predictions using a MLFlow model logged in a given “model_url”. They want to register the model as a Spark UDF in order to apply it to a test dataset.
Which code block allows the data engineer to register the MLFlow model as a Spark UDF ?

  A. predict_udf = mlflow.pyfunc.spark_udf(spark, "model_url")
  B. predict_udf = mlflow.spark_udf(spark, "model_url")
  C. predict_udf = mlflow.udf(spark, "model_url")
  D. predict_udf = pyfunc.spark_udf(spark, "model_url")
  E. predict_udf = mlflow.pyfunc(spark, "model_url")

Ans: A.
Mlflow.pyfunc.spark_udf function allows to register a MLFlow model as a Apache Spark UDF. It needs at least 2 parameters:
  spark: A SparkSession object
  model_uri: the location, in URI format, of the MLflow model

Once the Spark UDF created, it can be applied to a dataset to calculate the predictions:
  predict_udf = mlflow.pyfunc.spark_udf(spark, "model_url")
  pred_df = data_df.withColumn("prediction", predict_udf(*column_list))
```
```
19. “A Delta Lake’s functionality that automatically compacts small files during individual writes to a table by performing two complementary operations on the table”
Which of the following is being described in the above statement?

  A. Optimized writes
  B. Auto compaction
  C. Auto Optimize
  D. OPTIMIZE command
  E. REORG TABLE command

Ans: C.
Auto Optimize is a functionality that allows Delta Lake to automatically compact small data files of Delta tables. This can be achieved during individual writes to the Delta table.
Auto optimize consists of 2 complementary operations:
  - Optimized writes: with this feature enabled, Databricks attempts to write out 128 MB files for each table partition.
  - Auto compaction: this will check after an individual write, if files can further be compacted. If yes, it runs an OPTIMIZE job with 128 MB file sizes (instead of the 1 GB file size used in the standard OPTIMIZE)
```
```
20. The data engineering team has a large external Delta table where new changes are merged very frequently. They enabled Optimized writes and Auto Compaction on the table in order to automatically compact small data files to target files of size 128 MB. However, when they look at the table directory, they see that most data files are smaller than 128 MB.
Which of the following likely explains these smaller file sizes ?

  A. Optimized Writes and Auto Compaction have no effect on large Delta tables. The table needs to be partitioned so Auto Compaction can be applied at partition level.
  B. Optimized Writes and Auto Compaction have no effect on external tables. The table needs to be managed in order to store the information of file sizes in the Hive metastore.
  C. Optimized Writes and Auto Compaction automatically generate smaller data files to reduce the duration of future MERGE operations.
  D. Auto compaction supports Auto Z-Ordering which is more expensive than just compaction
  E. The team needs to look at the table’s _auto_optimize directory, where all new compacted files are written.

Ans: C.
Having many small files can help minimize rewrites during some operations like merges and deletes.
For such operations, Databricks can automatically tune the file size of Delta tables. As a result, it can generate data files smaller than the default 128MB.
This helps in reducing the duration of future MERGE operations.
```
```
21. 

```









