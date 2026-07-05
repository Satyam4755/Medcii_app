import frappe

def get_permission_query_conditions(user):
    if not user: user = frappe.session.user
    if "System Manager" in frappe.get_roles(user):
        return None
        
    patient = frappe.db.get_value("Patient", {"user": user}, "name")
    doctor = frappe.db.get_value("Doctor", {"user": user}, "name")
    
    conditions = []
    if patient:
        conditions.append(f"patient = '{patient}'")
    if doctor:
        conditions.append(f"doctor = '{doctor}'")
        
    if conditions:
        return "(" + " OR ".join(conditions) + ")"
    return "1=2"

def has_permission(doc, ptype="read", user=None):
    if not user: user = frappe.session.user
    if "System Manager" in frappe.get_roles(user):
        return True
        
    patient = frappe.db.get_value("Patient", {"user": user}, "name")
    doctor = frappe.db.get_value("Doctor", {"user": user}, "name")
    
    if patient and doc.patient == patient: return True
    if doctor and doc.doctor == doctor: return True
    
    return False
