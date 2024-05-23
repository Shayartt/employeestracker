try : 
    import unzip_requirements
except ImportError:
    pass

from datetime import datetime
import json
from pyathena import connect as athena_connect

def update_data_lake(event,context):
    # This should be a hourly crone job to update the data lake with new data.
    
    where_query = " where created_at >= date_add('hour', -1, CURRENT_TIMESTAMP);"

    pyathena_client = athena_connect(region_name = "eu-central-1", s3_staging_dir = "s3://iceberg-track/result_queries/")

    # If first time you'll need to create the table, do the same for other tables.
    # query_first_time = "CREATE TABLE IF NOT EXISTS employees_activity.iceberg_employees WITH (table_type = 'ICEBERG', format='parquet', location='s3://iceberg-track/topics/data_lake/employees', is_external=false) AS SELECT id,full_name,employee_position,contact_info,department_id,CAST(created_at AS TIMESTAMP(6)) AS created_at FROM employees_activity.employees3 " + str(where_query)
    # with pyathena_client.cursor() as cursor:
    #     cursor.execute(query_first_time)
        
    query_update_employees_hourly = "insert into employees_activity.iceberg_employees  SELECT id,full_name,employee_position,contact_info,department_id,CAST(created_at AS TIMESTAMP(6)) AS created_at FROM employees_activity.employees3 " + str(where_query)
    with pyathena_client.cursor() as cursor:
        cursor.execute(query_update_employees_hourly)
        
    where_query = " where start_date >= date_add('hour', -1, CURRENT_TIMESTAMP);"
    
    query_update_activity_logs_hourly = "insert into employees_activity.iceberg_activity_logs  SELECT id,employees_id,action,location,CAST(start_date AS TIMESTAMP(6)) AS start_date,CAST(end_date AS TIMESTAMP(6)) AS end_date FROM employees_activity.activity_logs " + str(where_query)
    with pyathena_client.cursor() as cursor:
        cursor.execute(query_update_activity_logs_hourly)
    
    # Add adittional updates queries here.
    
    # Return success :
    body = {
        "Status":"Data updated.",
    }  
    return {"statusCode": 200, "body": json.dumps(body)}