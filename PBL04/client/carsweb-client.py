from flask import Flask, render_template, request, redirect, url_for
import json, requests

app = Flask(__name__)

global appType 

appType = 'Web Service'

@app.route('/')
def index():
    return render_template('index.html', appType=appType)

@app.route('/createcar')
def createcar():
    return render_template('createcar.html', appType=appType)

@app.route('/createcarsave',methods=['GET','POST'])
def createcarsave():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']

    datacar = {
        "carname" : fName,
        "carbrand" : fBrand, 
        "carmodel" : fModel,
        "carprice" : fPrice
    }
    
    datacar_json = json.dumps(datacar)

    alamatserver = "http://localhost:5055/cars/"
    
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('readcar'))


@app.route('/readcar')
def readcar():
    alamatserver = "http://localhost:5055/cars"
    datas = requests.get(alamatserver)

    rows = json.loads(datas.text)

    return render_template('readcar.html', rows=rows, appType=appType)

@app.route('/updatecar')
def updatecar():
    return render_template('updatecar.html', appType=appType)

@app.route('/updatecarsave', methods=['POST'])
def updatecarsave():
    fId = request.form['id']
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']

    # Prepare the car data to be updated
    datacar = {
        "id": fId,
        "carname": fName,
        "carbrand": fBrand,
        "carmodel": fModel,
        "carprice": fPrice
    }
    datacar_json = json.dumps(datacar)
    headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

    # Send a PUT request to the external API to update the car
    response = requests.put(f"http://localhost:5055/cars/", data=datacar_json, headers=headers)

    if response.status_code == 200:
        return redirect(url_for('readcar'))
    else:
        # Handle error (you might want to show an error message)
        return f"Error: {response.status_code}"

@app.route('/deletecar')
def deletecar():
    return render_template('deletecar.html', appType=appType)

@app.route('/deletecarsave', methods=['GET','POST'])
def deletecarsave():
    fName = request.form['carName']

    datacar = {
        "carname" : fName
    }
    
    datacar_json = json.dumps(datacar)

    alamatserver = "http://localhost:5055/cars/"
    
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.delete(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('readcar'))

@app.route('/searchcar')
def searchcar():
    return render_template('searchcar.html', appType=appType)

@app.route('/searchcarinput', methods=['POST'])
def searchcarinput():
    if request.method == 'POST':
        search_term = request.form.get('searchTerm')

        # Send a GET request to the external API to search for cars
        params = {'searchTerm': search_term}
        response = requests.get("http://localhost:5055/cars/search", params=params)

        if response.status_code == 200:
            results = response.json()  # Assuming the API returns JSON
        else:
            results = []  # Handle no results or error

        return render_template('searchcar.html', results=results, appType=appType)



if __name__ == '__main__':
    
    app.run(
        host = '0.0.0.0',
        debug = 'True'
        )