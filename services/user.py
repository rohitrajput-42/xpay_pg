from fastapi import FastAPI, HTTPException, status
import datetime
import uuid
from db.db import get_db
from utils.utils import create_hash
import uuid

def get_users(request, user_id):
    try:
        db = get_db()
        with db.get_connection() as connection:
            cursor = connection.cursor()
            
            query = f"SELECT * FROM user_config WHERE id = '{user_id}';"
            cursor.execute(query)
            user_data = cursor.fetchone()

            json_data = dict(zip([column.name for column in cursor.description], user_data))

            query = f"SELECT * FROM profile WHERE user_id = '{user_id}';"
            cursor.execute(query)
            profile_data = cursor.fetchone()

            json_data.update({"profile_pic": profile_data[2]})

        db.put_connection(connection)
        if json_data:
            return {"user_data": json_data, "status_code": status.HTTP_200_OK}
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No system configurations found")
            
    except Exception as e:
        print("Error ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def create_user(request, payload):
    is_uploaded = 0
    email_counter = 0
    phone_counter = 0
    try:
        id = str(uuid.uuid4())
        full_name = payload["full_name"]
        email = payload["email"]
        hashed_pwd = create_hash(payload["password"])
        phone = payload["phone"]
        profile_picture = payload["profile_picture"]
        
        db = get_db()
        with db.get_connection() as connection:
            cursor = connection.cursor()

            id = str(uuid.uuid4())
            id = id.replace("-", "_")
            cursor.execute(f'select * from user_config')
            data = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            check_data = [dict(zip(column_names, row)) for row in data]

            if len(check_data) != 0:
                for check in check_data:
                    if email == check["email"]:
                        email_counter = 0
                    else:
                        email_counter = 1

                    if phone == check["phone"]:
                        phone_counter = 0
                    else:
                        phone_counter = 1

                if email_counter == 1:
                    if phone_counter == 1:
                        cursor.execute(f'INSERT INTO user_config(id, full_name, email, password, phone) VALUES (%s, %s, %s, %s, %s) RETURNING * ', 
                                    (id, full_name, email, hashed_pwd, phone))
                        
                        cursor.execute(f'INSERT INTO profile(user_id, profile_picture) VALUES (%s, %s) RETURNING * ', 
                                    (id, profile_picture))

                        is_uploaded = 1
                    else:
                        return {"description" : "Phone number already registerd, please use a different phone number", "status_code" : status.HTTP_409_CONFLICT}
                else:
                    return {"description" : "Email already registerd, please use a different email", "status_code" : status.HTTP_409_CONFLICT}
            else:
                cursor.execute(f'INSERT INTO user_config(id, full_name, email, password, phone) VALUES (%s, %s, %s, %s, %s) RETURNING * ', 
                            (id, full_name, email, hashed_pwd, phone))
                
                cursor.execute(f'INSERT INTO profile(user_id, profile_picture) VALUES (%s, %s) RETURNING * ', 
                            (id, profile_picture))

                is_uploaded = 1

        db.put_connection(connection)
        if is_uploaded == 1:
            return {"description" : "User successfully Registered", "status_code" : status.HTTP_201_CREATED}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Some error, Please try again")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))