import frappe

def create_doctype():
    if not frappe.db.exists("DocType", "Appointment Request"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Appointment Request",
            "module": "Medci",
            "custom": 1,
            "naming_rule": "By \"Naming Series\" field",
            "autoname": "REQ-.YYYY.-.#####",
            "fields": [
                {"fieldname": "patient", "fieldtype": "Link", "options": "Patient", "label": "Patient", "reqd": 1, "in_list_view": 1},
                {"fieldname": "doctor", "fieldtype": "Link", "options": "Doctor", "label": "Doctor", "reqd": 1, "in_list_view": 1},
                {"fieldname": "appointment_date", "fieldtype": "Date", "label": "Date", "reqd": 1, "in_list_view": 1},
                {"fieldname": "appointment_time", "fieldtype": "Time", "label": "Time", "reqd": 1, "in_list_view": 1},
                {"fieldname": "reason", "fieldtype": "Small Text", "label": "Reason"},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Pending\nAccepted\nRejected", "default": "Pending", "in_list_view": 1},
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Appointment Request DocType created successfully.")
    else:
        print("Appointment Request DocType already exists.")
