#!/bin/bash
# Run this on the DATABASE SERVER (192.168.108.234)
# Usage: ssh pnc@192.168.108.234 < scripts/deploy_db.sh
#   or: cat scripts/deploy_db.sh | ssh pnc@192.168.108.234

set -e

echo "=== Creating database car_rental_db ==="
mysql -u dba -p'abc123' -e "CREATE DATABASE IF NOT EXISTS car_rental_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u dba -p'abc123' -e "SHOW DATABASES LIKE 'car_rental_db';"

echo "=== Granting privileges to dba ==="
mysql -u dba -p'abc123' -e "GRANT ALL PRIVILEGES ON car_rental_db.* TO 'dba'@'%'; FLUSH PRIVILEGES;"

echo "=== Database ready ==="
