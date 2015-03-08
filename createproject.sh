#!/bin/bash

read -p "Enter project name: " name

scriptpath=$(cd $(dirname $0); pwd -P)

python "$scriptpath/createproject.py" "$name"