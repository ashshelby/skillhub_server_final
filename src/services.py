import sqlalchemy.orm as _orm
from sqlalchemy import or_
import src.database as _database
import src.models as _models
import passlib.hash as _hash
import src.schemas as _schemas
import jwt as _jwt
import fastapi.security as _security
from datetime import datetime,timedelta
import fastapi as _fastapi
from json import dumps as _dumps
from fastapi import Request,UploadFile
import os
import random
import string


def get_pickid()->str:
    return "".join(random.choices(string.ascii_letters,k=10))
#during production store this in a evnriornment variable, I cant do that becasuse right now the dot env module is not working
oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/auth/user")
JWT_SECRET_KEY :str = "SUPER_SECRET_JWT_KEY_GO_BRR"
FILE_PATH = os.path.join(os.getcwd(),'images')
LOGO_FILE_PATH = os.path.join(os.getcwd(),'images','logos')


def check_image_integrety(name)->bool:
    bad_chars = ['../','/','/..']
    for bad_char in bad_chars:
        if bad_char in name:
            return False
    return True


def get_random_data_for_image()->str:
    return "".join(random.choices(string.ascii_letters,k=14))


def check_with_email(email:str,db:_orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()

def defaultconverter(o):
  if isinstance(o, datetime):
      return o.__str__()


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    except StopIteration :
        pass
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
        pass

def make_db(db:_orm.Session = get_db()):
    try :
        return next(db)
    except StopIteration:
        return next(get_db())

#def register_user(user_data:_schemas.UserCreate,db:_orm.Session):
#    user_obj = _models.User(email=user_data.email,username=user_data.username,password_hashed=_hash.bcrypt.hash(user_data.password),phone_number=user_data.phone_number)
#    print("returning user_object")
#    db.add(user_obj)
#    db.commit()
#    db.refresh(user_obj)
#    return user_obj


#def make_authentication_token(user_obj:_schemas.UserCreate,db:_orm.Session):
#    user = _schemas.User.from_orm(user_obj)
#    # print("here in jwt")
#    # print(type(user))
#    print("this is the dict")
#    print(user.dict())
#    payload = {
#        "dat":user.dict(),
#     "exp":int((datetime.utcnow() + timedelta(days=7)).timestamp()),
#     "ist":int(datetime.utcnow().timestamp())
#     }
#    token = _jwt.encode(payload, JWT_SECRET_KEY)
#    return token

def make_authentication_token_admin(admin_obj:_schemas.AdminCookie,db:_orm.Session):
    admin = _schemas.AdminCookie.from_orm(admin_obj)
    # print("here in jwt")
    # print(type(user))
    print("this is the dict")
    print(admin.dict())
    payload = {
        "dat":admin.dict(),
     "exp":int((datetime.utcnow() + timedelta(days=7)).timestamp()),
     "ist":int(datetime.utcnow().timestamp())
     }
    token = _jwt.encode(payload, JWT_SECRET_KEY)
    return token

def get_current_admin(token:str,db:_orm.Session = make_db()):
    try:
        payload = _jwt.decode(token,JWT_SECRET_KEY,algorithms=["HS256"])
    except Exception as e:
        print(e)
    # admin = db.query(_modles.Admin).get(payload['dat']['id'])
    try:
        return payload
    except UnboundLocalError:
        raise _fastapi.HTTPException(status_code=301,detail="No Such User in Database")

def get_current_user(token:str,db:_orm.Session = make_db()):
    try:
        print(token)
        try:
            payload = _jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            print(e)
        print('payload is')
        print(payload)
        user = db.query(_models.User).get(payload["dat"]['id'])
        user.date_created = str(user.date_created)
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(status_code=401,detail="Invalid Credentials")
    return _schemas.UserCookie.from_orm(user)

def check_with_email_admin(email:str,db:_orm.Session):
    print("IN DB ADMIN")
    try:
    # print((db.query(_models.Admin).filter(_models.Admin.email == email).first()).hashed_password)
        return db.query(_models.Admin).filter(_models.Admin.email == email).first()
    except AttributeError:
        raise _fastapi.HTTPException(status_code=401,detail="No Such User")

def create_admin(admin_data:_schemas.AdminPost,db:_orm.Session = make_db()):
    admin_obj = _models.Admin(email=admin_data.email,username=admin_data.username,hashed_password=_hash.bcrypt.hash(admin_data.password),is_active=True)
    db.add(admin_obj)
    db.commit()
    db.refresh(admin_obj)
    return [f"{admin_obj.username}'s account is created","SUCCESS"]

def check_if_admin(request:Request):
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        raise _fastapi.HTTPException(status_code=301,detail="Unauthorized")
    token = auth_header.split(' ')[1]
    # print(auth_header)
    admin_d = get_current_admin(token)
    try:
        if admin_d['dat']['is_active'] == True:
            return True
    except KeyError:
        return False

def add_instructor_to_db(instructor_data:_schemas.InstructorGet,db:_orm.Session=make_db()):
    instructor_object = _models.Instructor(name=instructor_data.name_of_instructor,organization=instructor_data.organization_of_instructor,experience=instructor_data.experience_of_instructor,education=instructor_data.education_of_instructor,number_of_instructor=instructor_data.number_of_instructor)
    try:
        db.add(instructor_object)
        db.commit()
        db.refresh(instructor_object)
        # print(add_rert)
        # print(com_retr)
        db.expire_all()
        return True
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(status_code=201,detail=str("Instructor with that number already exists"))


def delete_user(user_obj,db:_orm.Session):
    db_data = db.query(_models.User).filter(_models.User.email ==user_obj.email).first()
    try:
        db.delete(db_data)
        db.commit()
        db.refresh(db_data)
        return f"deleted user {user_obj.username}"
    except Exception as e:
        print(e)
        return e
    
def delete_admin(admin_obj,db:_orm.Session = make_db()):
    print(admin_obj['dat']['email'])
    db_data = db.query(_models.Admin).filter(_models.Admin.email ==admin_obj['dat']['email']).first()
    try:
        db.delete(db_data)
        db.commit()
        # db.refresh(db_data)
        return f"deleted user {db_data.username}"
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(status_code=401,detail="INVALID REQUEST")


def get_token(request:Request):
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        raise _fastapi.HTTPException(status_code=301,detail="Unauthorized")
    token = auth_header.split(' ')[1]
    return token

async def add_vacancy(logo_image_url:str,vacancy_data:_schemas.VacaPost,posted_by:int,db:_orm.Session = make_db()):
    vacancy_object = _models.Vacancy(location_of_company=vacancy_data.location_of_company,name_of_vacancy=vacancy_data.name_of_vacancy,name_of_organization=vacancy_data.name_of_organization,description=vacancy_data.description,vacancy_type=vacancy_data.vacancy_type,posted_by=posted_by,salary_proposed=vacancy_data.salary_proposed,pick_id=vacancy_data.pick_id,email_of_office=vacancy_data.email_of_office,experience_required=vacancy_data.experience_required,other_qualification=vacancy_data.other_qualification,post_type=vacancy_data.post_type,logo_url_of_company=logo_image_url,number_of_office=vacancy_data.number_of_office,education_required=vacancy_data.education_required,date_created=vacancy_data.date_created)
    try:
        db.add(vacancy_object)
        await db.commit()
        db.refresh(vacancy_object)
        # db.close()
        return ["Vacancy Posted",vacancy_object.pick_id]
    except Exception as e:
        raise _fastapi.HTTPException(status_code=401,detail=str(e))


def get_all_vacancys(db= make_db()):
    db.expire_all()
    return db.query(_models.Vacancy).all()

def save_image(image:UploadFile):
    try:
        main_file_name = image.filename.split('.')[0]+get_random_data_for_image()+'.'+image.filename.split('.')[-1]
        file_name = os.path.join(FILE_PATH,main_file_name)
        with open(file_name,"wb+") as image_writer:
            image_writer.write(image.file.read())
        
        return "/images/"+file_name
    except Exception as e:
        print(e)
        return None

def save_logo_image(image:UploadFile):
    try:
        main_file_name = image.filename.split('.')[0]+get_random_data_for_image()+"."+image.filename.split('.')[-1]
        file_name = os.path.join(LOGO_FILE_PATH,main_file_name)
        with open(file_name,"wb+") as image_writer:
            image_writer.write(image.file.read())
        
        return file_name
    except Exception as e:
        print(e)
        return None



def add_course_to_db(image_name:str,admin_id:int,course_data:_schemas.CoursePost,course_content:_schemas.ContentGet,instructor_data:_schemas.InstructorGet,db:_orm.Session=make_db()):
    
    course = _models.Course()
    course.setData(course_data, admin_id, image_name)

    try: 
        db.add(course)
        db.commit()
        db.refresh(course)
    except Exception as e:
        print(e)
        
        raise _fastapi.HTTPException(500, detail="Cannot save the course data, Maybe that pick id already exists")


    content = _models.Content()
    instructor = _models.Instructor()

    try: 
        content.setData(course_content, course.id, get_pickid())
        instructor.setData(instructor_data, course.id)
        db.add_all([content, instructor])
        db.commit()
        db.refresh(content)
        db.refresh(instructor)

    except Exception as e:
        print(e)
        # db.delete(course)
        # db.delete(content)
        # db.delete(instructor)
        # db.commit()
        raise _fastapi.HTTPException(201, detail="Instructor with that number already exists")

    db.expire_all()
    return course.send_with(content, instructor)


    # pass



def get_all_courses(db = make_db()):
    print(db)
    db=  make_db()
    return db.query(_models.Content).with_entities(_models.Course, _models.Content, _models.Instructor).filter(_models.Course.id == _models.Content.course_id).filter(_models.Course.id == _models.Instructor.course_id).all()
    


def get_course_by_id(id:str,db=make_db()):
 return  db.query(_models.Course).filter(_models.Course.pick_id == id).with_entities(_models.Course, _models.Content, _models.Instructor).filter(_models.Course.id == _models.Content.course_id).filter(_models.Course.id == _models.Instructor.course_id).first()



def get_vacancy_by_id(id:str,db=make_db()):
    pick_id=id
    vacancy_datas =  db.query(_models.Vacancy).filter(_models.Vacancy.pick_id==pick_id).first()
    # vacancy_datas = db.get(vacancy_datas)
    print(vacancy_datas)
    _database.SessionNow.remove()
    new_vacancy_data  = {"pick_id":id,"vacancy_data":_schemas.VacancyReturn.from_orm(vacancy_datas)}
    return new_vacancy_data



def add_enquiry_data_to_db(enquiry_data:_schemas.EnquiryGet,db:_orm.Session = make_db()):
    try:
        pick_id_new =  get_pickid()
        user_obj = _models.User(full_name=enquiry_data.full_name,email=enquiry_data.email,phone_number=enquiry_data.phone_number,pick_id=pick_id_new)
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        user_obj = db.query(_models.User).filter(pick_id_new==_models.User.pick_id).first()
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(status_code=302,detail="Error working with User Data")
    try:
        enquiry_obj = _models.Enquiry(message=enquiry_data.message,subject=enquiry_data.subject,posted_user_id=user_obj.id,pick_id=get_pickid(),enquiry_for=enquiry_data.enquiry_for)
        db.add(enquiry_obj)
        db.commit()
        db.refresh(enquiry_obj)
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(status_code=302,detail="Error Adding Enquiry Data")
        print(e)
    return ["added enquiry",enquiry_obj.pick_id]
    



def delete_course_data(course_pick_id:str,db:_orm.Session = make_db()):
    try :
        course_obj =  db.query(_models.Course).filter(_models.Course.pick_id == course_pick_id).first()
        print(course_obj)
        db.delete(course_obj)
        db.commit()
        db.refresh(course_obj)
        return {"deleted":course_obj.title}
    except Exception as e:
        print(e)
        return e

def delete_vacancy_data(vacancy_pick_id:str,db:_orm.Session = make_db()):
    try:
        vacancy_obj = db.query(_models.Vacancy).filter(_models.Vacancy.pick_id == vacancy_pick_id).first()
        db.delete(vacancy_obj)
        print('this vacancy obj')
        print(vacancy_obj)
        db.commit()
        # db.refresh(vacancy_obj)
        # db.close()
        return {"deleted":vacancy_obj.name}
    except Exception as e:
        print(e)
        return e


def delete_image(image_url:str):
    try :
        old_image_path = os.path.join(os.getcwd(),'images','logos',image_url.split('/')[-1])
        print("old image path is "+old_image_path)
        print("image url"+ image_url)
        # os.chdir('./images/logos')
        print("new "+os.getcwd())
        print()
        os.remove(old_image_path)
        return True
    except Exception as e:
        return e

def edit_vacancy_data(pick_id:str,new_data:_schemas.VacaPostEdit,image_file:UploadFile,db:_orm.Session = make_db()):
    print(pick_id)
    data_in_db = db.query(_models.Vacancy).filter( pick_id== _models.Vacancy.pick_id).first()
    print(data_in_db)
    print(type(data_in_db))

    new_file_name = save_image(image_file)
    print("saved image")
    print(data_in_db.logo_url_of_company)
    check = delete_image(data_in_db.logo_url_of_company)
    if check != True:
        print("failed to delete image")
        print(check)
        return check
        # db.close()
    if check == True:
        print("changing data in database")
        data_in_db.name_of_vacancy = new_data.name_of_vacancy
        data_in_db.name_of_organization = new_data.name_of_organization
        data_in_db.location_of_company = new_data.location_of_company
        data_in_db.post_type = new_data.post_type
        data_in_db.vacancy_type = new_data.vacancy_type
        data_in_db.description = new_data.description
        data_in_db.email_of_office = new_data.email_of_office
        data_in_db.number_of_office = new_data.number_of_office
        data_in_db.logo_url_of_company = "/images/"+new_file_name.split('/')[-1]
        data_in_db.salary_proposed = new_data.salary_proposed
        data_in_db.experience_required = new_data.experience_required
        data_in_db.education_required = new_data.education_required
        data_in_db.other_qualification = new_data.other_qualification
        db.commit()
        # db.close()
        print("done shit")
        return "Vacancy Succesfully Edited"

def edit_course_data():
    pass


def get_enquiry_data_back(of:str,db:_orm.Session = make_db()):
    #return enquiry_for using some data slicing
    if of=="course":
        db=make_db()
        #user ko email fullname phone number subject date created at ani message chiyo
        return db.query(_models.Enquiry).filter(_models.Enquiry.enquiry_for == "course").with_entities(_models.User,_models.Enquiry).filter(_models.Enquiry.posted_user_id ==_models.User.id ).all()
    elif of == "vacancy":
        db = make_db()
        datas =  db.query(_models.Enquiry).filter(_models.Enquiry.enquiry_for == "vacancy").with_entities(_models.User,_models.Enquiry).filter(_models.Enquiry.posted_user_id ==_models.User.id).all()
        return datas
    elif of==None:
        return db.query(_models.Enquiry).all()
    else:
        raise _fastapi.HTTPException(status_code=302,detail="Some error occured")

def get_vacancy_for_search(keyword:str,db:_orm.Session = make_db()):
    data =   db.query(_models.Vacancy).filter(or_(_models.Vacancy.name_of_vacancy.contains(keyword),_models.Vacancy.description.contains(keyword),_models.Vacancy.name_of_organization.contains(keyword),_models.Vacancy.location_of_company.contains(keyword),_models.Vacancy.post_type.contains(keyword),_models.Vacancy.vacancy_type.contains(keyword))).all()
    # print(str(data[0]))
    return data

def get_course_for_search(keyword:str,db:_orm.Session = make_db()):
    db = make_db()
    return  db.query(_models.Course).with_entities(_models.Instructor,_models.Content,_models.Course).filter(_models.Course.category.contains(keyword) ).filter(_models.Course.id == _models.Content.course_id).filter(_models.Course.id == _models.Instructor.course_id).all()

def delete_enquiry_data(id:str,db:_orm.Session = make_db()):
    try:
        enquiry_obj = db.query(_models.Enquiry).filter(_models.Enquiry.pick_id == id).first()
        print(enquiry_obj)
        db.delete(enquiry_obj)
        print(enquiry_obj)
        db.commit()
        db.expire_all()
        message = {"status":201,"Deleted":id}
    except Exception as e:
        print(enquiry_obj)
        print("exception: ",e)
        message = e
    return message

# define( 'DB_NAME', 'skillhub_wp821' );

# /** MySQL database username */
# define( 'DB_USER', 'skillhub_wp821' );

# /** MySQL database password */
# define( 'DB_PASSWORD', 'dW]S8p8!0N' );
def return_course_as_per_number(num:int,db:_orm.Session = make_db()):
    return  db.query(_models.Content).with_entities(_models.Course, _models.Content, _models.Instructor).filter(_models.Course.id == _models.Content.course_id).filter(_models.Course.id == _models.Instructor.course_id).limit(num).all()
    

def return_vacancy_as_per_number(num,db:_orm.Session = make_db()):
    db = make_db()
    return  db.query(_models.Vacancy).limit(num).all()
