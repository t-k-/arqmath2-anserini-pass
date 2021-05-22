#!/bin/sh
cat ${1:-/dev/stdin} | grep 'RunTime' | awk -v ORS="," '{print $10}'
echo ""
