import os, sqlite3
from scripts import utils

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self): # Establishes a connection to the SQLite database.
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, params=()): # Executes a query that modifies data (INSERT/UPDATE/DELETE)
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
                
        except sqlite3.Error as e:
            utils.log_error(f" > Database error: {e}")
            return None

    def fetch_all(self, query, params=()): # Fetches all results for a SELECT query. Returns a list of tuples.
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            utils.log_error(f" > Database error: {e}")
            return []

    def create_table(self, table_name, schema): # schema should be a string like "id INTEGER PRIMARY KEY, name TEXT"
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});"
            self.execute_query(query)
        except sqlite3.Error as e:
            utils.log_error(f" > Error creating table {table_name}: {e}")

db = None 

collumn_cache = {}

def get_columns(table_name):
    if table_name in collumn_cache:
        return collumn_cache[table_name]
    try:
        global db
        if db is None:
            utils.log_error("Database not initialized. Cannot get columns.")
            return []
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            columns = [col[1] for col in columns]
            collumn_cache[table_name] = columns
            return columns
    except sqlite3.Error as e:
        utils.log_error(f" > Database error: {e}")
        return []

def convert_row_to_dict(row, columns):
    return {columns[i]: row[i] for i in range(len(columns))}

# =====================================================
# Database Functions
# =====================================================
def initialize_database(db_path):
    try:
        global db
        print(f"Initializing database at: {db_path}")
        db = DatabaseManager(db_path) # Create database if it doesn't exist. This will be used to store connection data.
        
        if not os.path.exists(db_path):
            # Creates a table for Store Connections
            db.create_table('stores', '''
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                store_number INTEGER NOT NULL,
                address TEXT,
                city TEXT,
                state TEXT,
                zip INTEGER,
                coordinates TEXT,
                contact_name TEXT,
                contact_phone TEXT,
                contact_email TEXT,
                notes TEXT,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ''')

            # Creates a table for Services offered by the lawn service company
            db.create_table('services', '''
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                default_price REAL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ''')

            # Creates a table for Service Records, which will link to the stores and services tables
            db.create_table('service_records', '''
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                price REAL,
                frequency TEXT,
                start_date DATE,
                end_date DATE,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ''')

            # Creates a table for service history, which will log each time a service is performed at a store
            db.create_table('service_history', '''
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                date_completed DATE,
                worker_name TEXT,
                status TEXT,
                amount_charged REAL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ''')

            db.create_table('images', '''
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                history_id INTEGER NOT NULL,
                file BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ''')

            db._get_connection().execute('PRAGMA journal_mode=WAL;')
            journal_mode = db._get_connection().execute('PRAGMA journal_mode').fetchone()[0]
            utils.log_info(f" > Journal mode set to: {journal_mode}")
            utils.log_info(f"Database created at: {db_path}")
        else:
            utils.log_info(f"Database already exists at: {db_path}")

        return True
    except Exception as e:
        utils.log_error(f" > Error creating database: {str(e)}")
        return False

def delete_database(db_path):
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
            utils.log_info(f"Database deleted at: {db_path}")
        else:
            utils.log_info(f"No database found at: {db_path}")
    except Exception as e:
        utils.log_error(f" > Error deleting database: {str(e)}")

# =====================================================
# Count functions
# =====================================================
def get_store_count():
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get store count.")
            return 0
        query = "SELECT COUNT(*) FROM stores"
        result = db.fetch_all(query)
        count = result[0][0] if result else 0
        utils.log_debug(f" > Retrieved store count: {count}")
        return count
    except Exception as e:
        utils.log_error(f" > Error getting store count: {str(e)}")
        return 0

def get_service_count():
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get service count.")
            return 0
        query = "SELECT COUNT(*) FROM services"
        result = db.fetch_all(query)
        count = result[0][0] if result else 0
        utils.log_debug(f" > Retrieved service count: {count}")
        return count
    except Exception as e:
        utils.log_error(f" > Error getting service count: {str(e)}")
        return 0

def get_active_services():
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get total active services.")
            return 0
        query = "SELECT COUNT(*) FROM service_records WHERE end_date >= DATE('now')"
        result = db.fetch_all(query)
        count = result[0][0] if result else 0
        utils.log_debug(f" > Retrieved total active services: {count}")
        return count
    except Exception as e:
        utils.log_error(f" > Error getting total active services: {str(e)}")
        return 0

def get_active_store_services(store_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get active services for store.")
            return 0
        query = "SELECT COUNT(*) FROM service_records WHERE store_id = ? AND end_date >= DATE('now')"
        params = (store_id,)
        result = db.fetch_all(query, params)
        count = result[0][0] if result else 0
        utils.log_debug(f" > Retrieved active services for store ID {store_id}: {count}")
        return count
    except Exception as e:
        utils.log_error(f" > Error getting active services for store ID {store_id}: {str(e)}")
        return 0

def get_services_completed():
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get total services completed.")
            return 0
        query = "SELECT COUNT(*) FROM service_history"
        result = db.fetch_all(query)
        count = result[0][0] if result else 0
        utils.log_debug(f" > Retrieved total services completed: {count}")
        return count
    except Exception as e:
        utils.log_error(f" > Error getting total services completed: {str(e)}")
        return 0

def get_services_completed_month():
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get total services completed this month.")
            return 0
        query = "SELECT COUNT(*) FROM service_history WHERE strftime('%Y-%m', date_completed) = strftime('%Y-%m', 'now')"
        result = db.fetch_all(query)
        count = result[0][0] if result else 0
        utils.log_debug(f" > Retrieved total services completed this month: {count}")
        return count
    except Exception as e:
        utils.log_error(f" > Error getting total services completed this month: {str(e)}")
        return 0

def get_services_completed_year():
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get total services completed this year.")
            return 0
        query = "SELECT COUNT(*) FROM service_history WHERE strftime('%Y', date_completed) = strftime('%Y', 'now')"
        result = db.fetch_all(query)
        count = result[0][0] if result else 0
        utils.log_debug(f" > Retrieved total services completed this year: {count}")
        return count
    except Exception as e:
        utils.log_error(f" > Error getting total services completed this year: {str(e)}")
        return 0

# =====================================================
# Store functions
# =====================================================
def add_store(store_data):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot add store.")
            return None
        query = '''
            INSERT INTO stores (company_name, store_number, address, city, state, zip, coordinates, contact_name, contact_phone, contact_email, notes, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            store_data.get('company_name'),
            store_data.get('store_number'),
            store_data.get('address'),
            store_data.get('city'),
            store_data.get('state'),
            store_data.get('zip'),
            store_data.get('coordinates'),
            store_data.get('contact_name'),
            store_data.get('contact_phone'),
            store_data.get('contact_email'),
            store_data.get('notes'),
            store_data.get('active', 1)
        )

        utils.log_info(f" > Adding store with data: {store_data}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error adding store: {str(e)}")
        return None

def update_store(store_id, update_data):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot update store.")
            return None
        set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
        query = f"UPDATE stores SET {set_clause} WHERE id = ?"
        params = list(update_data.values()) + [store_id]

        utils.log_info(f" > Updating store with ID {store_id} using data: {update_data}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error updating store with ID {store_id}: {str(e)}")
        return None

def delete_store(store_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot delete store.")
            return None
        query = "DELETE FROM stores WHERE id = ?"
        params = (store_id,)

        utils.log_info(f" > Deleting store with ID: {store_id}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error deleting store with ID {store_id}: {str(e)}")
        return None

def get_store(store_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get store.")
            return None
        query = "SELECT * FROM stores WHERE id = ?"
        params = (store_id,)
        results = db.fetch_all(query, params)
        columns = get_columns('stores')
        
        if results and columns:
            results = [convert_row_to_dict(row, columns) for row in results]

        utils.log_info(f" > Retrieved store with ID {store_id}: {results[0] if results else 'None'}")
        return results[0] if results else None
    except Exception as e:
        utils.log_error(f" > Error getting store with ID {store_id}: {str(e)}")
        return None

def get_all_stores():
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get stores.")
            return []
        query = "SELECT * FROM stores"
        results = db.fetch_all(query)
        columns = get_columns('stores')
        
        if results and columns:
            results = [convert_row_to_dict(row, columns) for row in results]

        utils.log_debug(f" > Retrieved all stores: {results}")
        return results
    except Exception as e:
        utils.log_error(f" > Error getting all stores: {str(e)}")
        return []

# =====================================================
# Service functions
# =====================================================
def add_service(service_data):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot add service.")
            return None
        query = '''
            INSERT INTO services (name, default_price, description)
            VALUES (?, ?, ?)
        '''
        params = (
            service_data.get('name'),
            service_data.get('default_price'),
            service_data.get('description')
        )

        utils.log_info(f" > Adding service with data: {service_data}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error adding service: {str(e)}")
        return None

def update_service(service_id, update_data):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot update service.")
            return None
        set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
        query = f"UPDATE services SET {set_clause} WHERE id = ?"
        params = list(update_data.values()) + [service_id]

        utils.log_info(f" > Updating service with ID {service_id} using data: {update_data}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error updating service with ID {service_id}: {str(e)}")
        return None

def delete_service(service_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot delete service.")
            return None
        query = "DELETE FROM services WHERE id = ?"
        params = (service_id,)

        utils.log_info(f" > Deleting service with ID {service_id}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error deleting service with ID {service_id}: {str(e)}")
        return None

def get_service(service_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get service.")
            return None
        query = "SELECT * FROM services WHERE id = ?"
        params = (service_id,)
        results = db.fetch_all(query, params)
        columns = get_columns('services')

        if results and columns:
            results = [convert_row_to_dict(row, columns) for row in results]
        
        utils.log_debug(f" > Retrieved service with ID {service_id}: {results[0] if results else 'None'}")
        return results[0] if results else None
    except Exception as e:
        utils.log_error(f" > Error getting service with ID {service_id}: {str(e)}")
        return None

def get_services_by_name(name):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get services by name.")
            return []
        query = "SELECT * FROM services WHERE name LIKE ?"
        params = (f"%{name}%",)
        results = db.fetch_all(query, params)
        columns = get_columns('services')

        if results and columns:
            results = [convert_row_to_dict(row, columns) for row in results]
        
        utils.log_debug(f" > Retrieved services by name '{name}': {results}")
        return results
    except Exception as e:
        utils.log_error(f" > Error getting services by name '{name}': {str(e)}")
        return []

def get_next_service_date(store_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get next service date.")
            return None
        query = '''
            SELECT sr.start_date 
            FROM service_records sr
            WHERE sr.store_id = ?
            ORDER BY sr.start_date ASC
            LIMIT 1
        '''
        params = (store_id,)
        results = db.fetch_all(query, params)

        utils.log_debug(f" > Retrieved next service date for store ID {store_id}: {results[0][0] if results else 'None'}")
        return results[0][0] if results else None
    except Exception as e:
        utils.log_error(f" > Error getting next service date for store ID {store_id}: {str(e)}")
        return None

def get_all_services():
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get services.")
            return []
        query = "SELECT * FROM services"
        results = db.fetch_all(query)
        columns = get_columns('services')

        if results and columns:
            results = [convert_row_to_dict(row, columns) for row in results]

        utils.log_debug(f" > Retrieved all services: {results}")
        return results
    except Exception as e:
        utils.log_error(f" > Error getting all services: {str(e)}")
        return []

# =====================================================
# Service Record functions
# =====================================================
def add_service_record(record_data):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot add service record.")
            return None
        query = '''
            INSERT INTO service_records (store_id, service_id, price, frequency, start_date, end_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            record_data.get('store_id'),
            record_data.get('service_id'),
            record_data.get('price'),
            record_data.get('frequency'),
            record_data.get('start_date'),
            record_data.get('end_date'),
            record_data.get('notes')
        )

        utils.log_info(f" > Adding service record with data: {record_data}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error adding service record: {str(e)}")
        return None

def update_service_record(record_id, update_data):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot update service record.")
            return None
        set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
        query = f"UPDATE service_records SET {set_clause} WHERE id = ?"
        params = list(update_data.values()) + [record_id]

        utils.log_info(f" > Updating service record with ID {record_id} using data: {update_data}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error updating service record with ID {record_id}: {str(e)}")
        return None

def delete_service_record(record_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot delete service record.")
            return None
        query = "DELETE FROM service_records WHERE id = ?"
        params = (record_id,)

        utils.log_info(f" > Deleting service record with ID: {record_id}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error deleting service record with ID {record_id}: {str(e)}")
        return None

def get_service_record(record_id):
    try:    
        if db is None:
            utils.log_error("Database not initialized. Cannot get service record.")
            return None
        query = "SELECT * FROM service_records WHERE id = ?"
        params = (record_id,)
        results = db.fetch_all(query, params)
        columns = get_columns('service_records')
        
        if results and columns:
            results = [convert_row_to_dict(row, columns) for row in results]
        
        utils.log_debug(f" > Retrieved service record with ID {record_id}: {results[0] if results else 'None'}")
        return results[0] if results else None
    except Exception as e:
        utils.log_error(f" > Error getting service record with ID {record_id}: {str(e)}")
        return None

def get_all_service_records(store_id=None):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get service records.")
            return []
        query = "SELECT * FROM service_records"
        params = ()
        if store_id is not None:
            query += " WHERE store_id = ?"
            params = (store_id,)
        results = db.fetch_all(query, params)
        columns = get_columns('service_records')

        if results and columns:
            results = [convert_row_to_dict(row, columns) for row in results]

        utils.log_debug(f" > Retrieved service records for store ID {store_id if store_id else 'ALL'}: {results}")
        return results
    except Exception as e:
        utils.log_error(f" > Error getting service records: {str(e)}")
        return []

# =====================================================
# Service History functions
# =====================================================
def add_service_history(history_data):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot add service history.")
            return None

        query = '''
            INSERT INTO service_history (store_id, service_id, date_completed, worker_name, status, amount_charged, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            history_data.get('store_id'),
            history_data.get('service_id'),
            history_data.get('date_completed'),
            history_data.get('worker_name'),
            history_data.get('status'),
            history_data.get('amount_charged'),
            history_data.get('notes')
        )
        
        utils.log_info(f" > Adding service history with data: {history_data}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error adding service history: {str(e)}")
        return None

def update_service_history(history_id, update_data):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot update service history.")
            return None
        set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
        query = f"UPDATE service_history SET {set_clause} WHERE id = ?"
        params = list(update_data.values()) + [history_id]

        utils.log_info(f" > Updating service history with ID {history_id} using data: {update_data}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error updating service history with ID {history_id}: {str(e)}")
        return None

def delete_service_history(history_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot delete service history.")
            return None
        query = "DELETE FROM service_history WHERE id = ?"
        params = (history_id,)

        utils.log_info(f" > Deleting service history with ID: {history_id}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error deleting service history with ID {history_id}: {str(e)}")
        return None

def get_service_history(history_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get service history.")
            return None
        query = "SELECT * FROM service_history WHERE id = ?"
        params = (history_id,)
        results = db.fetch_all(query, params)
        columns = get_columns('service_history')
        
        if results and columns:
            results = [convert_row_to_dict(row, columns) for row in results]

        utils.log_debug(f" > Retrieved service history with ID {history_id}: {results[0] if results else 'None'}")
        return results[0] if results else None
    except Exception as e:
        utils.log_error(f" > Error getting service history with ID {history_id}: {str(e)}")
        return None

def get_all_service_history(store_id=None):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get service history.")
            return []
        query = "SELECT * FROM service_history"
        params = ()
        if store_id is not None:
            query += " WHERE store_id = ?"
            params = (store_id,)
        results = db.fetch_all(query, params)
        columns = get_columns('service_history')

        if results and columns:
            results = [convert_row_to_dict(row, columns) for row in results]

        utils.log_debug(f" > Retrieved service history for store ID {store_id if store_id else 'ALL'}: {results}")
        return results
    except Exception as e:
        utils.log_error(f" > Error getting service history: {str(e)}")
        return []
    
def clear_all_service_history():
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot clear service history.")
            return None
        query = "DELETE FROM service_history"
        utils.log_info(" > Clearing all service history records.")
        return db.execute_query(query)
    except Exception as e:
        utils.log_error(f" > Error clearing service history: {str(e)}")
        return None
    
# =====================================================
# Image functions
# =====================================================
def add_image(history_id, photo_path):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot add image.")
            return None
        query = '''
            INSERT INTO images (history_id, file)
            VALUES (?, ?)
        '''
        with open(photo_path, 'rb') as f:
            file_data = f.read()
        params = (history_id, file_data)

        utils.log_info(f" > Adding image for history ID {history_id} from path: {photo_path}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error adding image for history ID {history_id}: {str(e)}")
        return None

def delete_image(image_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot delete image.")
            return None
        query = "DELETE FROM images WHERE id = ?"
        params = (image_id,)

        utils.log_info(f" > Deleting image with ID: {image_id}")
        return db.execute_query(query, params)
    except Exception as e:
        utils.log_error(f" > Error deleting image with ID {image_id}: {str(e)}")
        return None

def get_image(image_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get image.")
            return None
        query = "SELECT file FROM images WHERE id = ?"
        params = (image_id,)
        results = db.fetch_all(query, params)
        
        utils.log_debug(f" > Retrieved image with ID {image_id}: {'Found' if results else 'None'}")
        return results[0][0] if results else None
    except Exception as e:
        utils.log_error(f" > Error getting image with ID {image_id}: {str(e)}")
        return None

def get_images_by_history_id(history_id):
    try:
        if db is None:
            utils.log_error("Database not initialized. Cannot get images.")
            return []
        query = "SELECT * FROM images WHERE history_id = ?"
        params = (history_id,)
        results = db.fetch_all(query, params)
        columns = get_columns('images')
        if results and columns:
            results = [convert_row_to_dict(row, columns) for row in results]
        
        utils.log_debug(f" > Retrieved images for history ID {history_id}: {results if results else 'None'}")
        return results
    except Exception as e:
        utils.log_error(f" > Error getting images for history ID {history_id}: {str(e)}")
        return []