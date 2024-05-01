# First level import

# Second level import 
from DataGenerator.Employee import Employee, Department
from DatabaseHandler import AthenaHandler



__version__ = "0.0.1"


def main():
    """
    Main function to generate employees and departments
    """
    print(f"Welcome to the Employees Tracker Simulator! \n you're running version : {__version__} \n")
    
    # First we'll need to load available department from database :
    athena_handler = AthenaHandler()
    athena_handler.connect()
    
    query = "SELECT * FROM departments"
    departments = athena_handler.fetch(query)

if __name__ == "__main__":
    main()