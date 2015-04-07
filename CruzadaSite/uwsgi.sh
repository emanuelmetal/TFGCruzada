#!/bin/bash

BASEDIR=$( cd $(dirname $0) ; pwd)
echo $BASEDIR
if [ -z "$VIRTUAL_ENV" -a -d $BASEDIR/../virtualenv ] ; then
        . $BASEDIR/../virtualenv/bin/activate
fi

cd $BASEDIR

uwsgi --module=CruzadaSite.wsgi:application \
--env DJANGO_SETTINGS_MODULE=CruzadaSite.settings \
--master --processes=1 --enable-threads \
--home=${VIRTUAL_ENV} --socket=127.0.0.1:8001 \
--python-path=${BASEDIR} \
--static-map /static=${BASEDIR}/Cruzada/static
