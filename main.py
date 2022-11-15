from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os,sys
import io
import csv
import codecs
import pandas as pd
from sensor.logger import logging
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
import os
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.constant.training_pipeline import SCHEMA_DROP_COLS,SCHEMA_FILE_PATH
from fastapi import FastAPI,File, UploadFile
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response,FileResponse,StreamingResponse
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        df = df.drop(schema_config[SCHEMA_DROP_COLS],axis=1)
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        predicted_arr = model.predict(df)
        prediction = pd.DataFrame(list(predicted_arr))
        prediction.columns = ["class"]
        prediction.replace(TargetValueMapping().reverse_mapping(), inplace=True)
        predicted_dataframe = pd.concat([df, prediction], axis=1)
        predicted_dataframe = io.StringIO()
        return StreamingResponse(iter([predicted_dataframe.getvalue()]),media_type="text/csv")
    except Exception as e:
            raise SensorException(e,sys)
  
if __name__=="__main__":

    app_run(app, host=APP_HOST, port=APP_PORT)






    