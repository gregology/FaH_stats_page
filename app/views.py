from flask import Markup, render_template
from app import app
import yaml
import requests
import json
import os
import csv

@app.route('/')
def home():

  a = csv.DictReader(open('data.csv'), delimiter=',')
  data = [x for x in a]

  data_points = {
    'MindBridge Ai': '',
    'Shopify': '',
  }

  for point in data:
    data_points[point['Team']] += f"{{t: new Date('{point['Datetime']}'), y: {point['Credits']}}},"

  return render_template('home.html', data_points=data_points)
  return "hello world!"

@app.route('/extract')
def extract():
  with open(r'app/teams.yml') as file:
    teams = yaml.load(file, Loader=yaml.FullLoader)

  exists = os.path.isfile('data.csv')
  file_progress = open('data.csv', 'a')
  if not exists:
      file_progress.write("Datetime,Team,Credits\r\n")

  for team in teams:
    r = requests.get(f"https://stats.foldingathome.org/api/team/{team['id']}")
    data = json.loads(r.text)
    file_progress.write(f"{data['last']},{team['name']},{data['credit'] - team['starting_score']}\r\n")

  return "extracted!"