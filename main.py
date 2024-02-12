from aiolimiter import AsyncLimiter

rate_limiter = AsyncLimiter(rate=5, period=10)

async def create_contact_async(contact_data: ContactCreate, current_user: User, db: Session):

    contact = Contact(**contact_data.dict(), user_id=current_user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

@app.post("/contacts/", response_model=ContactInDB)
async def create_contact(
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
        Create a new contact.

        :param contact: Contact data.
        :param db: Database session.
        :param current_user: Current authenticated user.

        :return: Created contact.
        """
    async with rate_limiter:
        created_contact = await create_contact_async(contact_data, current_user, db)
        return created_contact