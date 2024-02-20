from fastapi import FastAPI, File, UploadFile
import uvicorn

# Import Logger class from secore_log_lin
from secore_log_lin import Logger

app = FastAPI()

# Create an instance of the Logger class
logger_instance = Logger()

@app.post("/api/v1/upload")
def upload_json(request, file: UploadFile = File()):
    # Save the JSON file
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(file.file.read())
    
    # Add information to the log using the instance of Logger
    logger_instance.add_log_entry(request.client.host)
    
    # Return success response
    return {"success": True, "message": "File uploaded successfully!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
