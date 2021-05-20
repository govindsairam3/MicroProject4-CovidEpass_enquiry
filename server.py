from flask import Flask, render_template, request
from twilio.rest import Client
import requests
import requests_cache

account_sid = 'AC1619be4816f2569ca3f394415c265575'
auth_token = 'e26f51d120b79f84e857fe5afec64ced'

client = Client(account_sid,auth_token)
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def registration_form():
    return render_template('test_page.html')

@app.route('/details', methods=['POST','GET'])
def login_registration_details():
    first_name = request.form['fname']
    #last_name = request.form['lname']
    email_id = request.form['email']
    source = request.form['Source']
    destination = request.form['Destination']
    dest_dist = request.form['Destination-District']
    contact = request.form['Contact No']
    #id_proof = request.form['ID']
    #date = request.form['date_to_GO']
    fullname = first_name #+'.'+ last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    count = json_data[destination]['districts'][dest_dist]['total']['confirmed']
    population = json_data[destination]['districts'][dest_dist]['meta']['population']
    travel_pass = ((count/population)*100)
    if travel_pass <30 and request.method=='POST' :
        status = 'CONFIRMED'
        #return status
        client.messages.create(to="whatsapp:+917013510927", from_="whatsapp:+14155238886", body="Hello "+fullname+"your travel is "+status)
        return render_template('login_page.html',var=first_name,var1=email_id,var2=source,var3=destination,var4=dest_dist,var5=contact,var6=status)
    else:
        status= 'NOT_CONFIRMED'
        #return status
        client.messages.create(to="whatsapp:+917013510927", from_="whatsapp:+14155238886", body="Hello "+fullname+"your travel is "+status)
        return render_template('login_page.html',var=first_name,var1=email_id,var2=source,var3=destination,var4=dest_dist,var5=contact,var6=status)


if __name__ == "__main__":
    app.run(port=9000,debug=True)