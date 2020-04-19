from flask import Markup, render_template
from app import app
import yaml
import requests
import json
import os
import csv

@app.route('/')
def home():
  raw_data = list(csv.DictReader(open('data.csv'), delimiter=','))

  data = {
    'MindBridge Ai': [],
    'Shopify': [],
  }

  shopify_lead = [(raw_data[0]['Datetime'], 0)]

  for row in raw_data:
    data[row['Team']].append((row['Datetime'], int(row['Credits'])))
    if row['Datetime'] > '2020-04-14 12:30:00':
      shopify_lead.append((row['Datetime'], data['Shopify'][-1][1] - data['MindBridge Ai'][-1][1]))

  diff_data = [i[1] for i in shopify_lead]
  return render_template('home.html', data=data, shopify_lead=shopify_lead, diff_data=diff_data)

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