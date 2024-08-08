import sys
#from signLanguage.configuration.s3_operations import S3Operation
from signLanguage.entity.artifacts_entity import (
    ModelPusherArtifacts,
    ModelTrainerArtifact
)

from signLanguage.entity.config_entity import ModelPusherConfig
from signLanguage.exception import SignException
from signLanguage.logger import logging
import shutil
import os

class ModelPusher:

    #def __init__(self,model_pusher_config: ModelPusherConfig,model_trainer_artifact: ModelTrainerArtifact, s3: S3Operation):

    def __init__(self,model_pusher_config: ModelPusherConfig,model_trainer_artifact: ModelTrainerArtifact):

        self.model_pusher_config = model_pusher_config
        self.model_trainer_artifacts = model_trainer_artifact
        #self.s3 = s3
    
    def initiate_model_pusher(self) -> ModelPusherArtifacts:

       
        logging.info("Entered initiate_model_pusher method of Modelpusher class")
        try:
            # Uploading the best model to s3 bucket

            trained_model_path = self.model_trainer_artifacts.trained_model_file_path


            #copy to model_pusher directory
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)

            #copy to saved_model directory
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)

            # self.s3.upload_file(
            #     self.model_trainer_artifacts.trained_model_file_path,
            #     self.model_pusher_config.S3_MODEL_KEY_PATH,
            #     self.model_pusher_config.BUCKET_NAME,
            #     remove=False,
            # )
            logging.info("Uploaded best model to s3 bucket")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")

            # Saving the model pusher artifacts
            model_pusher_artifact = ModelPusherArtifacts(
                saved_model_path = saved_model_path,
                model_file_path = model_file_path
                
            )

            return model_pusher_artifact

        except Exception as e:
            raise SignException(e, sys) from e