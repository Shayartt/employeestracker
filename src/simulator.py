# First level import
import random 

# Second level import 
from DataGenerator.Employee import Employee, Department, to_dict as employee_to_dict
from DatabaseHandler import AthenaHandler
from KafkaHandler.producer import KafkaProducer



__version__ = "0.0.1"


def main():
    """
    Main function to generate employees and departments
    """
    print(f"Welcome to the Employees Tracker Simulator! \n you're running version : {__version__} \n")
    
    # Init database handler:
    athena_handler = AthenaHandler()
    athena_handler.connect()
    
    # First we'll need to load available department from database:
    query = 'SELECT * FROM "employees_activity"."department" '
    df_departments = athena_handler.fetch(query)
    
    # Ask the user if he wants to create employees:
    is_create_employees = input("Do you want to create employees? (y/n) : ")
    
    if is_create_employees.lower() == 'y': #  In case we want to create new employees
        
        num_employees = input("Enter the number of employees to generate: ")
        list_employees = []
        
        for i in range(int(num_employees)):
            # Pick a random department : 
            random_department = random.randint(0, df_departments.shape[0]- 1)
            department = Department(name = df_departments.iloc[random_department]['name'], id = df_departments.iloc[random_department]['id'], description=df_departments.iloc[random_department]['description'])
            
            # Create our employee :
            employee = Employee(i, department)
            
            list_employees.append(employee)
            
        # Prepare Kafka Producer to publish employees to Kafka topic:
        my_kafka_producer = KafkaProducer(topic = "employees", schema = "src/KafkaHandler/schema/employee.avsc", serializer_function = employee_to_dict)
        
        # Send list of employees to our topic : 
        # TODO very weird bug run with debuger and stop line at next line, then run it normally
        my_kafka_producer.produce(list_employees)
            
        print("Employees have been successfully created and sent to Kafka topic!")
        
    # # Now we'll need to load available employees from database, then we'll simulate random activities for them :
    query = 'SELECT * FROM "employees_activity"."employees3" '
    df_employees = athena_handler.fetch(query)
    
    print(df_employees.head())
    
    
if __name__ == "__main__":
    main()