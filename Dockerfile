FROM python:2.7

# update sources.list for firefox availability (http://mozilla.debian.net)
RUN echo "deb http://mozilla.debian.net/ jessie-backports firefox-release" >> /etc/apt/sources.list
RUN apt-get update

# firefox - as instructed at: http://mozilla.debian.net/
RUN apt-get -y --force-yes install -t jessie-backports firefox

# pyvirtualdisplay dependencies
RUN apt-get -y --force-yes install xvfb xserver-xephyr

RUN pip install selenium pyvirtualdisplay

RUN mkdir -p /captureapp
ADD capture.py /captureapp

ENTRYPOINT ["python", "/captureapp/capture.py"]
