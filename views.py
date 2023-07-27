from flask import Blueprint, render_template, request, flash
import requests 
import pandas as pd
from bs4 import BeautifulSoup

api = 'https://data.cms.gov/data-api/v1/dataset/f1a8c197-b53d-4c24-9770-aea5d5a97dfb/data?size=1500'
resp = requests.get(api).json()
df = pd.DataFrame(resp)

views = Blueprint(__name__,'views')

@views.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        state = request.form.get('state')
        if len(state) < 1:
            return render_template('error.html')
        else:
            st = df[df['STATE']==state]
            col = st.shape[0]
            total = df.shape[0]
        
            soup = BeautifulSoup(open('templates/home.html'))
            state_name = soup.find(attrs={"value": state}).get_text()

            return render_template('index.html', tables=[st.to_html(classes='data',index=False)],num=col,ttl=total,place=state,name=state_name)
    else:
        return render_template('home.html')