import frappe
from frappe.utils import today, add_days

def hourly_cleanup():
    # Expire old requests
    requests = frappe.get_all("Appointment Request", filters={"status": "Pending", "creation": ["<", add_days(today(), -1)]})
    for r in requests:
        frappe.db.set_value("Appointment Request", r.name, "status", "Rejected")
        
    # Auto mark past appointments as Completed
    appointments = frappe.get_all("Appointment", filters={"status": "Scheduled", "appointment_date": ["<", today()]})
    for a in appointments:
        frappe.db.set_value("Appointment", a.name, "status", "Completed")

def daily_reminders():
    # Get tomorrow's appointments
    tomorrow = add_days(today(), 1)
    appointments = frappe.get_all("Appointment", filters={"status": "Scheduled", "appointment_date": tomorrow})
    
    for apt in appointments:
        doc = frappe.get_doc("Appointment", apt.name)
        # Assuming email sending is configured
        pass
