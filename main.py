import pandas as pd
from datetime import datetime as dt
import os
import shutil


def get_str_timestamp():
    return str(dt.now().strftime('%Y%m%d%H%M%S'))


def get_asistencia(source_files, target):
    df = pd.DataFrame()
    for f in source_files:
        if f.endswith('.xls') or f.endswith('.xlsx'):
            df = df.append(pd.read_excel(f), ignore_index=True)
    df = df.assign(Dia=pd.to_datetime(df['Tiempo'], dayfirst=True).dt.date).\
        drop_duplicates(subset=(['ID de Usuario', 'Dia']))
    df.head()
    nom = get_str_timestamp() + ".xlsx"
    destination = os.path.abspath(os.path.join(target, nom))

    df.to_excel(destination)


if __name__ == '__main__':
    source_dir_name = "a-procesar"
    target_dir_name = "procesados"

    source_path = os.path.abspath(source_dir_name)
    backup_path = os.path.abspath('archivados')

    files = [os.path.abspath(os.path.join(source_dir_name, i)) for i in os.listdir(source_dir_name)]

    get_asistencia(files, target_dir_name)

    for file in files:
        shutil.move(os.path.join(source_path, file), backup_path)
