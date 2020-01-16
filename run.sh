#!/bin/sh

docker stop gracio_cityio_backup_instance
docker rm gracio_cityio_backup_instance
docker run --name gracio_cityio_backup_instance -v ~/city_scope_grasbrook/city_io_backups:/app/backups -d gracio_cityio_backup
