#!/bin/bash
docker-compose up -d
adb connect localhost:5555
adb install /path/to/hayday.apk