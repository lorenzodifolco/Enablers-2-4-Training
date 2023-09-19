"""
File to include global variables across the python package and configuration.
All the other files inside the python package can access these variables.
"""
from decouple import config
import os
import pathlib
import json

TESTING = 'Importing a variable from conf.py'

MAIN_FOLDER_DEFAULT = pathlib.Path(__file__).parent.parent.absolute()
MAIN_FOLDER = config('MAIN_FOLDER', default=MAIN_FOLDER_DEFAULT)
DATASETS_FOLDER = os.path.join(MAIN_FOLDER,'datasets')
OUTPUTS_FOLDER = os.path.join(MAIN_FOLDER,'outputs')
KEY = config('KEY')

# Yet to check if this is really necessary, maybe only for cases where passing values as ENV VARS is too cumbersome
# e.g. [[1, 'a', ],['789', 'o', 9]] would be very annoying to write and parse.
CUSTOM_SETTINGS = {
    'key': {
        'default': 'value',
    },
    'pre_processing':{
        'some_config_preprocessing': 'values',
    }
}
PATH_CUSTOM_SETTINGS = os.path.join(MAIN_FOLDER, 'configuration.json')
if os.path.exists(PATH_CUSTOM_SETTINGS):
    with open(PATH_CUSTOM_SETTINGS, 'r') as f:
        CUSTOM_SETTINGS = json.load(f)

RAVDESS_LABEL_TO_EMOTION =  {"01":"neutral", 
                             "02":"calm",
                             "03":"happy",
                             "04":"sad",
                             "05":"angry",
                             "06":"fearful",
                             "07":"disgust",
                             "08":"surprised"
        }
RAVDESS_EMOTION_TO_LABEL =  {"neutral":"01",
                             "calm":"02",
                             "happy":"03",
                             "sad":"04",
                             "angry":"05",
                             "fearful":"06",
                             "disgust":"07",
                             "suprised":"08"
        }