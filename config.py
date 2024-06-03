from enum import Enum

IMAGE_TYPE = '.png'
IMAGE_FOLDER = './images'

DATA_PATH = 'data.json'


# for Json seria
class FilterType(str, Enum):
    ALL = 'ALL'
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    LINK = 'LINK'
    TABLE = 'TABLE'
    CODE = 'CODE'
    PASSWORD = 'PASSWORD'
    UNKNOWN = 'UNKNOWN'


class DataType(str, Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    HTML = 'HTML'
