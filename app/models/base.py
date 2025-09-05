from beanie import Document
from datetime import datetime

# base mongodb model
class BaseDocument(Document):
  created_at: datetime = datetime.utcnow()
  updated_at: datetime = datetime.utcnow()

  class Settings:
    use_state_management = True
    validate_on_save = True