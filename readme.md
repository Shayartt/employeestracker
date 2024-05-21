Project Idea: Streaming employees informations (Activity + location), apply ETL and finally monitoring dashboards.

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

#### Create Kafka connector : 

## Flush size we'll make it 100 for now, maybe change it later, we don't need to be very precise for this project.

curl -i -X PUT -H "Accept:application/json" \
    -H  "Content-Type:application/json" http://localhost:8083/connectors/employees-s3-conn/config \
    -d '
 {
		"connector.class": "io.confluent.connect.s3.S3SinkConnector",
		"key.converter":"org.apache.kafka.connect.storage.StringConverter",
		"tasks.max": "2",
		"topics": "employees",
		"s3.region": "eu-central-1",
		"s3.bucket.name": "iceberg-track",
		"flush.size": "1",
		"storage.class": "io.confluent.connect.s3.storage.S3Storage",
		"format.class": "io.confluent.connect.s3.format.parquet.ParquetFormat",
		"schema.generator.class": "io.confluent.connect.storage.hive.schema.DefaultSchemaGenerator",
		"schema.compatibility": "NONE",
        "partitioner.class": "com.example.connect.s3.CustomPartitioner"
	}
'