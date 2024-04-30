
from models import Messages
from sqlalchemy.orm import session
from schemas import MessageSend

async def get_messages(db: session):
    # Execute the query using the session
    query = db.query(Messages).filter(Messages.is_active == True).all()
    return query


async def create_message(message_data:MessageSend, db:session):
    new_message = Messages(**message_data.model_dump())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message
