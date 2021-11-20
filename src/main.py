import os
import pymongo
from datetime import datetime, timedelta

# Obtenemos las variables de entorno
URI_MONGODB_SRC = os.getenv("URI_MONGODB_SRC")
URI_MONGODB_DST = os.getenv("URI_MONGODB_DST")
COLLECTION_SRC = os.getenv("COLLECTION_SRC")
COLLECTION_DST = os.getenv("COLLECTION_DST")
COMMIT_SECONDS = int(os.getenv("COMMIT_SECONDS"))

db_src = pymongo.MongoClient(URI_MONGODB_SRC).get_database()
col_src = db_src[COLLECTION_SRC]
db_dst = pymongo.MongoClient(URI_MONGODB_DST).get_database()
col_dst = db_dst[COLLECTION_DST]
count_changes = 0
last_time = datetime.utcnow()
path_offset = "/app/data/offset"

print("App start with COMMIT_SECONDS={0}".format(COMMIT_SECONDS))

# Leemos el fichero donde almacenamos el ultimo offset, si no existe le creamos
try:
    f = open(path_offset, "r")
    token = f.read()
    f.close()
    token = {'_data': token}
    print("Last offset: {0}".format(token))

except FileNotFoundError:
    token = None

# Nos subscribimos a los cambios de la coleccion y vamos actualizando los offset en el documento
with col_src.watch(start_after=token) as stream:
    while stream.alive:
        change = stream.try_next()
        if change is not None:
            # print("Change: {0}".format(change))
            count_changes += 1
            f = open(path_offset, "w")
            f.write(change["_id"]["_data"])
            f.close()

        # Si han pasado X segundos actualizamos
        now = datetime.utcnow()
        if now >= last_time + timedelta(seconds=COMMIT_SECONDS):
            print("{0} - {1} Changes".format(now, count_changes))

            # Si ha habido cambios insertamos la cantidad en base de datos
            if count_changes > 0:
                col_dst.insert_one({"date": now, "collection": COLLECTION_SRC, "count": count_changes})
            count_changes = 0
            last_time = now
