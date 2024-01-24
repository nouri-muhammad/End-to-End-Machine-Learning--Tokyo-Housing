import numpy as np
import pandas as pd 
from flask import Flask, request, render_template
from sklearn.preprocessing import StandardScaler 
from TokyoRentML.pipeline.predict_pipeline import CustomData, PreditPipeline



application = Flask(__name__)
app = application

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            size=float(request.form.get('size')),
            deposit=float(request.form.get('deposit')),
            key_money=float(request.form.get('key_money')),
            year_built=float(request.form.get('year_built')),
            unit_floor=float(request.form.get('unit_floor')),
            total_floors=float(request.form.get('total_floors')),
            nearest_station_distance_in_min=float(request.form.get('nearest_station_distance_in_min'))
        )
        pred_df = data.get_data_as_df()
        print(pred_df)

        predict_pipeline = PreditPipeline()
        results = predict_pipeline.predict(pred_df)
        return render_template('home.html', results=results[0])


if __name__=='__main__':
    app.run(host="0.0.0.0", debug=True)
