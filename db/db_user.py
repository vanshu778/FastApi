from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser
from db.hash import Hash
from fastapi import HTTPException, status

def create_user(db:Session,request:UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db:Session):
    return db.query(DbUser).all()

def get_user(db:Session, id:int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return 

def update_user(db:Session,id:int, request:UserBase): 
    user=db.query(DbUser).filter(DbUser.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    user.update({
        DbUser.username:request.username,
        DbUser.email:request.email,
        DbUser.password:Hash.bcrypt(request.password)
    })
    db.commit()
    return 'ok'

def delete_user(db:Session, id:int):
    user=db.query(DbUser).filter(DbUser.id == id).first()
    if not delete_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')

    #Handle any exceptions
    db.delete(user)
    db.commit()
    return 'ok'