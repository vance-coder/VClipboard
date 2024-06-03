import os
import json
import time
from copy import deepcopy
from pathlib import Path

from PyQt5.QtGui import QPixmap

from config import FilterType, IMAGE_TYPE, IMAGE_FOLDER, DATA_PATH


def save_data(data: list):
    previous_data = []
    if Path(DATA_PATH).exists():
        with open(DATA_PATH, encoding='utf-8') as fp:
            previous_data = json.loads(fp.read())

    previous_id_list = [row['id'] for row in previous_data]
    data_id_list = [row['id'] for row in data]

    # 如果previous_id_list有，data list没有则是被删除了，所以需要同时删除previous_id_list里面的数据
    deleted_list = [row for row in previous_data if row['id'] not in data_id_list]
    for row in deleted_list:
        # 删除对应的图片如果存在的话
        if row['filterType'] == FilterType.IMAGE:
            os.remove(os.path.join(IMAGE_FOLDER, str(row['id']) + IMAGE_TYPE))
        # remove the item from previous_data
        previous_data.remove(row)

    for idx, row in enumerate(data):
        if row['id'] in previous_id_list:
            # no need to handle it again because this item has been saved before
            continue

        # 底下数据就是新增的，需要额外保存
        row_data = row.pop('data')
        new_row = deepcopy(row)  # in case affect the original data
        if row['filterType'] == FilterType.IMAGE:
            # save image to disk
            filename = str(row['id']) + IMAGE_TYPE
            image: QPixmap = row_data
            image.save(os.path.join(IMAGE_FOLDER, filename))
            new_row['data'] = filename
        else:
            new_row['data'] = row_data

        row['data'] = row_data

        previous_data.append(new_row)

    new_data = json.dumps(previous_data, indent=4, ensure_ascii=False)
    with open(DATA_PATH, 'w+', encoding='utf-8') as fp:
        fp.write(new_data)


def load_data() -> list:
    data = []
    if Path(DATA_PATH).exists():
        with open(DATA_PATH, encoding='utf-8') as fp:
            data = json.loads(fp.read())

    new_data = []
    for row in data:
        if row['filterType'] == FilterType.IMAGE:
            # load images with filename
            filename = row.pop('data')
            row['data'] = QPixmap()
            row['data'].load(os.path.join(IMAGE_FOLDER, filename))

        new_data.append(row)
    return new_data
