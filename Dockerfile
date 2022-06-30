# docker  build -f Dockerfile -t check .
# docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
# docker run -ti --rm check
# docker run -ti --rm --entrypoint=dir/script.py check

# docker stop check && docker rm check
# docker run -d --restart unless-stopped --name=check -v "$PWD"/config.py:/home/check/dir/config.py check
# docker logs -f check

FROM python:3.8-alpine3.12
LABEL maintainer="hjltu@ya.ru"

RUN apk update && apk add py3-setuptools git && pip3 install requests pytest

ENV USER=check
RUN addgroup -S $USER && adduser -S -G $USER $USER
USER $USER

WORKDIR /home/$USER/
COPY apilayer ./
COPY crypto ./
COPY data ./
COPY exceptions ./
COPY plots ./
COPY tinkoff ./

RUN cd tinkoff && git clone --single-branch -b main https://github.com/hjltu/tinkoff_client

CMD /bin/sh
#ENTRYPOINT [ "python3", "-u", "apilayer/get_curr.py" ]

