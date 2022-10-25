from flask import Flask,request,jsonify,render_template
import numpy as np
import pickle
import json
import config
from flask_mysqldb import MySQL

app = Flask(__name__)

# sql-connection-setup ##

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AjayAjay1504'
app.config['MYSQL_DB'] = 'bike_database'
mysql = MySQL(app)


@app.route("/")
def home_api():
    return render_template('index.html')

@app.route("/bike_price",methods=['GET','POST'])
def bike():

    with open(config.DATA_PATH,'r') as f:
        bike_data = json.load(f)

    with open(config.MODEL_PATH,'rb') as f:
        bike_model = pickle.load(f)

    test_array = np.zeros(len(bike_data['columns']))

    data  = request.form

    seller_type   = data['seller_type']
    test_array[0] = bike_data['seller_type'][seller_type]
    a = test_array[0]

    owner         = data['owner']
    test_array[1] = bike_data['owner'][owner]
    b = test_array[1]

    test_array[2] = eval(data['km_driven'])
    c = test_array[2]
 
    test_array[3] = eval(data['ex_showroom_price'])
    d = test_array[3]
    
    name          = data['name']
    name_index    = np.where(bike_data['columns'] == 'name_'+name)
    test_array[name_index] = 1
    e = test_array[name_index]

    test_array[283] = eval(data['no_of_years'])
    f = test_array[283]
   
    output = bike_model.predict([test_array])

    cursor = mysql.connection.cursor()
    query  = 'CREATE TABLE IF NOT EXISTS bike_price (seller_type VARCHAR(20),owner VARCHAR(20),km_driven VARCHAR(20),ex_showroom_price VARCHAR(20),name VARCHAR(45),no_of_years VARCHAR(20),output VARCHAR(20))'
    cursor.execute(query)
    cursor.execute('INSERT INTO bike_price (seller_type,owner,km_driven,ex_showroom_price,name,no_of_years,output) VALUES (%s,%s,%s,%s,%s,%s,%s)',(a,b,c,d,e,f,output))
    mysql.connection.commit()
    cursor.close()

    return render_template("index1.html",output=output)




if __name__ == "__main__":
    app.run(port=config.PORT_NO)




 