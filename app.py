from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from src.pipeline import Pipeline

app = FastAPI(title="PII Redaction Tool")


@app.get("/")
def home():
    return {
        "message": "PII Redaction API is running!"
    }


@app.post("/redact")
async def redact(file: UploadFile = File(...)):

    job_id = str(uuid.uuid4())

    upload_dir = Path("temp") / job_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    input_file = upload_dir / file.filename
    output_file = upload_dir / "redacted.docx"
    mapping_file = upload_dir / "mapping.json"
    report_file = upload_dir / "evaluation_report.json"

    with open(input_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pipeline = Pipeline()

    pipeline.execute(
        input_file=input_file,
        output_file=output_file,
        mapping_file=mapping_file,
        report_file=report_file,
    )

    return FileResponse(
        output_file,
        filename="redacted.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )