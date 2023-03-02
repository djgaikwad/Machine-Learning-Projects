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
    output = model.predict(l1)[0]
    if output == 0 :
        return f'Client not left the membership'
    
    else:
        return f'Client will left the membership'

def sctrans(a):
    model1 = pickle.load(open('stdscl.pkl','rb'))
    trans = model1.transform(a)
    return trans

@app.route('/pred', methods = ['post'])
def newobs():
    CreditScore = float(request.form['creditscore'])
    Age = float(request.form['age'])
    Tenure = float(request.form['tenure'])
    Balance = float(request.form['balance'])
    NumOfProducts = float(request.form['products'])
    HasCrCard = int(request.form['creditcard'])
    IsActiveMember = int(request.form['active'])
    EstimatedSalary = float(request.form['salary'])
    obs = [[CreditScore,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary]]
    a = np.array(obs)
    a1 = sctrans([[a[0][0],a[0][1],a[0][3],a[0][-1]]])
    a2 = np.array([[a1[0][0],a1[0][1],Tenure,a1[0][2],NumOfProducts,HasCrCard,IsActiveMember,a1[0][3]]])
    p=pred(a2)
    if HasCrCard==1:
        i='Yes'
    else:
        i='No'
    if IsActiveMember==1:
        j='Yes'
    else:
        j='No'
    list1= [CreditScore,Age,Tenure,Balance,NumOfProducts,i,j,EstimatedSalary]
    return render_template('display.html',data=list1,msg=p)

if __name__ =='__main__':
    app.run(debug=True)