FROM nginx/unit:1.29.1-python3.11

COPY nginx-unit/config/requirements.txt /config/requirements.txt

# PIP isn't installed by default, so we install it first.
# Next, we install the requirements, remove PIP, and perform image cleanup.
RUN apt update && apt install -y python3-pip vim curl lsof                    \
    && pip3 install -r /config/requirements.txt                               \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

RUN mkdir -p           /var/log/quota
RUN chown -R unit:unit /var/log/quota
RUN chmod -R 777       /var/log/quota

EXPOSE 8000
