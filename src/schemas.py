import pydantic as _pydantic
from datetime import datetime
# from sqlalchemy import DateTime
import src.models as _models
from src.routes import Form

class ReturnCourseAll(_pydantic.BaseModel):
    pick_id:str
    title:str
    image_url:str
    class Config:
        orm_mode=True

class EnquiryGet(_pydantic.BaseModel):
    full_name:str 
    email:str 
    phone_number:str
    # pick_id:str
    message:str
    subject:str 
    enquiry_for:str
    # date:str 
    class Config:
        orm_mode = True



class InstructorGet(_pydantic.BaseModel):
    name_of_instructor:str
    organization_of_instructor:str
    education_of_instructor:str 
    experience_of_instructor:str 
    number_of_instructor:str
    @classmethod
    def as_form(
        cls,
        name_of_instructor:str = Form(),
        organization_of_instructor:str = Form(),
        education_of_instructor:str = Form(),
        experience_of_instructor:str = Form(), 
        number_of_instructor:str = Form()
    ):
        return cls(name_of_instructor=name_of_instructor,organization_of_instructor=organization_of_instructor,education_of_instructor=education_of_instructor,experience_of_instructor=experience_of_instructor,number_of_instructor=number_of_instructor)

class AdminPost(_pydantic.BaseModel):
    username:str
    password:str 
    email:str 
    class Config:
        orm_mode = True


class ContentGet(_pydantic.BaseModel):
    duration_time:int 
    # objective_data :str
    about_data :str
    overview_data :str
    learned_information:str
    overview_description:str
    category:str
    @classmethod
    def as_form(
    cls = Form(),
    duration_time:int = Form() ,
    # objective_data :str
    about_data :str = Form(),
    overview_data :str = Form(),
    learned_information:str = Form(),
    overview_description:str = Form(),
    category:str = Form()
    ):
        return cls(duration_time=duration_time,
        about_data=about_data,overview_data=overview_data,learned_information=learned_information,
        overview_description=overview_description,category=category)



class CourseGet(_pydantic.BaseModel):
    title:str 
    # content:ContentGet
    description:str 
    date_created:str
    # date_last_updated:str 
    pick_id:str
    category:str
    # image:bytes 
    class Config:
        arbitrary_types_allowed = True

class CoursePost(CourseGet):
    #needs a full revamp
    # def __init__(self,):
    @classmethod
    def as_form(cls,
    title:str =Form(),
    # content:ContentGet
    description:str =Form(),
    date_created:str = Form(),
    # date_last_updated:str =Form(),
    pick_id:str = Form(),
    category:str=Form()
    ):
        return cls(title=title,description=description,pick_id=pick_id,category=category,date_created=date_created)
    
class CoursePostEdit():
    title:str 
    # content:ContentGet
    description:str 
    # date_created:str
    # date_last_updated:str 
    # pick_id:str
    category:str
    # image:bytes 
    class Config:
        arbitrary_types_allowed = True
    #needs a full revamp
    # def __init__(self,):
    @classmethod
    def as_form(cls,
    title:str =Form(),
    # content:ContentGet
    description:str =Form(),
    # date_created:str = Form(),
    # date_last_updated:str =Form(),
    # pick_id:str = Form(),
    category:str=Form()
    ):
        return cls(title=title,description=description,category=category)

class VacancyGet(_pydantic.BaseModel):
    name_of_vacancy:str
    pick_id:str
    date_created:str
    location_of_company:str
    post_type:str
    vacancy_type:str
    name_of_organization:str
    description:str
    email_of_office:str 
    number_of_office:str
    salary_proposed:str 
    experience_required:str 
    education_required:str
    other_qualification:str
    class Config:
        orm_mode = True
    
    

class VacancyEditGet(_pydantic.BaseModel):
    name_of_vacancy:str
    # pick_id:str
    location_of_company:str
    post_type:str
    vacancy_type:str
    name_of_organization:str
    description:str
    email_of_office:str 
    number_of_office:str
    salary_proposed:str 
    experience_required:str 
    education_required:str
    other_qualification:str
    class Config:
        orm_mode = True
    


class VacaPost(VacancyGet):
    @classmethod
    def as_form(
        cls,
        name_of_vacancy:str = Form(),
        date_created:str = Form(),
        pick_id:str = Form(),
        location_of_company:str = Form(),
        post_type:str = Form(),
        vacancy_type:str = Form(),
        name_of_organization:str = Form(),
        description:str = Form(),
        email_of_office:str  = Form(),
        number_of_office:str = Form(),
        salary_proposed:str  = Form(),
        experience_required:str = Form(),
        education_required:str = Form (),
        other_qualification:str = Form()
        ):
        return cls(name_of_vacancy=name_of_vacancy,
        date_created=date_created,
        pick_id=pick_id,
        location_of_company=location_of_company,
        post_type=post_type,
        vacancy_type=vacancy_type,
        name_of_organization=name_of_organization,
        description=description,
        email_of_office=email_of_office,
        number_of_office=number_of_office,
        salary_proposed=salary_proposed,
        experience_required=experience_required,
        education_required=education_required,
        other_qualification=other_qualification
        )

    pass

class VacaPostEdit(VacancyEditGet):
    @classmethod
    def as_form(
        cls,
        name_of_vacancy:str = Form(),
        location_of_company:str = Form(),
        post_type:str = Form(),
        vacancy_type:str = Form(),
        name_of_organization:str = Form(),
        description:str = Form(),
        email_of_office:str  = Form(),
        number_of_office:str = Form(),
        salary_proposed:str  = Form(),
        experience_required:str = Form(),
        education_required:str = Form (),
        other_qualification:str = Form()
        ):
        return cls(name_of_vacancy=name_of_vacancy,
        location_of_company=location_of_company,
        post_type=post_type,
        vacancy_type=vacancy_type,
        name_of_organization=name_of_organization,
        description=description,
        email_of_office=email_of_office,
        number_of_office=number_of_office,
        salary_proposed=salary_proposed,
        experience_required=experience_required,
        education_required=education_required,
        other_qualification=other_qualification
        )

    pass

class VacancyReturn(_pydantic.BaseModel):
    name_of_vacancy:str
    pick_id:str
    date_created:str
    location_of_company:str
    post_type:str
    vacancy_type:str
    name_of_organization:str
    description:str
    email_of_office:str 
    number_of_office:str
    salary_proposed:str 
    # required_qualification:str
    logo_url_of_company:str
    experience_required:str 
    education_required:str
    other_qualification:str
    class Config:
        orm_mode = True


class User(_pydantic.BaseModel):
    id:int
    email:str
    password_hashed:str 
    date_created:str
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True



class UserCreate(_pydantic.BaseModel):
    email:str
    username:str
    password:str
    phone_number:str
    class Config:
        orm_mode = True

    

class UserAuth(_pydantic.BaseModel):
    email:str 
    password:str 
    class Config:
        orm_mode=True

class UserCookie(_pydantic.BaseModel):
    email:str 
    date_created:str
    class Config:
        orm_mode = True


class AdminAuth(_pydantic.BaseModel):
    email:str 
    password:str 
    class Config:
        orm_Mode = True 

class AdminCookie(_pydantic.BaseModel):
    id:int
    email:str
    # password_hashed:str 
    date_created:str
    is_active:bool
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CourseToReturn(_pydantic.BaseModel):
    title:str 
    id:int
    description:str
    category:str
    # content:str
    date_last_updated:datetime
    date_created:datetime
    class Config:
        orm_mode=True
        arbitrary_types_allowed = True

class ContentToReturn(_pydantic.BaseModel):
    duration_time:int 
    # objective_data :str
    about_data :str
    overview_data :str
    learned_information:str
    overview_description:str
    # category:str
    class Config:
        orm_mode=True
        arbitrary_types_allowed = True

