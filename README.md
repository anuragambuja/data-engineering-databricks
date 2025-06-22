
# databricks
- Multi-cloud Lakehouse Platform based on Apache Spark
- In-memory, distributed data processing
- All languages support: Scala, Python, SQL, R, & Java
- Batch processing & stream processing
- Structured, semi structured, & unstructured data
- Databricks File System (DBFS)
  - Distributed file system
  - Preinstalled in Databricks clusters
  - Abstraction layer: data persisted to the underlaying cloud storage
- Databases = Schemas in Hive metastore
- Photon accelerates modern Apache Spark workloads, reducing your total cost per workload.

- Tables
- Manged tables
  - Created under the database directory
  - Dropping the table, delete the underlying data files
  - `CREATE TABLE table_name`
- External tables
  - Created outside the database directory
  - Dropping the table, will Not delete the underlying data files
  - ` CREATE TABLE table_name LOCATION 'path'`



> ## Delta Lake
- Open-source storage framework and used for building Lakehouse (and not Data warehouse)
- Transaction log (Delta log)
  - Ordered records of every transaction performed on the table
  - Single Source of Truth
  - Spark needs to process many tiny, inefficient JSON files in order to the resolve the current table state. So, Databricks automatically creates Parquet checkpoint files every 10 commits to accelerate the resolution of the current table state. Then, Spark only has to perform incremental processing of newly added JSON files.

    ![image](https://github.com/user-attachments/assets/7b16990d-cd6c-4fdc-9a06-aef6639c2937)

  - Running the VACUUM does not delete Delta log files. Log files are automatically cleaned up by Databricks. Each time a checkpoint is written, Databricks automatically cleans up log entries older than the log retention interval (default: 30 days)
    - By default, you can time travel to a Delta table only up to 30 days old. `delta.logRetentionDuration` controls how long the history for a table is kept
  - JSON file contains commit information:
    - Operation performed + Predicates used
    - data files affected (added/removed)
  - Delta Lake captures statistics in the transaction log for each added data file. 
    - Statistics indicate per file:
      1. Total number of records: Statistics on the first 32 columns of the table. Nested fields count when determining the first 32 columns Example: 4 struct fields with 8 nested fields will total to the 32 columns.
      2. Minimum value in each column
      3. Maximum value in each column
      4. Null value counts for each of the columns
    - Statistics will always be leveraged for file skipping.
    - Statistics are uninformative for string fields with very high cardinality. Example: free text fields. Move them outside the first 32 columns

- Delta Lake Advantages
  - Brings ACID transactions to object storage
  - Handle scalable metadata
  - Full audit trail of all changes
  - Builds upon standard data formats: Parquet + Json

- Time travel
  - Query older versions of the data
  - Audit data changes: DESCRIBE HISTORY command
  ```
  # Using a timestamp
  SELECT * FROM my_table TIMESTAMP AS OF "2019-01-01"
  
  # Using a version number
  SELECT * FROM my_table VERSION AS OF 36
  SELECT * FROM my_table@v36

  # Rollback Versions: RESTORE TABLE command:
  RESTORE TABLE my_table TO TIMESTAMP AS OF "2019-01-01”
  RESTORE TABLE my_table TO VERSION AS OF 36
  ```
- Compaction
  - Compacting Small Files
  - OPTIMIZE my_table

- Indexing
  - Co-locate column information
  - OPTIMIZE my_table ZORDER BY column_name

- Vacuum a Delta table
  - Cleaning up unused data files
    - uncommitted files
    - files that are no longer in in latest table state
    - Default retention period: 7 days
  - VACUUM table_name [retention period]
    - Vacuum = no time travel



- In Databricks, Databases = Schemas in Hive metastore (repository of metadata of Databases, Tables etc.)
- The `default` database stores files in `dbfs:/user/hive/warehouse` . 

- View
  - Logical query against source tables
  - Types of views
    1. (Stored) Views
      - Persisted in DB
      - Dropped only by DROP VIEW
      - `CREATE VIEW view_name AS query`
    2. Temporary views
      - Session-scoped view. It is tied to Spark session.
        - when a spark session is created:
          - 
      - dropped when session ends
      - `CREATE TEMP VIEW view_name AS query`
    3. Global Temporary views
      - Cluster-scoped view
      - dropped when cluster restarted
      - Not listed in `SHOW TABLES` command. Instead use `SHOW TABLES IN global_temp;`
      - `CREATE GLOBAL TEMP VIEW view_name AS query;`
      - `SELECT * FROM global_temp.view_name`

- CTAS (CREATE TABLE _ AS SELECT statement)
  - Automatically infer schema information from query results
    - do not support manual schema declaration
  ```
  CREATE TABLE new_table
  COMMENT "Contains PII”
  PARTITIONED BY (city, birth_date)
  LOCATION ‘/some/path’
  AS SELECT id, name, email, birth_date, city FROM users

  ```


> ## Querying Files
`SELECT * FROM file_format.`/path/to/file`/`
- file_format: Can be Self-describing formats like json, parquet or non self-describing like CSV, TSV
- path to file can be single file, regexx expression or directory.
- Extract text files as raw strings
  - Text-based files (JSON, CSV, TSV, and TXT formats)
  - `SELECT * FROM text.`/path/to/file``
- Extract files as raw bytes
  - Images or unstructured data
  - `SELECT * FROM binaryFile.`/path/to/file``
- CTAS (create table as)
  - Do Not support manual schema declaration.
  - Useful for external data ingestion with well-defined schema
  - Do Not support file options
  ```
  CREATE TABLE table_name
  AS SELECT * FROM file_format.`/path/to/file`;

  # External Non-Delta table
  CREATE TABLE table_name
  (col_name1 col_type1, ...)
  USING data_source  # CSV, TSV, JDBC
  OPTIONS (header = "true", delimiter = ”;", ...)
  <!-- OPTIONS (url = "jdbc:sqlite://hostname:port", dbtable = "database.table", user = "username", password = ”pwd” ) -->
  LOCATION = path;
  ```
  - Since external tables are non delta table, we can create a temporary view and then create a delta table from it. 


> ## Table Constraints
- NOT NULL constraints
- CHECK constraints
```
ALTER TABLE table_name ADD CONSTRAINT constraint_name constraint_details
ALTER TABLE orders ADD CONSTRAINT valid_date CHECK (date > '2020-01-01');
```

> ## Cloning Delta Lake Tables
- Useful to set up tables for testing in development.
- Types: In either case, data modifications will not affect the source
  - DEEP CLONE
    - Fully copies data + metadata from a source table to a target
    - CREATE TABLE table_clone DEEP CLONE source_table;
    - Can sync changes 

  - SHALLOW CLONE
    - Just copy the Delta transaction logs
    - CREATE TABLE table_clone SHALLOW CLONE source_table;

> ## Data Stream
- Any data source that grows over time
  - New files landing in cloud storage
  - Updates to a database captured in a CDC feed
  - Events queued in a pub/sub messaging feed
- Unsupported Operations: Sorting, Deduplication
- Spark Streaming guarantees:
  - Fault Tolerance
    - Checkpointing + Write-ahead logs
      - record the offset range of data being processed during each trigger interval.
  - Exactly-once guarantee
      - Idempotent sinks

- Trigger Intervals

    ![image](https://github.com/user-attachments/assets/a51a08d2-5192-4ca5-ac93-778db569ecf0)

- Output Modes 

    ![image](https://github.com/user-attachments/assets/4857d2ed-ad46-4cc3-a7df-a26411e24917)

- Checkpointing
  - Store stream state. Used to track the progress of your stream processing
  - Can Not be shared between separate streams

```
streamDF = spark.readStream
  .table("Input_Table")

streamDF.writeStream
  .trigger(processingTime="2 minutes")
  .outputMode("append")
  .option("checkpointLocation", "/path")
  .table("Output_Table")

```

- Incremental Data Ingestion
  - Loading new data files encountered since the last ingestion. 
  - Two Mechnisms:
    - COPY INTO
      - SQL command
      - Idempotently and incrementally load new data files: Files that have already been loaded are skipped.
      - Thousands of files. Less efficient at scale
      ```
      COPY INTO my_table
      FROM '/path/to/files’
      FILEFORMAT = CSV -- JSON
      FORMAT_OPTIONS ('delimiter' = '|’, 'header' = 'true', ...)
      COPY_OPTIONS ('mergeSchema' = 'true’);
      ```
    - Auto loader
      - Structured Streaming. Support near real-time ingestion of millions of files per hour.
      - Can process billions of files.
      - Store metadata of the discovered files
      - Exactly-once guarantees. Fault tolerance
      ```
      spark.readStream
          .format("cloudFiles")
          .option("cloudFiles.format", <source_format>)
          .option("cloudFiles.schemaLocation", <schema_directory>)
          .load('/path/to/files’)
        .writeStream
          .option("checkpointLocation", <checkpoint_directory>)
          .option("mergeSchema", “true”)
          .table(<table_name>)
      ```
> ## Multi-Hop Architecture
- Medallion Architecture
- Organize data in multi-layered approach

  ![image](https://github.com/user-attachments/assets/f4faef87-20b4-47f0-9cf2-bc3ee6492dcc)

- Bronze Ingestion Patterns
  - Singleplex: One-to-One mapping

      ![image](https://github.com/user-attachments/assets/0b19b42f-8964-4f77-9347-be655a427e9e)

  - Multiplex: Many-to-One mapping

      ![image](https://github.com/user-attachments/assets/045bc758-47b2-413a-941c-f9a5aac5b017)

    - Promoting to Silver layer

        ![image](https://github.com/user-attachments/assets/1090cf23-7ba0-483c-9ca0-d623e73f6b88)


> ## Deleta Live Tables
- Data pipelines
- Change Data Capture
  - Process of identifying changes (Insert, Update, Delete) made to data in the source and delivering those changes to the target.
  - Processing CDC feed using MERGE
    ```
    MERGE INTO target_table t
    USING source_updates s
    ON t.key_field = s.key_field
    WHEN MATCHED AND t.sequence_field < s.sequence_field
    THEN UPDATE SET *
    WHEN MATCHED AND s.operation_field = "DELETE"
    THEN DELETE
    WHEN NOT MATCHED
    THEN INSERT *
    ```
    - Merge can not be performed if multiple source rows matched and attempted to modify the same target row in the Delta table. Use `rank().over(Window)` to fix the issue. 
  - APPLY CHANGES INTO Statement for Delta Live Tables
    - Orders late-arriving records using the sequencing key
    - Default assumption is that rows will contain inserts and updates
    - Can optionally apply deletes (APPLY AS DELETE WHEN condition)
    - Specify one or many fields as the primary key for a table
    - Specify columns to ignore with the EXCEPT keyword
    - Support applying changes as SCD Type 1 (default) or SCD Type 2
    - Breaks the append-only requirements for streaming table sources. So, Cannot perform streaming queries against the table
    ```
    APPLY CHANGES INTO LIVE.target_table
    FROM STREAM(LIVE.cdc_feed_table)
    KEYS (key_field)
    APPLY AS DELETE WHEN operation_field = "DELETE"
    SEQUENCE BY sequence_field
    COLUMNS *;
    ```
  - Delta Lake Change Data Feed (CDF)
    - Automatically generate CDC feeds about Delta Lake tables.
    - Records row-level changes for all data written into a Delta table i.e. Row data + metadata (whether row was inserted, deleted, or updated)
    - Change Type:
      - The update_preimage offers a snapshot of the row before any updates.
      - The update_postimage provides its state after the changes.
    - Querying the change data
      ```
      SELECT *
      FROM table_changes('table_name’, start_version, [end_version]);

      SELECT *
      FROM table_changes('table_name’, start_timestamp, [end_timestamp]);
      ```
    - Enabling CDF
      - New tables: `CREATE TABLE myTable (id INT, name STRING) TBLPROPERTIES (delta.enableChangeDataFeed = true);`
      - Existing table: `ALTER TABLE myTable SET TBLPROPERTIES (delta.enableChangeDataFeed = true);`
      - All new tables: `spark.databricks.delta.properties.defaults.enableChangeDataFeed`
    - When running VACUUM, CDF data is also deleted.
    - Use CDF when:
      - Table’s changes include updates and/or deletes
      - Small franction of records updated in each batch (from CDC feed)
    - Don’t use CDF when:
      - Table’s changes are appendonly
      - Most records in the table updated in each batch


> ## Data Governance
- Programmatically grant, deny, and revoke access to data objects
- Operations include: GRANT, DENY, REVOKE, SHOW GRANTS
- GRANT `Privilege` ON `Object` object-name TO userOrGroup

  ![image](https://github.com/user-attachments/assets/342f50f6-c886-41a2-bd6c-2b43c65eb8bd)

  ![image](https://github.com/user-attachments/assets/079e5857-cf99-4ebf-9fe6-6926339746f2)

- Unity Catalog
  - Centralized governance solution across all your workspaces on any cloud.
  - Unify governance for all data and AI assets
    - files, tables, machine learning models and dashboards
    - based on SQL
    - Follows 3-level namespace i.e. `SELECT * FROM catalog.schema.table `
  - Identities
    - Users: identified by e-mail addresses
      - Account administrator
    - Service Principles: identified by Application IDs
      - Service Principles with administrative privilege
    - Groups: grouping Users and Service Principles
      - Nested groups
  - Built-in data search and discovery
  - Automated lineage
  - No hard migration required from Catalog to Unity Catalog
  - Architecture

      ![image](https://github.com/user-attachments/assets/48412111-aa8f-4c5e-acf4-1e09cd52b697)

  - Hierarchy

      ![image](https://github.com/user-attachments/assets/406ef24b-907f-48e1-8835-4884afb624cb)



> Slowly Changing Dimensions
- Data management concept that determines how tables handle data which change over time
- SCD Types:
  - Type 0: No changes allowed. Static/Append only
  - Type 1: Overwrite. No history retained (use Delta Time Travel if needed but vacuum can delete the history)
  - Type 2: Add new row for each change and mark the old as obsolete. Retains the full history of values.


> ## Partitioning Delta Lake Tables
- A partition is a subset of rows that share the same value for predefined partitioning columns
```
CREATE TABLE my_table (id INT, name STRING, year INT, month INT)
PARTITIONED BY (year, month);

DELETE FROM my_table
Where year < 2023;
```
- Choosing partition columns
- Low cardinality fields should be used for partitioning
- Partitions should be at least 1 GB in size. If most partitions < 1GB of data, the table is over-partitioned.
- In case records with a given value will continue to arrive indefinitely, use Datetime fields as partition column
- Files cannot be combined or compacted across partition boundaries. So, Partitioned small tables increase storage costs and total number of files to scan.
```
spark.readStream
  .option("ignoreDeletes", True)  # Keeps table streamable on partition deletes
  .table("my_table")
```
- Use `vacuum` to delete at partition boundaries. 

> ## Stream vs. Static tables
- Streaming tables are ever-appending data sources
- Static tables contain data that may be changed or overwritten. It breaks the requirement of an ever-appending source for Structured Streaming.
- Streaming drives the join. 
  - Change in static table does not trigger the stream processing. 
  - Unmatched records in the Stream will not be pushed to output table. 
- Stream-static joins are not stateful. So even if the unmatched key arrives in static table later, the streaming mismatched record is not processed. e.g. In below snapshot, the late arrival of `course id = C03` does not lead to processing of the data in stream. 

    ![image](https://github.com/user-attachments/assets/7f26e62c-3056-4c6a-b86b-5cc8da3443e9)







