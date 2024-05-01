# First level imports
from dataclasses import dataclass
from faker import Faker

# Second level import
from .Department import Department

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
        
        # Generate random job title
        self.position = self.department.get_random_job_title()
        
    def __str__(self) -> str:
        """
        Return the string representation of the employee
        """
        return f"Employee: {self.full_name} - {self.position} in {self.department.name} department"