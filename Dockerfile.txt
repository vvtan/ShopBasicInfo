FROM daocloud.io/mingchuan/isv_service_info_crawler:master-0336b00
MAINTAINER vvtan

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN chmod 755 run.sh
RUN cd /usr/src/app/IsvServiceInfo
RUN cp /etc/localtime /etc/localtime.bak
RUN ln -svf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime


EXPOSE 6800

ENTRYPOINT  ["./run.sh"]

