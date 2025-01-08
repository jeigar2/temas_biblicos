#!/bin/bash

URL=$1

for i in {1..10}; do
  lynx -dump -listonly $URL | grep -m 6 -o 'https.*\.HTM' | xargs lynx -dump -listonly
done
