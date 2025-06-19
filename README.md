
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
 
- Photon accelerates modern Apache Spark workloads, reducing your total cost per workload.

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








