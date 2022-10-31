from enum import unique
from pydantic.schema import schema
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine, Boolean,Text
from sqlalchemy.orm import  sessionmaker, relationship,backref
import src.database as db
import passlib.hash as _hash
import datetime as dt
from sqlalchemy_utils.types import URLType,EmailType
import pytz
NEPAL_TIMEZONE = pytz.timezone("Asia/Kathmandu")

class User(db.Base):
    __tablename__ = 'user'
    id = Column(Integer(),primary_key=True,index=True)
    pick_id = Column(String(50),unique=True,nullable=False,index=True)
    full_name = Column(String(300),unique=False,index=True,nullable=False)
    email = Column(EmailType,index=True,nullable=False,unique=True)
    phone_number = Column(String(10),index=True,nullable=False)
    enquired = relationship("Enquiry",back_populates="user",single_parent=True,cascade="all, delete-orphan")

    def verify_password(self,password_to_check:str):
        return _hash.bcrypt.verify(password_to_check,self.password_hashed)

    def config(self):
        orm_mode = True





class Admin(db.Base):
    __tablename__ = 'admin'
    id = Column(Integer(), primary_key=True, index=True)
    username = Column(String(100),unique=True,index=True)
    email = Column(EmailType, unique=True,index=True)
    hashed_password = Column(String(300))
    is_active = Column(Boolean())
    posted_course = relationship('Course',back_populates="owner",single_parent=True,cascade="all, delete-orphan")
    date_created = Column(DateTime(),default=dt.datetime.now(NEPAL_TIMEZONE))

    def verify_password(self,password_to_check:str):
        return _hash.bcrypt.verify(password_to_check,self.hashed_password)



class Course(db.Base):
    __tablename__ = 'course'
    id = Column(Integer(),primary_key=True, index=True)
    title = Column(String(200),index=True)
    posted_by = Column(Integer(), ForeignKey('admin.id'))
    date_created = Column(String(200),default=str(dt.datetime.now(NEPAL_TIMEZONE)))
    date_last_updated = Column(DateTime(),default=dt.datetime.now(NEPAL_TIMEZONE))
    image_url = Column(URLType,index=True)
    category = Column(String(300),nullable=False,index=True)
    pick_id = Column(String(100),nullable=False,index=True,unique=True)
    owner = relationship("Admin",back_populates='posted_course')
    description = Column(Text(),nullable=False,index=True)
    content = relationship("Content", back_populates="course", cascade="all, delete-orphan")
    instructor = relationship("Instructor", back_populates="course", cascade="all, delete-orphan")


    def setData(self, course_data, admin_id: int, image_url: str):
        self.course_data = course_data
        self.title = course_data.title
        self.posted_by = admin_id
        self.category = course_data.category
        self.date_created = course_data.date_created
        self.image_url = image_url
        self.pick_id = course_data.pick_id
        self.description =course_data.description

    def send_with_data(self, **kwargs):

        if ("content" in kwargs and kwargs.get("content") == True):
            self.content = self.content

        if ("instructor" in kwargs and kwargs.get("instructor") == True):
            self.instructor = self.instructor

        return self

    def send_with(self, content, instructor):
        self.course_data = self.course_data.dict()
        self = self.course_data
        self["content"] = content 
        self["instructor"] = instructor
        return self




class Vacancy(db.Base):
    __tablename__ = 'vacancy'
    id = Column(Integer(), primary_key=True,index=True)
    name_of_vacancy = Column(String(3000),nullable=False,index=True)
    date_created = Column(String(200),default=str(dt.datetime.now(NEPAL_TIMEZONE)))
    pick_id = Column(String(50),index=True,unique=True)
    location_of_company = Column(String(300), nullable=False,index=True)
    post_type = Column(String(3000), nullable=False,index=True) #full time/part time
    vacancy_type = Column(String(300),index=True,nullable=False)
    name_of_organization = Column(String(300),index=True)
    description = Column(Text(),index=True)
    email_of_office = Column(EmailType,index=True,nullable=False)
    number_of_office = Column(String(10),index=True,nullable=False)
    posted_by = Column(Integer(),ForeignKey('admin.id'))
    logo_url_of_company = Column(String(300),index=True,nullable=False)
    salary_proposed = Column(String(300),index=True,nullable=False,default="Negotable")
    experience_required = Column(Text,index=True,nullable=False)
    education_required = Column(Text,index=True,nullable=False)
    other_qualification = Column(Text,index=True,nullable=False)

class Content(db.Base):
    __tablename__ = 'content'
    id = Column(Integer(),primary_key=True,index=True)
    duration_time = Column(Integer(),index=True)
    pick_id = Column(String(50),index=True,unique=True)
    overview_description = Column(Text(),index=True)
    about_data = Column(Text(),index=True,nullable=False)
    overview_data = Column(String(300),index=True,nullable=False)
    learned_information = Column(String(400),index=True,nullable=True)
    course_id = Column(Integer(), ForeignKey("course.id"))
    course = relationship("Course", back_populates="content")

    def setData(self, content_data, course_id, pick_id):
        self.duration_time = content_data.duration_time
        self.pick_id = pick_id
        self.overview_description = content_data.overview_description
        self.about_data = content_data.about_data
        self.overview_data = content_data.overview_data
        self.learned_information = content_data.learned_information
        self.course_id = course_id

class Instructor(db.Base):
    __tablename__ = 'instructor'
    id = Column(Integer(),primary_key=True,index=True)
    name = Column(String(300),nullable=False,index=True)
    organization = Column(String(400),index=True,nullable=False,default="Freelancer")
    education=Column(String(400),index=True,nullable=True)
    experience = Column(String(400),index=True,nullable=True)
    number_of_instructor = Column(String(10),nullable=False,unique=True)
    course_id = Column(Integer(), ForeignKey("course.id"))
    course = relationship("Course", back_populates="instructor")

    def setData(self, instructor_data, course_id):
        self.name = instructor_data.name_of_instructor
        self.organization = instructor_data.organization_of_instructor
        self.education = instructor_data.education_of_instructor
        self.experience = instructor_data.experience_of_instructor
        self.number_of_instructor = instructor_data.number_of_instructor
        self.course_id = course_id

class Enquiry(db.Base):
    __tablename__ ='enquiry'
    id = Column(Integer(),primary_key=True,index=True)
    user = relationship('User',back_populates='enquired',cascade="all, delete-orphan",single_parent=True)
    posted_user_id = Column(Integer(),ForeignKey('user.id'))
    message = Column(Text(),nullable=False,index=True)
    subject = Column(String(3000),nullable=False,index=True)
    enquiry_for = Column(String(50),nullable=False,index=True)
    date = Column(DateTime(),default=dt.datetime.now(NEPAL_TIMEZONE))
    # enquired_course = Column(Integer(),ForeignKey('course.id'))
    pick_id = Column(String(50),index=True,unique=True)
