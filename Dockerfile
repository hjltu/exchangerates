# docker  build -f Dockerfile -t exchangerates .
# docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
# docker run -ti --rm exchangerates
# docker run -ti --rm --entrypoint=dir/script.py exchangerates

# chmod 666 data/file.db
# docker run -ti --rm --restart unless-stopped --name=check -v "$PWD"/config.py:/home/check/dir/config.py exchangerates
# docker run -d --restart unless-stopped --name=check -v "$PWD"/config.py:/home/check/dir/config.py  -v "$PWD"/data/file.db:/home/check/data/dile.db exchangerates /bin/sh -c 'cd dir; python service.py'
# docker stop exchangerates && docker rm exchangerates
# docker logs -f exchangerates
# chmod 666 data/file.png
# docker run --rm -v "$PWD"/config_user.py:/home/check/exchangerates/dir/config.py -v "$PWD"/data/curr.db:/home/check/exchangerates/data/curr.db -v "$PWD"/plots/file.png:/home/check/exchangerates/plots/file.png exchangerates /bin/sh -c 'cd dir; python draw.py'

FROM python:3.8-alpine3.12
LABEL maintainer="hjltu@ya.ru"

RUN apk update && \
    apk add python3-dev py3-setuptools build-base git
RUN pip3 install -U pip 
RUN pip3 install -U requests pytest tabulate matplotlib

ENV USER=check
RUN addgroup -S $USER && adduser -S -G $USER $USER

WORKDIR /home/$USER
#RUN cd /home/$USER && git clone --single-branch -b master https://github.com/hjltu/exchangerates.git
COPY . .
RUN chown $USER:$USER *
USER $USER

#WORKDIR /home/$USER/exchangerates

RUN cd tinkoff && git clone --single-branch -b main https://github.com/hjltu/tinkoff_client

CMD /bin/sh
#ENTRYPOINT [ "python3", "-u", "apilayer/get_curr.py" ]

