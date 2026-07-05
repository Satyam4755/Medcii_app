import frappe
from frappe.website.serve import get_response

def run():
    frappe.set_user("Administrator")
    # This will simulate a web request to /doctor-dashboard
    try:
        response = get_response("/doctor-dashboard")
        print(f"Doctor Dashboard Response Code: {response.status_code}")
    except Exception as e:
        print(f"Doctor Dashboard Error: {e}")
        import traceback
        traceback.print_exc()

    try:
        response = get_response("/patient-dashboard")
        print(f"Patient Dashboard Response Code: {response.status_code}")
    except Exception as e:
        print(f"Patient Dashboard Error: {e}")
        import traceback
        traceback.print_exc()
