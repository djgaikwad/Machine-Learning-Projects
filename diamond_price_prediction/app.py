from flask import *
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
app = Flask(__name__)
app.secret_key = 'abc'

@app.route('/')
def home():

    return render_template('home.html')

def pred(l1):
    model = pickle.load(open('predict.pkl','rb'))
    price = model.predict(l1)[0]
    return price

def sctrans(a):
    model = pickle.load(open('stdscl.pkl','rb'))
    trans = model.transform(a)
    return trans

def encode(a):
    model = pickle.load(open('ordencode.pkl','rb'))
    enc = model.transform(a)
    return enc

@app.route('/pred', methods = ['post'])
def newobs():
    carat = float(request.form['carat'])
    cut = request.form['cut']
    color = request.form['color']
    clarity = request.form['clarity']
    depth = float(request.form['depth'])
    table = float(request.form['table'])
    x = float(request.form['x'])
    y = float(request.form['y'])
    z = float(request.form['z'])
    list1 = [carat,cut,color,clarity,depth,table,x,y,z]
    print(list1)
    a=np.array([list1])
    o = encode([[a[0][1],a[0][2],a[0][3]]])
    s = sctrans([[a[0][0],a[0][4],a[0][5],a[0][6],a[0][7],a[0][8]]])
    l1=np.array([[s[0][0],o[0][0],o[0][1],o[0][2],s[0][1],s[0][2],s[0][3],s[0][4],s[0][5]]])
    p=pred(l1)
    return render_template("display.html",data=list1,price=round(p,2))


    

if __name__ =='__main__':
    app.run(debug=True)