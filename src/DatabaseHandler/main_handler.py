from abc import ABC, abstractmethod

class DatabaseHandler(ABC):
    """
    This class represents a database handler, it's an abstract class
    """
    @abstractmethod
    def connect(self):
        """
        Connect to the database
        """
        pass
    
    @abstractmethod
    def insert(self, data: dict) -> bool:
        """
        Insert data to the database
        """
        pass
    
    @abstractmethod
    def fetch(self, query: str) -> dict:
        """
        Fetch data from the database
        """
        pass
    
    @abstractmethod
    def close(self):
        """
        Close the connection
        """
        pass