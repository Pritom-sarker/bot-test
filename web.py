from flask import Flask, render_template
import json
import pandas as pd
import csv

app = Flask(__name__)

results = []
@app.route('/')
def index():
    
    return render_template("table.html",title='Crypto Currency Data',data=results)
    

if __name__ == '__main__':
  
  with open("All Data.csv") as csvfile:
    reader = csv.reader(csvfile) # change contents to floats
    for row in reader: # each row is a list
      results.append(row)
  #print(results)
  app.run(debug=True,host='66.42.118.86',port=80)
