import frappe
from frappe.utils.jinja import get_jenv

def run():
    jenv = get_jenv()
    frappe.msgprint("Jinja Env setup")
    
    # Check if frappe.db.exists is exposed
    db_obj = jenv.globals.get('frappe', {}).get('db', {})
    
    msg = ""
    if 'exists' in db_obj:
        msg += "frappe.db.exists is AVAILABLE.\n"
    else:
        msg += "frappe.db.exists is MISSING.\n"
        
    if 'count' in db_obj:
        msg += "frappe.db.count is AVAILABLE.\n"
    else:
        msg += "frappe.db.count is MISSING.\n"
        
    print(msg)
