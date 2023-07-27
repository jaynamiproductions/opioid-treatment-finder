from flask import Blueprint, render_template, request
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
        st = df[df['STATE']==state]

        col = st.shape[0]

        soup = BeautifulSoup(open('templates/home.html'))
        html = st.to_html()
        state_name = soup.find(attrs={"value": state}).get_text()


        # text_file = open('templates/index.html', 'w')
        # text_file.write('templates/home.html')
        # text_file = open('templates/index.html', 'a')
        # text_file.write(html)

        return render_template('index.html',num=col,name=state_name)
    else:
    # print('There are ' + str(st.shape[0]) + ' opioid treamtent providers in ' + state + ' .')   
        return render_template('home.html')