Project Idea: Streaming employees informations (Activity + location), apply ETL and finally monitoring dashboards.

NOTE : Don't forget to update the .env and put your own configuration.

## Technology used :

    - Apache Iceberg ( AWS Glue + Athena) with S3 as storage system.
    - Kafka Connect for data ingestion.
    - Spark (EMR) for pipelines.
    - OpenSearch for logs.
	- Kibana for visualization.
	- AWS Lambda for scripting crone jobs


## High-Level Diagram

![High-Level Diagram](docs/diagrams/EmployeesTracker.drawio.png?raw=true "High-Level")

### Credits : 

Apache Kafka & Kafka connect Installation : https://www.youtube.com/watch?v=_RdMCc4HGPY

## TODO Stream via AWS Glue streaming later or EMR instead of KAFKA Connect (Limitation of Partitioning ect..)

#### Setup (KAFKA)

docker-compose up -d

Connect into the docker image running zookeeper and run this command : 

kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic employees
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic employees_activity

#### Create Kafka connector : 

## Flush size we'll make it 100 for now, maybe change it later, we don't need to be very precise for this project.

curl -i -X PUT -H "Accept:application/json" \
	-H "Content-Type:application/json" http://localhost:8083/connectors/employees-s3-conn/config \
	-d '
 {
	"connector.class": "io.confluent.connect.s3.S3SinkConnector",
	"key.converter": "org.apache.kafka.connect.storage.StringConverter",
	"tasks.max": "1",
	"topics": "employees",
	"s3.region": "eu-central-1",
	"s3.bucket.name": "iceberg-track",
	"flush.size": "100",
	"storage.class": "io.confluent.connect.s3.storage.S3Storage",
	"format.class": "io.confluent.connect.s3.format.parquet.ParquetFormat",
	"schema.generator.class": "io.confluent.connect.storage.hive.schema.DefaultSchemaGenerator",
	"schema.compatibility": "NONE",
	"partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
	
	"partition.duration.ms": "86400000",
		"path.format": "'yyyy/MM/dd'",
	"locale": "en",
	"timezone": "UTC"
  }'


curl -i -X PUT -H "Accept:application/json" \
	-H "Content-Type:application/json" http://localhost:8083/connectors/employees_activity-s3-conn/config \
	-d '
 {
	"connector.class": "io.confluent.connect.s3.S3SinkConnector",
	"key.converter": "org.apache.kafka.connect.storage.StringConverter",
	"tasks.max": "1",
	"topics": "employees_activity",
	"s3.region": "eu-central-1",
	"s3.bucket.name": "iceberg-track",
	"flush.size": "100",
	"storage.class": "io.confluent.connect.s3.storage.S3Storage",
	"format.class": "io.confluent.connect.s3.format.parquet.ParquetFormat",
	"schema.generator.class": "io.confluent.connect.storage.hive.schema.DefaultSchemaGenerator",
	"schema.compatibility": "NONE",
	"partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
	
	"partition.duration.ms": "86400000",
		"path.format": "'yyyy'",
	"locale": "en",
	"timezone": "UTC"
  }'

## To Run Spark analyzer Job : 
spark-submit --jars tools/opensearch-spark-30_2.12-1.0.0.jar analyzer.py

## Conclusion : 

The choice of technology was very good for this project, I really enjoyed learning this, however I have found some limitation using AWS Athena with iceberg like not being able to use the table property "sorted_by" to optimize more my IO and file sizes, however I was able to play around with the partitionning and compressions and file types and used the beautiful Iceberg's statistics to monitor the changes, this helps me undestand the importance of storage configuration and how they can optimize the cost and performance.