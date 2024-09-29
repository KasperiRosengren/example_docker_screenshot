FROM python:3.12-bullseye

RUN apt-get update && apt-get install -y \
    xvfb \
    x11-apps \
    x11-utils \
    scrot \
    xfonts-base \
    python3-dev \
    python3-pip \
    krita \
    gnome-screenshot \
    gimp \
    wmctrl \
    xdotool \
    colord \
    && apt-get clean

RUN apt-get update && apt-get install -y \
    fluxbox \
    && apt-get clean

#openbox

RUN pip install pyautogui pillow pywinctl opencv-python-headless

WORKDIR /app

COPY ./app /app
#COPY ./configs/rc.xml /root/.config/openbox/rc.xml
COPY ./configs/fluxbox_init /root/.fluxbox/init

ENV XAUTHORITY=/dev/null
ENV DISPLAY=:99

CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x16 & fluxbox & python3 main.py --screenshots-dir ./screenshots"]
#CMD ["sh", "-c", 'xvfb-run --server-args="-screen 0 1920x1080x16" & python3 main.py --screenshots-dir ./screenshots']