from eve import Eve

app = Eve(settings='settings.py')
app.run(port=8085, host='0.0.0.0')