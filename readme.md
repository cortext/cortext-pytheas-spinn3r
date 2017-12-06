# Pytheas_tweet
Simple web interface to download data from Spinn3r

## based on :
- requests
- flask

## next to do : 
* processing db 
* enhance method from docker
* finish template
* lot of things

## how to use ? 
### with docker and docker-compose

1. first git clone this repo
``` 
git clone https://github.com/ikario404/spinn3r-data-extract.git
```

2. run docker
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

```

3. Finally :
``` 
python app.py

```
