import asyncio
import os
import tempfile
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI()


async def run_cpg_program(input_path: str, output_path: str):
    try:
        env = os.environ.copy()

        command = f"$CPG_EXECUTABLE_PATH {input_path} --export-json {output_path} --no-neo4j"

        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
        )

        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=120,
        )

        if process.returncode != 0:
            logger.warning(f"External program failed with exit code {process.returncode}")
            logger.warning(f"STDERR: {stderr.decode()}")
            raise HTTPException(status_code=500)

    except asyncio.TimeoutError:
        logger.warning("External program took too long to respond.")
        raise HTTPException(status_code=500)


def cleanup_files(*file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up temporary file: {file_path}")


@app.post("/cpg")
async def post_cpg(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    if file.filename is None:
        raise HTTPException(status_code=400, detail="No file provided")

    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_input_file:
        input_path = temp_input_file.name

        content = await file.read()
        temp_input_file.write(content)

        logger.info(f"Temporary input file created at: {input_path}")

    output_path = f"{input_path}.json"

    await run_cpg_program(input_path, output_path)

    if os.path.exists(output_path):
        background_tasks.add_task(cleanup_files, input_path, output_path)
        return FileResponse(path=output_path, media_type="application/json")
    else:
        raise HTTPException(status_code=500)
