import datetime
import os
import zipfile

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.gis.geos import GEOSGeometry
import psycopg2
from psycopg2.sql import SQL, Identifier

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
            {gdal_path} ogr2ogr  -f PostgreSQL  PG:"{databaseInfo}" {folder_path} -nln {file_name} -nlt MULTIPOLYGON """
            os.system(command)
        except Exception as e:
            print(e)
            return Response(status=500)
        return Response(status=204)

class FeatureApiView(APIView):


    def post(self, request,layer_name, format=None):
        try:
            geos = GEOSGeometry(request.data)
            geoJson = geos.json
            properties = geoJson['properties']
            wkb = geos.wkb
            with getDatabaseConnection() as connection:
                with connection.cursor() as curser:
                    sql = SQL("Insert into {} (%s,%s) values (%s,%s)").format(Identifier(layer_name))
                    geoColumn = getGeometryColumns(curser, layer_name)
                    curser.execute(sql,(geoColumn,','.join(properties.keys()),wkb,','.join(properties.values())))
        except ValueError as e:
            return Response(status=422, exception=e)
        except Exception as e:
            return Response(status=500, exception=e)





def getDatabase():
    NAME = os.environ.get('DB_NAME')
    USER = os.environ.get('DB_USER')
    PASSWORD = os.environ.get('DB_PASS')
    HOST = os.environ.get('DB_HOST')
    return f'host={HOST} user={USER} password={PASSWORD} dbname={NAME} port=5432'
def getDatabaseConnection():
    NAME = os.environ.get('DB_NAME')
    USER = os.environ.get('DB_USER')
    PASSWORD = os.environ.get('DB_PASS')
    HOST = os.environ.get('DB_HOST')
    psycopg2.connect('dbname='+NAME+' user='+USER +' password='+PASSWORD+'host='+HOST+'port=5432')

def getGeometryColumns(curser,table_name):
    curser.execute("select f_geometry_column from geometry_columns where f_table_name = %s", (table_name,))
    return curser.fetchone()[0]
