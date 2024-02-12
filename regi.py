from fastapi import HTTPException, status
from fastapi_mail import MessageSchema, FastMail
from jose import jwt, JWTError



@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    new_user = User(email=user.email)
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    verification_token = create_verification_token(data={"sub": new_user.email})
    send_verification_email(new_user.email, verification_token)
    return new_user

def create_verification_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def send_verification_email(email: str, token: str):
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=f"Click the following link to verify your email: {verify_url}?token={token}",
    )
    fastmail.send_message(message)

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
verify_url = "http://your_domain/verify-email"

@app.post("/verify-email/")
def verify_email(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    user.is_verified = True
    db.commit()

    return {"message": "Email successfully verified"}


