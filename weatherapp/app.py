from flask import Flask, render_template, request , session ,redirect,url_for ,  flash
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SECRET_KEY'] = 'thisisasecret'

db=SQLAlchemy(app)

class City(db.Model):
    id= db.Column(db.Integer , primary_key=True)
    name= db.Column(db.String , nullable=False)

def get_weather_data(city):

    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&appid=40e0f2f0449bf1c3b7a90caae3553193'
    r= requests.get(url).json()
    print(r)
    return r


@app.route("/" )
def index_get():
    
    cities = City.query.all()
    weather_data= []

    for city in cities:

        r= get_weather_data(city.name)
         

        weather= {
            'city': city.name,
            'tempature': r['main']['temp'],
            'humidity':r['main']['humidity'],
            'desc':  r['weather'][0]['description'],
            'icon':  r['weather'][0]['icon'],

        }
        
        weather_data.append(weather)

    # print(weather_data)


    return render_template('index.html' ,weather_data = weather_data) 



@app.route("/" , methods =[ 'POST'])
def index_post():
    err_msg=''
    new_city= request.form.get('city').capitalize()
    
    if new_city:
        existing_city= City.query.filter_by(name=new_city).first()

        if not existing_city:
            city_exists= get_weather_data(new_city)
            if city_exists['cod'] ==200:

                new_city_obj = City(name=new_city)
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg='City name is  Incorrect!'
        else:
            err_msg='City already exists in list!'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added succesfully!')


    return redirect(url_for('index_get'))

@app.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted { city.name }', 'success')
    return redirect(url_for('index_get'))

    




if __name__ == "__main__":
    app.run(debug=True)      











    