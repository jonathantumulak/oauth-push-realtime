#Tweet Push Notif

This app will send users a stream of push notifications of Tweets which contains the keyword that the 
user subscribed.

##Tech Used
- `Firebase` for multi platform push notification
- `Tweety` a python package for twitter API
- `Bootstrap CSS` - CSS framework for UI/UX
- `Django` - backend server
- `Celery` - task queue for handle push notification when user wants new data (TODO)

##Installation
install the required python packages
```
pip install -r requirements.txt
```

## Run Server
```
python manage.py runserver
```

##HOW TO RUN CELERY
```
python manage.py celeryd --loglevel=DEBUG  -E -B -c 1
```
