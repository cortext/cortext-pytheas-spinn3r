# Pytheas_Spinn3r
Simple web interface to download data from spinn3r (with credentials) in json/csv and simple/advanced mode.

## based on :
- flask
- requests

## next to do : 
* date in simple mode
* documentation
* see about other elasticsearch webInterfaces
* others apis from spinn3r

## how to use ? 
### with docker and docker-compose

1. first git clone this repo
``` 
git clone --recursive https://github.com/cortext/simple-tweet-web-extract.git
```

2. create docker-compose.yaml && conf/conf.json (with credentials) from example files

3. run docker
```
docker build -t cortext/cortext_pytheas . && docker-compose up 
```


### with virtualenv and python 

1. Locally you can also more easily (and to debug principaly) directly create a virtualenv with python 3.x
```
virtualenv env3 -p /usr/bin/python3 && source ./env3/bin/activate
```

2. Then install dependancies :
``` 
pip install -r requirements.txt
git clone https://github.com/ikario404/twitterscraper.git
cd twitterscraper && python setup.py install && cd ..
```

3. Finally :
``` 
python app.py
```
