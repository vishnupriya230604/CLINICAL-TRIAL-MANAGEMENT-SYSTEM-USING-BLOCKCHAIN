from hashlib import sha3_512
from flask import Flask, render_template, request
from datetime import datetime
import bcrypt

app = Flask(__name__, template_folder='templates')
app = Flask(__name__, static_folder='static')
app.secret_key = 'gotohell'

blockchain = []

class ClinicalTrialRecord:
    def __init__(self, patient_name, trial_id, age, report):
        self.timestamp = datetime.now()
        self.patient_name = patient_name
        
        self.trial_id = self.hash_trial_id(trial_id)
        self.age = age
        self.report = report
        self.previous_hash = self.calculate_previous_hash()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hash_data = str(self.timestamp) + self.patient_name + str(self.trial_id) + str(self.age) + self.report
        return sha3_512(hash_data.encode()).hexdigest()

    def calculate_previous_hash(self):
        if len(blockchain) > 0:
            previous_record = blockchain[-1]
            return previous_record.hash
        else:
            return None

    def hash_trial_id(self, trial_id):
        return bcrypt.hashpw(trial_id.encode(), bcrypt.gensalt()).decode()

@app.route('/addtobc', methods=['POST'])
def addtobc():
    patient_name = request.form['patient_name']
    age = request.form['age']
    report = request.form['report']
    trial_id = request.form['trial_id']

    record = ClinicalTrialRecord(patient_name, trial_id, age, report)
    blockchain.append(record)

    return f'Report added to blockchain successfully. Your Trial ID - {trial_id}'

@app.route('/view_blockchain', methods=['GET'])

def view_blockchain():
    return render_template('blockchain.html', blockchain=blockchain)


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def login():
    return render_template('login.html')
@app.route('/addreport')
def addreport():
    return render_template('addreport.html')
@app.route('/viewreport')
def viewreport():
    return render_template('view.html')


if __name__ == '__main__':
    app.run(debug=True)