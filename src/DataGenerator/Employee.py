# First level imports
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import random
from faker import Faker

# Second level import
from .Department import Department, possible_location_activities

@dataclass
class Employee:
    """
    This class represents an employee in the company
    """
    id: int
    department: Department
    
    def __post_init__(self):
        """
        We'll generate random name and job title after creating our employee.
        """
        # Create a Faker instance
        fake = Faker()

        # Generate a random full name
        self.full_name = fake.name()
        self.phone_number = fake.phone_number()
        self.created_at = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
        # Generate random job title
        self.position = self.department.get_random_job_title()
        
    def __str__(self) -> str:
        """
        Return the string representation of the employee
        """
        return f"Employee: {self.full_name} - {self.position} in {self.department.name} department"
  
@dataclass
class EmployeesActivity:
    """
    This class represents an employee activity in the company
    
    """
    id : int 
    employees_id : int
    action : str 
    location : str
    random_date : bool = False
    
    def __post_init__(self):
        """
        Prepare start / end date in a timestamp format
        """
        if not self.random_date:
            self.start_date = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
        else:
            # Generate random date in the previous 10 days : 
            self.start_date = datetime.now(tz=timezone.utc) - timedelta(days=random.randint(1, 10))
            self.start_date = int(self.start_date.timestamp() * 1000)
    
        
        # Add random from 1 to 60 minutes : 
        self.end_date = self.start_date + (60 * 1000 * random.randint(1, 60))

    
    def __str__(self) -> str:
        """
        Return the string representation of the employee activity
        """
        return f"Employee: {self.employees_id} is {self.action} in {self.location}"
  

def activity_to_dict(employee: EmployeesActivity, _) -> dict: # Had to make it outside the class because of the uses in our Kafka producer
        """
        Returns a dict representation of a Employee instance for serialization.
        """
        return dict(id=employee.id,
                    employees_id=employee.employees_id,
                    action=employee.action,
                    location=employee.location,
                    start_date = employee.start_date,
                    end_date = employee.end_date
                    )   
 
def to_dict(employee: Employee, _) -> dict: # Had to make it outside the class because of the uses in our Kafka producer
        """
        Returns a dict representation of a Employee instance for serialization.
        """
        return dict(full_name=employee.full_name,
                    id=employee.id,
                    department_id=employee.department.id,
                    employee_position=employee.position,
                    contact_info = employee.phone_number,
                    created_at = employee.created_at
                    )
        
        
        