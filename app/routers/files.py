import os
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse

UPLOAD_DIR = "uploads"
# create the folder if does not exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/files", tags=["files"])

# upload file route
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
  try:
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # write the file to the path
    with open(file=file_path, mode="wb") as buffer:
      buffer.write(await file.read())

    # normalize the path => had to slashes 
    file_path = file_path.replace("\\", "/")

    return {"filename": file.filename, "path": file_path}

  except Exception:
    raise HTTPException(status_code=500, detail="File upload failed")

# get file by name
@router.get("/{filename}")
async def get_file(filename: str):
  # file folder path + filename
  file_path = os.path.join(UPLOAD_DIR, filename)

  # if path does not exists
  if (not os.path.exists(file_path)):
    raise HTTPException(status_code=404, detail="File not found")
  
  return FileResponse(path=file_path)
