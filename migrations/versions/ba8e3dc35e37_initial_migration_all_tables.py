"""Initial migration: all tables

This is a baseline migration for the existing database.
It creates all 6 tables matching the schema defined in db_config.py.
Uses CREATE TABLE IF NOT EXISTS so it's safe on existing databases.

Revision ID: ba8e3dc35e37
Revises:
Create Date: 2026-06-03 14:08:03.309611

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = 'ba8e3dc35e37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            INDEX idx_email (email),
            INDEX idx_is_active (is_active)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS admin_accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE,
            phone VARCHAR(20),
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            INDEX idx_email (email),
            INDEX idx_is_active (is_active)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            brand VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            year INT NOT NULL,
            category VARCHAR(50) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            image TEXT,
            seats INT NOT NULL,
            transmission VARCHAR(20) NOT NULL,
            fuel_type VARCHAR(30) DEFAULT 'Gasoline',
            engine VARCHAR(50),
            horsepower INT,
            mileage INT DEFAULT 0,
            license_plate VARCHAR(20) UNIQUE,
            vin VARCHAR(50) UNIQUE,
            location VARCHAR(100) DEFAULT 'Main Branch',
            features TEXT,
            color VARCHAR(50),
            doors INT DEFAULT 4,
            luggage_capacity INT DEFAULT 2,
            air_conditioning BOOLEAN DEFAULT TRUE,
            gps BOOLEAN DEFAULT FALSE,
            bluetooth BOOLEAN DEFAULT TRUE,
            backup_camera BOOLEAN DEFAULT FALSE,
            status VARCHAR(20) DEFAULT 'available',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_brand (brand),
            INDEX idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_email VARCHAR(120) NOT NULL,
            user_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20),
            car_id INT NOT NULL,
            car_name VARCHAR(100) NOT NULL,
            car_image TEXT,
            pickup_date DATE NOT NULL,
            return_date DATE NOT NULL,
            days INT NOT NULL,
            base_cost DECIMAL(10, 2) NOT NULL,
            discount_amount DECIMAL(10, 2) DEFAULT 0,
            total_cost DECIMAL(10, 2) NOT NULL,
            discounts_applied TEXT,
            promotion_id INT DEFAULT NULL,
            status VARCHAR(20) DEFAULT 'confirmed',
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_user_email (user_email),
            INDEX idx_car_id (car_id),
            INDEX idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS promotions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(50) UNIQUE NOT NULL,
            description TEXT,
            discount_type ENUM('percentage', 'fixed') NOT NULL DEFAULT 'percentage',
            discount_value DECIMAL(10, 2) NOT NULL,
            active_from DATE,
            active_to DATE,
            max_uses INT DEFAULT NULL,
            uses_count INT DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_code (code),
            INDEX idx_is_active (is_active),
            INDEX idx_active_dates (active_from, active_to)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NULL,
            title VARCHAR(255) NOT NULL,
            message TEXT,
            promotion_id INT NULL,
            is_read TINYINT DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_user_id (user_id),
            INDEX idx_is_read (is_read),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)


def downgrade():
    op.execute("DROP TABLE IF EXISTS notifications")
    op.execute("DROP TABLE IF EXISTS promotions")
    op.execute("DROP TABLE IF EXISTS bookings")
    op.execute("DROP TABLE IF EXISTS cars")
    op.execute("DROP TABLE IF EXISTS admin_accounts")
    op.execute("DROP TABLE IF EXISTS users")
