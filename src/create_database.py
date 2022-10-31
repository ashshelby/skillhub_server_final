from models import  Admin, Course, Vacancy,Enquiry,Instructor
from database import Base,engine
Base.metadata.create_all(engine)