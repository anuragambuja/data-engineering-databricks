
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

- 



