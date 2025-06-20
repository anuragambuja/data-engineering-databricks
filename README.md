
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
  - JSON file contains commit information:
    - Operation performed + Predicates used
    - data files affected (added/removed)
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










