# For users from China, please use this mirror site.
# FROM docker.1ms.run/python:3.12-alpine
FROM python:3.12-alpine

# init ash file (for non-login shells)
ENV ENV='$HOME/.ashrc'

# default screen size
ENV XRES=1280x800x24
ENV PYTHONUNBUFFERED=1

# default tzdata settings
ENV TZ=Etc/UTC

# update and install system software
RUN apk update && apk upgrade
RUN apk add --no-cache sudo supervisor openssh-server openssh nano tzdata
RUN apk add --no-cache xvfb x11vnc xauth python3-dev tk
RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing novnc gnome-screenshot
RUN ln -s /usr/share/novnc/vnc.html /usr/share/novnc/index.html

# Minimal xfce4
# RUN apk add libxfce4util thunar xfce4-appfinder xfce4-panel xfce4-whiskermenu-plugin \
# 	xfce4-session xfce4-settings xfce4-terminal xfconf xfdesktop xfwm4 \
# 	adwaita-icon-theme mousepad

# Core xfce4
RUN apk add --no-cache xfce4 xfce4-terminal adwaita-icon-theme mousepad librewolf

# add main user
RUN adduser -D alpine

# change passwords and permissions
RUN	echo "root:alpine" | /usr/sbin/chpasswd \
    && 	echo "alpine:alpine" | /usr/sbin/chpasswd \
    && 	echo "alpine ALL=(ALL) ALL" >> /etc/sudoers

# setup sshd
RUN 	mkdir /run/sshd \
	&& 	ssh-keygen -A

# add my sys config files
ADD etc /etc

# customizations
RUN 	echo "alias ll='ls -l'" > /home/alpine/.ashrc \
	&& 	echo "alias lla='ls -al'" >> /home/alpine/.ashrc \
	&& 	echo "alias llh='ls -hl'" >> /home/alpine/.ashrc \
	&& 	echo "alias hh=history" >> /home/alpine/.ashrc \
	#
	# ash personal config file for login shell mode
	&& cp /home/alpine/.ashrc /home/alpine/.profile

# RUN chown -R alpine:alpine /home/alpine/.config /home/alpine/.xscreensaver
RUN chown -R alpine:alpine /home/alpine/

# Install packages for computer control
RUN pip install fastapi pyautogui uvicorn pillow python-multipart

# add FastAPI server
ADD server /server
RUN touch /home/alpine/.Xauthority
RUN xauth add 127.0.0.1:1 . $(xxd -l 16 -p /dev/urandom)
RUN export DISPLAY=:1

# exposed ports (ssh, novnc, tigervnc)
EXPOSE 22 6080 5900

# default command
CMD ["/usr/bin/supervisord","-c","/etc/supervisord-alpine.conf"]
