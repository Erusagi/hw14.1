from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import cloudinary
from cloudinary import uploader

cloudinary.config(
    cloud_name="your_cloud_name",
    api_key="your_api_key",
    api_secret="your_api_secret",)

DATABASE_URL = "enter your URL"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

@app.put("/users/update-avatar/")
def update_user_avatar(
    avatar: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """
       Update user avatar.

       :param avatar: New avatar file.
       :param current_user: Current authenticated user.

       :return: Message indicating success.
       """
    response = uploader.upload(avatar.file, folder="avatars", overwrite=True)

    current_user.avatar_url = response["secure_url"]
    db.commit()

    return {"message": "Avatar updated successfully"}