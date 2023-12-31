from flask import Blueprint, render_template, request, flash
import requests 
import pandas as pd
from bs4 import BeautifulSoup

api = 'https://data.cms.gov/data-api/v1/dataset/f1a8c197-b53d-4c24-9770-aea5d5a97dfb/data?size=1500'
resp = requests.get(api).json()
df = pd.DataFrame(resp)

views = Blueprint(__name__,'views')

@views.route('/opd-treatment', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        state = request.form.get('state')
        if len(state) < 1:
            flash('Error. No selection made. Select a location to view provider information.',category='error')
            return render_template('home.html')
        else:
            st = df[df['STATE']==state]
            col = st.shape[0]
            total = df.shape[0]

            npi_col = st['NPI']
            prov_col = st['PROVIDER NAME'].str.title()
            addr1 = st['ADDRESS LINE 1'].str.title()
            addr2 = st['ADDRESS LINE 2'].str.title()
            city = st['CITY'].str.title()
            state_col = st['STATE']
            zip_col = st['ZIP']
            date_col = st['MEDICARE ID EFFECTIVE DATE']
            phone = st['PHONE']
            infos = zip(npi_col,prov_col,addr1,addr2,city,state_col,zip_col,date_col,phone)
    
            soup = BeautifulSoup(open('/home/jaynamiproductions/opioid-treatment-finder/templates/home.html'))
            state_name = soup.find(attrs={"value": state}).get_text()

            return render_template('index.html',
                                   num=col,
                                   ttl=total,
                                   place=state,
                                   name=state_name,
                                   infos=infos)
    else:
        return render_template('home.html')
    

@views.route('/otp-faq')
def faq():
    return render_template('faq.html')

@views.route('/')
def about():
    return render_template('about.html')

@views.route('/npi-validation',methods=['GET','POST'])
def check():
    if request.method == 'POST':
        npi = request.form.get('npi')
        if len(npi) < 1:
            flash('No entry made.',category='error') 
        elif len(npi) != 10:
            flash(npi + ' is invalid.',category='error')
        elif npi.startswith('1') or npi.startswith('2'):
            new = npi[-2::-1]
            test = ''
            for i in range(len(new)):
                if i % 2 == 0:
                    test += str(int(new[i])*2)
                else:
                    test += new[i]
            total = map(int, str(test))
            final = sum(total)+24
            check = 10 - (final%10)
            if check == int(npi[-1]):
                flash(npi + ' is valid.',category='success')
            else:
                flash(npi + ' is invalid.',category='error')
        return render_template('npi.html',num=npi)
    else:
        return render_template('npi.html')