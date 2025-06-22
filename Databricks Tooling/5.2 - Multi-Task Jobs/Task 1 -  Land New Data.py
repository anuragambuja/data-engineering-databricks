# Databricks notebook source
# MAGIC %run ../../Includes/Copy-Datasets-2

# COMMAND ----------

spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", True)
spark.conf.set("spark.databricks.delta.autoCompact.enabled", True)

# COMMAND ----------

dbutils.widgets.text("number_of_files", "1") # this be enabled through the UI by setting 'parameters' key-value pair.
num_files = int(dbutils.widgets.get("number_of_files"))

# COMMAND ----------

bookstore.load_new_data(num_files)

# COMMAND ----------


