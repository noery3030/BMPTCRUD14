import pymongo

#Membuat koneksi url mongo

koneksi_url = "mongodb://localhost:27017"

def cekKoneksi() :
    client =  pymongo.MongoClient(koneksi_url)
    try:
        cek = client.list_database_names()
        print(cek)
    except:
        print('database error')
# cekKoneksi()


def createDatabase():
    myclient = pymongo.MongoClient(koneksi_url)
    mydatabase = myclient['dbTB']
    mycollection = mydatabase['material']
    mydocument = mycollection.insert_one({ 'kode': 'BTK001', 'nama_material' : 'batu bata', 'harga' : '1000', 'stok': '250000' })

    return mydocument
# createDatabase()

class MongoCRUD:
    def __init__(self,data,koneksi):
        self.client = pymongo.MongoClient(koneksi)
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data
    
    def readData(self):
        documents = self.collection.find()
        value = [{
            item: data[item] for item in data if item != '_id'} for data in documents]
        return value
    
    def createData(self, data):
        new_documents = data['document']
        response = self.collection.insert_one(new_documents)
        value = {
            'Status' : 'Berhasil',
            'Document_id' : str(response.inserted_id)
        }
        return value

    def editData(self):
        beforeData = self.data['beforeData']
        update_data = {
            "$set" : self.data['afterData']
        }

        response = self.collection.update_one(beforeData, update_data)
        value = {
            "Status" : "Berhasil Diupdate" if response.modified_count > 0 else "Data tidak Ditemukan"
        }

        print(value)
    
    def deleteData(self, data):
        delete_data = data['document']
        response = self.collection.delete_one(delete_data)
        value = {
            'Status' : 'Berhasil Dihapus' if response.deleted_count > 0 else "Data tidak Ditemukan"
        }

        print(value)

if __name__ == '__main__':
    data = {
        # nama database yang akan disambungkan
        "database": "dbTB",
        # nama collection yang akan di sambungkan
        "collection": "material",

        "beforeData": {
            "kode" : "BTK001",
            "nama_material" : "batu bata",
            "harga" : 1000,
            "stok" : 250000

        },
        
        "afterData":{
            "kode" : "BTK001",
            "nama_material" : "batu kali",
            "harga" : 1500,
            "stok" : 300000
        }
    }

    delete_data = {
        'document':{
            "kode" : "BTK001",
            "nama_material" : "batu bata",
            "harga" : 1000,
            "stok" : 250000
        }
    }

    mongo_objek = MongoCRUD(data, koneksi_url)
    readData =  mongo_objek.readData()
    print(readData)

    mongo_objek = MongoCRUD(data, koneksi_url)
    createData = mongo_objek.createData({
            'document':{
            "kode" : "BTK001",
            "nama_material" : "batu bata",
            "harga" : 1000,
            "stok" : 250000
        }
    })
    print(createData)

    mongo_objek = MongoCRUD(data, koneksi_url)
    mongo_objek.editData()

    mongo_objek = MongoCRUD(data, koneksi_url)
    delete = mongo_objek.deleteData(delete_data)