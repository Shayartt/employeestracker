from enum import Enum

class possible_jobs(Enum):
    IT = ["Software Developer", "QA Engineer", "DevOps Engineer", "Data Analyst", "Database Administrator"]
    ADMINISTRATION = ["HR Manager", "Office Manager", "Receptionist", "Accountant", "Secretary"]
    SALES = ["Sales Manager", "Sales Representative", "Sales Assistant", "Sales Analyst", "Sales Consultant"]
    MARKETING = ["Marketing Manager", "Marketing Specialist", "Marketing Assistant", "Marketing Analyst", "Marketing Consultant"]
    FINANCE = ["Financial Manager", "Financial Analyst", "Financial Advisor", "Financial Consultant", "Financial Specialist"]
    
class possible_location_activities(Enum):
    KITCHEN = ["Cooking", "Cleaning", "Dishwashing", "Eating"]
    OFFICE = ["Coding", "Testing", "Debugging", "Meeting"]
    MEETING_ROOM = ["Meeting", "Presenting", "Discussing", "Brainstorming"]
    PARKING = ["Parking", "Leaving", "Arriving", "Waiting"]
    PLAYING_ROOM = ["Playing", "Gaming", "Watching", "Listening"]