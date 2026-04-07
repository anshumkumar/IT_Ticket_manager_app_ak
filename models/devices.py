from database.db import get_db_connection


#Here i am creating class and attributes for devices table in database.

class Device:
    def __init__(self, device_id, device_name, device_type, assigned_to, serial_number, location, last_maintenance_date):
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type
        self.assigned_to = assigned_to
        self.serial_number = serial_number
        self.location = location
        self.last_maintenance_date = last_maintenance_date

    def __repr__(self):
        return (
            f"Device(device_id={self.device_id}, "
            f"device_name='{self.device_name}', "
            f"device_type='{self.device_type}', "
            f"assigned_to={self.assigned_to})"
        )

    # add a new device into the database
    def add_device(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO devices (
                device_name,
                device_type,
                assigned_to,
                serial_number,
                location,
                last_maintenance_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.device_name,
            self.device_type,
            self.assigned_to,
            self.serial_number,
            self.location,
            self.last_maintenance_date
        ))

        self.device_id = cursor.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_devices():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM devices')
        rows = cursor.fetchall()
        conn.close()

        devices = []
        for row in rows:
            devices.append(Device(
                row['device_id'],
                row['device_name'],
                row['device_type'],
                row['assigned_to'],
                row['serial_number'],
                row['location'],
                row['last_maintenance_date']
            ))
        return devices

    @staticmethod
    def get_device_by_id(device_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM devices WHERE device_id = ?', (device_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Device(
                row['device_id'],
                row['device_name'],
                row['device_type'],
                row['assigned_to'],
                row['serial_number'],
                row['location'],
                row['last_maintenance_date']
            )
        return None

    def update_device(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE devices
            SET device_name = ?, device_type = ?, assigned_to = ?, serial_number = ?, location = ?, last_maintenance_date = ?
            WHERE device_id = ?
        ''', (
            self.device_name,
            self.device_type,
            self.assigned_to,
            self.serial_number,
            self.location,
            self.last_maintenance_date,
            self.device_id
        ))

        conn.commit()
        conn.close()

    # for removing device, this removes it from database.

    @staticmethod
    def delete_device(device_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM devices WHERE device_id = ?', (device_id,))
        conn.commit()
        conn.close()