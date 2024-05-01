# First level import
import random 

# Second level import 
from DataGenerator.Employee import Employee, Department
from DatabaseHandler import AthenaHandler



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
        
        for i in range(int(num_employees)):
            # Pick a random department : 
            random_department = random.randint(0, df_departments.shape[0]- 1)
            department = Department(name = df_departments.iloc[random_department]['name'], id = df_departments.iloc[random_department]['id'], description=df_departments.iloc[random_department]['description'])
            
            # Create our employee :
            employee = Employee(i, department)
            
            employee.create()
        
    # Now we'll need to load available employees from database, then we'll simulate random activities for them :
    query = 'SELECT * FROM "employees_activity"."employees" '
    df_employees = athena_handler.fetch(query)
    
    print(df_employees.head())
    
    
if __name__ == "__main__":
    main()