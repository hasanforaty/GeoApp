import datetime

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from django.conf import settings
import zipfile


class ShapeFileUploadApiView(APIView):

    def post(self, request, format=None):

        try:
            file_obj = request.data['file']
            today_date = datetime.date.today().strftime("%Y%m%d")
            folder_path = f"./tmp/shapefiles/{file_obj.name}_{today_date}"
            gdal_path = settings.GDAL_LIBRARY_PATH
            file_name = file_obj.name.rsplit(".")[0]+today_date
            with zipfile.ZipFile(file_obj, 'r') as zip_ref:
                zip_ref.extractall(path=folder_path)
            databaseInfo = getDatabase()
            command = f"""
            {gdal_path} ogr2ogr -append -f PostgreSQL  PG:"{databaseInfo}" {folder_path} -nln {file_name}
             -nlt MULTIPOLYGON """
            os.system(command)
        except Exception as e:
            print(e)
            return Response(status=500)
        return Response(status=204)


def getDatabase():
    NAME = os.environ.get('DB_NAME')
    USER = os.environ.get('DB_USER')
    PASSWORD = os.environ.get('DB_PASS')
    HOST = os.environ.get('DB_HOST')
    return f'host={HOST} user={USER} password={PASSWORD} dbname={NAME} port=5432'
