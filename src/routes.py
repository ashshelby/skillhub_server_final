from fastapi import FastAPI, Request,File,UploadFile,Form
import fastapi.security as _security
import fastapi as _fastapi
from pydantic import BaseModel
print("importing schemas")
import src.schemas as schemas
import sqlalchemy.orm as _orm
import src.models as models
import src.services as _services
from src.database import SessionLocal
from fastapi.responses import FileResponse
import os
from fastapi.middleware.cors import CORSMiddleware
# from my_web_framework import get_current_request, on_request_end
from typing import Optional

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://localhost:3500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post('/api/token')
# def generate_token(form_data:_security.OAuth2PasswordRequestForm =_fastapi.Depends(),db:_orm.Session = _fastapi.Depends(_services.get_db)):
#     user = _services.make_authentication_token(form_data.email, db)
#     pass

# @app.post('/api/add/user')
# def add_user(form_data:schemas.UserCreate, db:_orm.Session = _fastapi.Depends(_services.get_db)):
#     print("add  user request")
#     print(form_data.phone_number)
#     if  _services.check_with_email(form_data.email,db):
#         raise _fastapi.HTTPException(status_code=401,detail="Email Already Exists")

#     return _services.register_user(form_data, db=_services.get_db())
    
# @app.delete('/api/del/user')
# def delete_user(request:Request,db:_orm.Session = _fastapi.Depends(_services.get_db)):
#     auth_header = request.headers.get('Authorization')
#     if auth_header == None:
#         raise _fastapi.HTTPException(status_code=301,detail="Unauthorized")
#     token = auth_header.split(' ')[1]
#     user_to_delete = _services.get_current_user(token)
#     return _services.delete_user(user_to_delete,db)

@app.delete('/api/del/admin')
def delete_admin(request:Request):
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        raise _fastapi.HTTPException(status_code=301,detail="Unauthorized")
    token = auth_header.split(' ')[1]
    admin_to_delete = _services.get_current_admin(token)
    return _services.delete_admin(admin_to_delete)


# @app.post('/api/auth/user')
# def login_user(form_data:schemas.UserAuth,db:_orm.Session =_fastapi.Depends(_services.get_db)):
#     print("authenticating")
#     print(form_data)
#     user = _services.check_with_email(form_data.email, db)
#     if not user:
#         raise _fastapi.HTTPException(status_code=401,detail="No Such Account Found")
#     if not user.verify_password(form_data.password):
#         raise _fastapi.HTTPException(status_code=302,detail="Incorrect Credentials")
    
#     user.date_created = str(user.date_created)
#     print(type(user.date_created))
#     token = _services.make_authentication_token(user,db)
    
#     return dict(access_token=token,token_type="bearer")
#     # ash@gmail.com ashutosh

# @app.get('/api/me')
# def self_information(request:Request):
#     auth_header = request.headers.get('Authorization')
#     if auth_header == None:
#         raise _fastapi.HTTPException(status_code=301,detail="Unauthorized")
#     token = auth_header.split(' ')[1]
#     user_d = _services.get_current_user(token)
#     return user_d

@app.post('/api/add/admin')
def create_admin(admin_data:schemas.AdminPost):
    print("add admin request ")
    if _services.check_with_email_admin(admin_data.email, db= _services.make_db()) :
        raise _fastapi.HTTPException(status_code=301,detail="An Admin of that email is already there")
    return _services.create_admin(admin_data)

@app.post('/api/auth/admin')
def login_admin(login_admin_data:schemas.AdminAuth,db:_orm.Session = _fastapi.Depends(_services.get_db)):
    print(login_admin_data)
    admin = _services.check_with_email_admin(login_admin_data.email, db)
    if not admin:
        raise _fastapi.HTTPException(401, detail="No such Admin Found")
    if not admin.verify_password(login_admin_data.password):
        raise _fastapi.HTTPException(status_code=302,detail="Incorrect Credentials")
    
    admin.date_created = str(admin.date_created)
    admin.password_hashed = admin.hashed_password
    print(admin)
    token = _services.make_authentication_token_admin(admin, db)
    return dict(token=token,token_type="bearer",is_admin=True)

# @app.post('/api/add/instructor')
# def add_instructor(request:Request,instructor_data:schemas.InstructorGet = _fastapi.Depends()):
#     return _services.add_instructor_to_db(instructor_data)

# course_data :schemas.CoursePost= _fastapi.Depends(),course_content:schemas.ContentGet = _fastapi.Depends(),instructor_data :schemas.InstructorGet= _fastapi.Depends(),career_image:UploadFile,
@app.post('/api/add/course')
async def add_course(request:Request,course_image:UploadFile,course_content:schemas.ContentGet = _fastapi.Depends(schemas.ContentGet.as_form),instructor_data:schemas.InstructorGet = _fastapi.Depends(schemas.InstructorGet.as_form),course_data :schemas.CoursePost= _fastapi.Depends(schemas.CoursePost.as_form)):
    print(course_image.content_type)
    if not "image/" in course_image.content_type:
        raise _fastapi.HTTPException(status_code=301,detail="invalid file type")
    if  _services.check_if_admin(request):
        token = _services.get_token(request)
        posted_by = _services.get_current_admin(token)
        image_name = _services.save_image(course_image).split('/')[-1]
        image_name = "images/"+os.path.basename(image_name)
        if image_name != None:
            # return [course_data,course_content,instructor_data]
            return  _services.add_course_to_db(image_name,posted_by['dat']['id'],course_data,course_content,instructor_data,db=_services.make_db())

        else:
            raise _fastapi.HTTPException(status_code=302,detail="NOT AN ADMIN")



massive_w=1

@app.get('/images/{image_id}')
def image(image_id:str)->UploadFile:
    if not _services.check_image_integrety(image_id):
        raise _fastapi.HTTPException(status_code=301,detail="Bad Characters in image, please change image name")
        
    
    images = os.listdir(_services.FILE_PATH)
    path = os.path.join(_services.FILE_PATH,image_id)
    #FileResponse(path)
    if image_id not in images:
        raise _fastapi.HTTPException(status_code=404,detail="No Such Image")
    else :
        return FileResponse(path)

    

@app.get('/api/checkadmin')
def test(request:Request)->bool:
    if not  _services.check_if_admin(request):
        raise _fastapi.HTTPException(status_code=302,detail="UNAUTHORIZED")
    else :return True
    
@app.post('/api/enquiry')
def get_enqury(request:Request,enquiry_data:schemas.EnquiryGet,db:_orm.Session = _fastapi.Depends(_services.get_db)):

    return _services.add_enquiry_data_to_db(enquiry_data)
    




@app.get('/api/search/vacancy/{keyword}',response_model=list[schemas.VacancyReturn],response_model_exclude_unset=True)
async def get_search_vacancy(keyword:str)->list:
    return  _services.get_vacancy_for_search(keyword)

@app.get('/api/search/course/{keyword}')
def get_search_vacancy(keyword:str)->list:
    return _services.get_course_for_search(keyword=keyword)



# 9841629817

@app.post('/api/add/vacancy')
def vacancy_add(logo_image:UploadFile,request:Request,vacancy_data:schemas.VacaPost = _fastapi.Depends(schemas.VacaPost.as_form)):
    if not _services.check_if_admin(request):
        raise _fastapi.HTTPException(status_code=302,detail="UNAUTHORIZED")
    token = _services.get_token(request)
    posted_by = _services.get_current_admin(token)

    if not "image/" in logo_image.content_type:
        raise _fastapi.HTTPException(status_code=301,detail="invalid file type")
    image_name = _services.save_logo_image(logo_image).split('/')[-1]
    image_name = os.path.basename(image_name)
    final_image_name = f"/images/logos/{image_name}"
    # return final_image_name
    return _services.add_vacancy(final_image_name,vacancy_data,posted_by['dat']['id'])
    # return [vacancy_data,{"posted_by":posted_by_email}]

@app.get('/images/logos/{logo_id}')
def return_logo_for_vacancy(logo_id:str)->UploadFile:
    print(os.getcwd())
    images = os.listdir(_services.LOGO_FILE_PATH)
    path = os.path.join(_services.LOGO_FILE_PATH,logo_id)
    #FileResponse(path)
    print(path)
    if logo_id not in images:
        raise _fastapi.HTTPException(status_code=404,detail="No Such Image")
    else :
        return FileResponse(path)

@app.delete('/api/course/{course_pick_id}/delete')
async def delete_course(request:Request,course_pick_id:str):
    print('hit delete '+course_pick_id)
    if not _services.check_if_admin(request):
        raise _fastapi.HTTPException(status_code=302,detail="Not Permitted")
    return  _services.delete_course_data(course_pick_id)


@app.delete('/api/vacancy/{vacancy_pick_id}/delete')
async def delete_vacancy(request:Request,vacancy_pick_id:str):
    if not _services.check_if_admin(request):
        raise _fastapi.HTTPException(302,"Not Permitted")
    return  _services.delete_vacancy_data(vacancy_pick_id)


# ,response_model=list[schemas.VacancyReturn],response_model_exclude_unset=True
@app.get('/api/get/vacancy/all',response_model=list[schemas.VacancyReturn],response_model_exclude_unset=True)
async def get_vacancys()->list:
    return   _services.get_all_vacancys()

@app.get('/')
def root()->dict:
    return {"Skillhub API":"Corpe Diem"}

@app.get('/api/get/course/all')
async def get_all_course()->list:
    return   _services.get_all_courses()

@app.get('/api/get/course/{id}')
async def get_course_by_id(id:str)->dict:
    return   _services.get_course_by_id(id)

@app.get('/api/get/vacancy/{id}')
async def get_vacancy_by_id(id:str)->dict:
    return  _services.get_vacancy_by_id(id)

# @app.put('/api/vacancy/{pick_id}/edit')
# def edit_vacancy(vacancy_image:UploadFile,pick_id:str,new_vacancy_data:schemas.VacaPostEdit = _fastapi.Depends(schemas.VacaPostEdit.as_form)):
#     return _services.edit_vacancy_data(pick_id,new_vacancy_data,vacancy_image)

# @app.put('/api/course/{pick_id}/edit')
# def edit_course(pick_id:str,request:Request,course_image:UploadFile,course_content:schemas.ContentGet = _fastapi.Depends(schemas.ContentGet.as_form),instructor_data:schemas.InstructorGet = _fastapi.Depends(schemas.InstructorGet.as_form),course_data :schemas.CoursePostEdit()= _fastapi.Depends(schemas.CoursePostEdit.as_form)):
#     return _services.edit_course_data(pick_id,course_data,course_content,instructor_data,course_image)

@app.get('/api/get/enquiry/{of}')
async def get_enquiry(of:Optional[str]  = None)->dict:
    return  _services.get_enquiry_data_back(of)

@app.delete('/api/enquiry/{pick_id}/delete')
async def delete_enquiry_data(pick_id:str)->dict:
    return  _services.delete_enquiry_data(pick_id)

# get random 8 course data
# get random 8 vacancy data
# @app.get(/course/num):
@app.get('/api/course/{num}')
async def return_course_as_per_number(num:int):
    return  _services.return_course_as_per_number(num)

@app.get('/api/vacancy/{num}',response_model=list[schemas.VacancyReturn],response_model_exclude_unset=True)
def return_vacancy_as_per_number(num:int):
    return  _services.return_vacancy_as_per_number(num)


@app.get('/.well-known/{file_name}')
def support(file_name:str):
    if file_name =="support.txt" or file_name =="security.txt":
        return {"contact":"developer@skillhubltd.org"}
    if file_name == "hacker.txt":
        return {"can never be hacked boyee :))"}
    else:
        raise _fastapi.HTTPException(418,"Tea")
