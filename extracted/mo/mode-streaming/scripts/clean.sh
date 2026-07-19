#!/bin/sh -e

if [ -d 'dist' ] ; then
    rm -r dist
fi
if [ -d 'site' ] ; then
    rm -r site
fi
if [ -d 'htmlcov' ] ; then
    rm -r htmlcov
fi
if [ -d 'mode_streaming.egg-info' ] ; then
    rm -r mode_streaming.egg-info
fi

# delete python cache
find . -iname '*.pyc' -delete
find . -iname '__pycache__' -delete

rm -rf .coverage.*
rm -rf *.logs
