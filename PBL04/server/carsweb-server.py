from flask import Flask, jsonify, request
from peewee import *
from flask_restful import Resource, Api, reqparse 

app = Flask(__name__)
api = Api(app)

db = SqliteDatabase('carsweb.db')

class BaseModel(Model):
    class Meta:
        database = db

class TBCarsWeb(BaseModel):
    carname = TextField()
    carbrand = TextField() 
    carmodel = TextField()
    carprice = TextField()

def create_tables():
    with db:
        db.create_tables([TBCarsWeb])

@app.route('/')
def masukkeindeks():
    return "Server Ready"

@app.route('/read')
def readdata():
    rows = TBCarsWeb.select()    
    datas=[]

    for row in rows:
        datas.append({
            'id':row.id,
            'carname':row.carname,
            'carbrand':row.carbrand,
            'carmodel':row.carmodel,
            'carprice':row.carprice
        })
    return jsonify(datas)

class CAR(Resource):
    def get(self):
        rows = TBCarsWeb.select()    
        datas=[]
        for row in rows:
            datas.append({
                'id': row.id,
                'carname': row.carname,
                'carbrand': row.carbrand,
                'carmodel': row.carmodel,
                'carprice': row.carprice
            })
        return jsonify(datas)

    def post(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carname')
        parserData.add_argument('carbrand')
        parserData.add_argument('carmodel')
        parserData.add_argument('carprice')

        parserAmbilData = parserData.parse_args()

        fName = parserAmbilData.get('carname')
        fBrand = parserAmbilData.get('carbrand')
        fModel = parserAmbilData.get('carmodel')
        fPrice = parserAmbilData.get('carprice')

        car_simpan = TBCarsWeb.create(
            carname=fName,
            carbrand=fBrand, 
            carmodel=fModel,
            carprice=fPrice
        )

        rows = TBCarsWeb.select()    
        datas = []
        for row in rows:
            datas.append({
                'id': row.id,
                'carname': row.carname,
                'carbrand': row.carbrand,
                'carmodel': row.carmodel,
                'carprice': row.carprice
            })
        return jsonify(datas)

    def put(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('id', required=True, help="ID is required")
        parserData.add_argument('carname')
        parserData.add_argument('carbrand')
        parserData.add_argument('carmodel')
        parserData.add_argument('carprice')

        args = parserData.parse_args()

        car_id = args['id']
        fName = args.get('carname')
        fBrand = args.get('carbrand')
        fModel = args.get('carmodel')
        fPrice = args.get('carprice')

        car = TBCarsWeb.get_or_none(TBCarsWeb.id == car_id)
        if car:
            car.carname = fName if fName else car.carname
            car.carbrand = fBrand if fBrand else car.carbrand
            car.carmodel = fModel if fModel else car.carmodel
            car.carprice = fPrice if fPrice else car.carprice
            car.save()

            return jsonify({'message': 'Car updated successfully'})

        return jsonify({'message': 'Car not found'}), 404


    def delete(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carname')

        parserAmbilData = parserData.parse_args()

        fName = parserAmbilData.get('carname') 

        car_delete = TBCarsWeb.delete().where(TBCarsWeb.carname==fName)
        car_delete.execute()

        rows = TBCarsWeb.select()    
        datas=[]
        for row in rows:
            datas.append({
                'id':row.id,
                'carname':row.carname,
                'carbrand':row.carbrand,
                'carmodel':row.carmodel,
                'carprice':row.carprice
            })
        return jsonify(datas)
    
class CARSearch(Resource):
    def get(self):
        # Extract 'searchTerm' from query parameters
        search_term = request.args.get('searchTerm')

        if not search_term:
            return {"error": "Search term is required"}, 400  # Return an error if searchTerm is missing

        # Perform the search query
        rows = TBCarsWeb.select().where(TBCarsWeb.carname.contains(search_term))
        datas = []

        for row in rows:
            datas.append({
                'id': row.id,
                'carname': row.carname,
                'carbrand': row.carbrand,
                'carmodel': row.carmodel,
                'carprice': row.carprice
            })

        return jsonify(datas)  # Return the search results as JSON

# Register the search resource
api.add_resource(CARSearch, '/cars/search', endpoint="search")



api.add_resource(CAR, '/cars/', endpoint="cars/")

if __name__ == '__main__':
    create_tables()
    app.run(
        host = '0.0.0.0',
        debug = 'True',
        port=5055
    )
