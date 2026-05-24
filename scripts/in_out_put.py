import os, csv
from scripts import utils, database

# ===============================================================
# Export CSV functions
# ===============================================================
def export_stores(path=None):
    if path:
        timestamp = utils.format_datetime().strip().replace(" ", "_").replace(":", "-")
        output_file = os.path.join(path, f"tiendas_{timestamp}.csv")
        stores = database.get_all_stores()

        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    "ID",
                    "Nombre de la Tienda",
                    "Numero de Tienda",
                    "Dirección",
                    "Ciudad",
                    "Estado",
                    "Código Postal",
                    "Coordenadas",
                    "Nombre del Contacto",
                    "Teléfono del Contacto",
                    "Correo Electrónico del Contacto",
                    "Notas",
                    "Activo",
                    "Creado En"
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for store in stores:
                    writer.writerow({
                        "ID": store.get("id"),
                        "Nombre de la Tienda": store.get("company_name"),
                        "Numero de Tienda": store.get("store_number"),
                        "Dirección": store.get("address"),
                        "Ciudad": store.get("city"),
                        "Estado": store.get("state"),
                        "Código Postal": store.get("zip"),
                        "Coordenadas": store.get("coordinates"),
                        "Nombre del Contacto": store.get("contact_name"),
                        "Teléfono del Contacto": store.get("contact_phone"),
                        "Correo Electrónico del Contacto": store.get("contact_email"),
                        "Notas": store.get("notes"),
                        "Activo": store.get("active"),
                        "Creado En": store.get("created_at")
                    })
            utils.log_info(f"Exported {len(stores)} stores to {output_file}")
        except Exception as e:
            utils.log_error(f"Error exporting stores: {e}")

def export_services(path=None):
    if path:
        timestamp = utils.format_datetime().strip().replace(" ", "_").replace(":", "-")
        output_file = os.path.join(path, f"servicios_{timestamp}.csv")
        services = database.get_all_services()
    
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    "ID",
                    "Nombre del Servicio",
                    "Precio Predeterminado",
                    "Descripción",
                    "Creado En"
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for service in services:
                    writer.writerow({
                        "ID": service.get("id"),
                        "Nombre del Servicio": service.get("name"),
                        "Precio Predeterminado": service.get("default_price"),
                        "Descripción": service.get("description"),
                        "Creado En": service.get("created_at")
                    })
            utils.log_info(f"Exported {len(services)} services to {output_file}")
        except Exception as e:
            utils.log_error(f"Error exporting services: {e}")

def export_service_records(path=None):
    if path:
        timestamp = utils.format_datetime().strip().replace(" ", "_").replace(":", "-")
        output_file = os.path.join(path, f"registros_de_servicio_{timestamp}.csv")
        records = database.get_all_service_records()
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    "ID",
                    "ID de la Tienda",
                    "ID del Servicio",
                    "Precio",
                    "Frecuencia",
                    "Fecha de Inicio",
                    "Fecha de Fin",
                    "Notas",
                    "Creado En"
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for record in records:
                    writer.writerow({
                        "ID": record.get("record_id"),
                        "ID de la Tienda": record.get("store_id"),
                        "ID del Servicio": record.get("service_id"),
                        "Precio": record.get("price"),
                        "Frecuencia": record.get("frequency"),
                        "Fecha de Inicio": record.get("start_date"),
                        "Fecha de Fin": record.get("end_date"),
                        "Notas": record.get("notes"),
                        "Creado En": record.get("created_at")
                    })
            utils.log_info(f"Exported {len(records)} service records to {output_file}")
        except Exception as e:
            utils.log_error(f"Error exporting service records: {e}")

def export_service_history(path=None):
    if path:
        timestamp = utils.format_datetime().strip().replace(" ", "_").replace(":", "-")
        output_file = os.path.join(path, f"historial_de_servicio_{timestamp}.csv")
        history = database.get_all_service_history()
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    "ID",
                    "ID de la Tienda",
                    "ID del Servicio",
                    "Fecha de Finalización",
                    "Nombre del Trabajador",
                    "Estado",
                    "Monto Cobrado",
                    "Notas",
                    "Ruta de la Foto",
                    "Creado En"
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for entry in history:
                    writer.writerow({
                        "ID": entry.get("history_id"),
                        "ID de la Tienda": entry.get("store_id"),
                        "ID del Servicio": entry.get("service_id"),
                        "Fecha de Finalización": entry.get("date_completed"),
                        "Nombre del Trabajador": entry.get("worker_name"),
                        "Estado": entry.get("status"),
                        "Monto Cobrado": entry.get("amount_charged"),
                        "Notas": entry.get("notes"),
                        "Ruta de la Foto": entry.get("photo_path"),
                        "Creado En": entry.get("created_at")
                    })
            utils.log_info(f"Exported {len(history)} service history entries to {output_file}")
        except Exception as e:
            utils.log_error(f"Error exporting service history: {e}")

def export_image(image_id):
    try:
        image_data = database.get_image(image_id)
        if not image_data:
            utils.log_error(f"No image found with ID {image_id}")
            return
        
        path = utils.request_dir()
        if not path:
            utils.log_info("Image export cancelled by user.")
            return

        filename = f"image_export_{image_id}_{utils.format_datetime().strip().replace(' ', '_').replace(':', '-')}.png"
        output_path = os.path.join(path, filename)

        with open(output_path, 'wb') as img_file:
            img_file.write(image_data)
        
        utils.log_info(f"Exported image ID {image_id} to {output_path}")
    except Exception as e:
        utils.log_error(f"Error exporting image ID {image_id}: {e}")

def export_all_data(exports=set()):
    try:
        if not exports:
            utils.log_info("No data types selected for export.")
            return
        
        path = utils.request_dir()

        if not path:
            utils.log_info("Export cancelled by user.")
            return

        utils.log_info("Exporting data...")
        if "stores" in exports:
            utils.log_info("Exporting stores...")
            export_stores(path)
        if "services" in exports:
            utils.log_info("Exporting services...")
            export_services(path)
        if "service_records" in exports:
            utils.log_info("Exporting service records...")
            export_service_records(path)
        if "service_history" in exports:
            utils.log_info("Exporting service history...")
            export_service_history(path)
        
        utils.log_info("Exported all data successfully.")
    except Exception as e:
        utils.log_error(f"Error exporting all data: {e}")

def backup_database():
    try:
        path = utils.request_dir()
        if not path:
            utils.log_info("Database backup cancelled by user.")
            return
        
        timestamp = utils.format_datetime().strip().replace(" ", "_").replace(":", "-")
        backup_file = os.path.join(path, f"lawn_service_manager_backup_{timestamp}.db")
        os.makedirs(os.path.dirname(backup_file), exist_ok=True)

        database.create_backup(backup_file)
    except Exception as e:
        utils.log_error(f"Error backing up database: {e}")

def import_database():
    try:
        path = utils.request_file()
        if not path:
            utils.log_info("Database import cancelled by user.")
            return
        
        if not os.path.exists(path):
            utils.log_error(f"Selected file does not exist: {path}")
            return

        database.restore_backup(path)
        utils.log_info(f"Database imported successfully from {path}")
    except Exception as e:
        utils.log_error(f"Error importing database: {e}")