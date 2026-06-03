#!/bin/bash
# =====================================================
# DATABASE SERVER SETUP
# Target: pnc@dbms  (or pnc@192.168.108.234)
# Password: 1234567
# =====================================================
# Run this on YOUR local machine:
#   scp deploy_db.sh pnc@dbms:~/deploy_db.sh
#   ssh pnc@dbms "bash ~/deploy_db.sh"
# =====================================================

set -e

echo "=== Creating car_rental_db database ==="
mysql -u dba -p'abc123' -e "CREATE DATABASE IF NOT EXISTS car_rental_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo "=== Verify database exists ==="
mysql -u dba -p'abc123' -e "SHOW DATABASES LIKE 'car_rental_db';"

echo "=== Grant privileges ==="
mysql -u dba -p'abc123' -e "GRANT ALL PRIVILEGES ON car_rental_db.* TO 'dba'@'%'; FLUSH PRIVILEGES;"

echo ""
echo "============================================"
echo "  DATABASE READY"
echo "  Host: dbms (192.168.108.234)"
echo "  Database: car_rental_db"
echo "  User: dba"
echo "  Password: abc123"
echo "============================================"
