# First level imports
from dataclasses import dataclass
import random 

# Second level imports
from .enums import possible_jobs


@dataclass
class Department:
    """
    This class represents a department in the company, after init will generate list of possible job titles
    """
    id: int
    name: str
    description: str
    
    def __post_init__(self):
        """
        We'll prepare the list to be consumed via main function
        """
        self.job_titles = self.generate_job_titles()
        
    def generate_job_titles(self):
        """
        Generate list of possible job titles for the department
        """
        return possible_jobs[self.name].value
    
    def get_random_job_title(self):
        """
        Get random job title from the list
        """
        return random.choice(self.job_titles)
    
    def __str__(self):
        return f"Department: {self.name} - {self.description}"