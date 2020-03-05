# Mason - Data Operator Framework ![Mason Logo](images/MasonLogo.png) 

Mason is the connecting tissue for your data projects.   It provides a "data aware" analogue to the concept of an airflow operator.   In reality it specifies operators which interact with 4 configuration abstractions:

1.   Storage Engine - for example S3, HDFS or Kafka
2.   Metadata Store - Hive, Glue, Iceberg
3.   Execution Engines -  Spark, Dask, Presto, Athena 
4.   Schedulers - Glue, Apache Airflow, DigDag

![Operator Configs](images/OperatorConfigs.png)

Mason is heavily inspired by language agnostic configuration driven tools like kubernetes, helm, and terraform.   Mason aims to help to make existing higher level open source big data tools _easier_ to coordinate with one another and make them easier to interact with for individuals of various expertise across organizations.  Mason does not attempt to make provisioning and standing up such services referenced in its configurations easier and thus is meant to be used in conjunction with tools
like kubernetes and helm.

Mason's mission is to provide ways to build composable self contained functional units called "Data Operators" which companies can stitch together to easily provide end to end data pipelines.   The target demographic of Mason are companies that are just breaking into the enterprise data space, or companies that are looking to consolidate their data operations.

## Quickstart
Local Development:
```
./install
```
Mason leverages `mypy` heavily for ensuring that function signatures and types are in line. Install will run mypy and stop if it does not succeed.  

To configure mason run `mason config`.  Configurations are validated for basic structure using json_schema.  See `configurations/schema.json`:
```
mason config examples/config/config_example.yaml
>>
Creating MASON_HOME at ~/.mason/
Creating OPERATOR_HOME at ~/.mason/operators/

Using config examples/config/config_example.yaml.  Saving to ~/.mason/config.yaml
+-------------------------------------------------+
| Reading configuration at ~/.mason/config.yaml:  |
+-------------------------------------------------+
{
 "metastore_config": "{'client': 'glue', 'configuration': {'region': 'us-east-1', 'aws_role_arn': 'arn:aws:iam::062325279035:role/service-role/AWSGlueServiceRole-anduin-data-glue'}}",
 "storage_config": "{'client': 's3', 'configuration': {'region': 'us-east-1'}}",
 "scheduler_config": "{'client': 'glue', 'configuration': {'region': 'us-east-1', 'aws_role_arn': 'arn:aws:iam::062325279035:role/service-role/AWSGlueServiceRole-anduin-data-glue'}}",
 "execution_config": "{}"
}
```

You will begin without any operators registered by default:
```
mason operator
>>
No Operators Registered.  Register operators by running "mason register"

```
  You can register some example operators.  Operators are validated for basic structure using json_schema.  See `/operators/schema.json` for the schema description.
```
mason register examples/operators/table
>>
Registering operator at examples/operators/table to ~/.mason/operators/table/
```
Listing Operators:
```
mason operator
>>
+--------------------------------------------------+
| Available Operator Methods: ~/.mason/operators/  |
+--------------------------------------------------+

namespace    command    description                                                                               parameters
-----------  ---------  ----------------------------------------------------------------------------------------  ----------------------------------------------------------------
table        refresh    Refresh metastore tables                                                                  {'required': ['database_name', 'table_name']}
table        get        Get metastore table contents                                                              {'required': ['database_name', 'table_name']}
table        list       Get metastore tables                                                                      {'required': ['database_name']}
table        infer      Registers a schedule for infering the table then does a one time trigger of the refresh.  {'required': ['database_name', 'storage_path', 'schedule_name']}

```
Listing Operators for a particular namespace:
```
mason operator table
```

Running operator with parameters argument:
```
mason operator table get -p database_name:crawler-poc,table_name:catalog_poc_data
>>
+--------------------+
| Parsed Parameters  |
+--------------------+
{'database_name': 'crawler-poc', 'table_name': 'catalog_poc_data'}

+-------------------------+
| Parameters Validation:  |
+-------------------------+
Validated: ['database_name', 'table_name']

+--------------------+
| Operator Response  |
+--------------------+
{
 "Errors": [],
 "Info": [],
 "Warnings": [],
 "Data": {
  "name": "catalog_poc_data",
  "created_at": "2020-02-26T12:57:31-05:00",
  "created_by": "arn:aws:sts::062325279035:assumed-role/AWSGlueServiceRole-anduin-data-glue/AWS-Crawler",
  "database_name": "crawler-poc",
  "schema": [...]
 }
}

```
Running operator with config parameters yaml file:

```
mason operator table get -c examples/parameters/table_get.yaml
>>
+--------------------+
| Operator Response  |
+--------------------+
{
 "Errors": [],
 "Info": [],
 "Warnings": [],
 "Data": {
  "name": "catalog_poc_data",
  "created_at": "2020-02-26T12:57:31-05:00",
  "created_by": "arn:aws:sts::062325279035:assumed-role/AWSGlueServiceRole-anduin-data-glue/AWS-Crawler",
  "database_name": "crawler-poc",
  "schema": [...]
 }
}
```


## Data Operators 

### Philosophy

The main concept in mason is something called a "Data Operator".  There are three main types of Data Operators:

1.  Ingress Operators
2.  Transform Operators
3.  Egress Operators

![Data Operators](images/DataOperators.png)

### Defining Data Operators:
COMING SOON


### Example: Import Operator

![Ingress Operator](images/IngressOperator.png)

### Example: Dedupe Operator

![Dedupe Operator](images/DedupeOperator.png)

### Example: Summarize Operator

![Summarize Operators](images/SummarizeOperator.png)

### Example: Export Operator

![Export Operators](images/ExportOperator.png)