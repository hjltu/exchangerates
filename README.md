# exchangerates

## Get currency with exchangerate API:
* test:  
docker run -ti --rm exchangerates /bin/sh -c 'cd exchangerate; pytest get_curr.py'
* run with user's config and database:  
docker run -ti --rm \  
    -v "$PWD"/config_curr.py:/home/check/exchangerate/config.py \  
    -v "$PWD"/data/curr.db:/home/check/data/curr.db  \
    exchangerates /bin/sh -c 'cd exchangerate; python get_curr.py'

* draw with user's config and database:  
chmod 666 data/curr.db  
docker run -ti --rm \  
    -v "$PWD"/config_curr.py:/home/check/exchangerate/config.py \  
    -v "$PWD"/data/curr.db:/home/check/data/curr.db \  
    -v "$PWD"/plots/curr.png:/home/check/plots/curr.png \  
    exchangerates /bin/sh -c 'cd exchangerate; python draw.py'
