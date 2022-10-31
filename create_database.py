from src.models import  Admin, Course, Vacancy,Enquiry,Instructor
from src.database import Base,engine
Base.metadata.create_all(engine)
