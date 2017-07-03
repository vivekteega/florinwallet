from flask import render_template, flash, redirect, request
from app import app
from .forms import walletForm
import subprocess,os
import json
import requests

if os.name=='nt':
	flodlocation = 'C:\\Program Files\\Florincoin\\daemon\\florincoind.exe '
	floclilocation = 'C:\\Program Files\\Florincoin\\daemon\\florincoin-cli.exe '
	homelocation = os.path.expanduser("~")
	doclocation = os.path.join(homelocation,"Documents") 
elif os.name=='posix':
	flodlocation = 'florincoind '
	floclilocation = 'florincoin-cli '
	homelocation = os.path.expanduser("~")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET', 'POST'])
def home():
	string = floclilocation+'getbalance'
	output = subprocess.check_output(string)
	for line in output.splitlines():
		available = float(line)			
	string = floclilocation+'getunconfirmedbalance'
	output = subprocess.check_output(string)
	for line in output.splitlines():
		pending = float(line)

	string = floclilocation+'listunspent'
	output = subprocess.check_output(string, universal_newlines=True)
	output = json.loads(output)
	tablelst = []
	for cur in output:
		temp = []
		temp.append(cur['address'])
		temp.append(cur['amount'])
		temp.append(cur['spendable'])
		tablelst.append(temp)
	return render_template("home.html", available=available, pending= pending, tablelst = tablelst)


@app.route('/send', methods=['GET', 'POST'])
def login():
    form = walletForm()
    if form.validate_on_submit():
        exestring = floclilocation + "sendtoaddress "+ str(form.address.data)+" "+str(form.amount.data)+" "+str(form.comm.data)
        result = subprocess.check_output(exestring)
        flash('FLO sent with transaction id="%s"' %
              (result))
        return redirect('/')
    return render_template('send.html', form=form)


@app.route('/receive', methods=['GET'])
def receive():
	return render_template('receive.html')


@app.route('/genadd', methods=['POST'])
def genadd():
	exestring = floclilocation + "getnewaddress"
	result = subprocess.check_output(exestring)
	flash('New address ="%s"' % (result))
	return redirect('/receive')

@app.route('/backup', methods=['GET'])
def backup():
	return render_template("newbackup.html")

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(doclocation, 'flo-backup')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    tstr = ''
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        tstr = os.path.join(target, filename)
    exestring = floclilocation+"importwallet "+tstr
    output = subprocess.check_output(exestring)
    return render_template("newbackup.html")
    #return str(exestring)

@app.route('/rates')
def rates():
	response = requests.get("https://poloniex.com/public?command=returnTicker").json()
	polxprice = response["BTC_FLO"]["last"]
	response = requests.get("https://bittrex.com/api/v1.1/public/getticker?market=BTC-FLO").json()
	btrexprice = response['result']['Last']
	btrexprice = '%.8f' % (btrexprice)
	return render_template('rates.html', btrexprice = btrexprice, polxprice = polxprice)