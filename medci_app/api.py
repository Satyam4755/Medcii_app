import frappe
from frappe import _
from frappe.utils import add_days, getdate, get_time, today, nowdate

@frappe.whitelist(allow_guest=True)
def register_user(full_name, email, password, role):
    if frappe.db.exists("User", email):
        frappe.throw(_("User with this email already exists"))

    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": full_name,
        "send_welcome_email": 0
    })
    user.insert(ignore_permissions=True)
    
    # Set password securely
    from frappe.utils.password import update_password
    update_password(user=email, pwd=password)
    
    if role == "Patient":
        if not frappe.db.exists("Patient", {"email": email}):
            patient = frappe.get_doc({
                "doctype": "Patient",
                "first_name": full_name.split()[0],
                "last_name": " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else "Unknown",
                "email": email,
                "gender": "Prefer not to say",
                "user": email
            })
            patient.insert(ignore_permissions=True)
    elif role == "Doctor":
        if not frappe.db.exists("Doctor", {"email": email}):
            doctor = frappe.get_doc({
                "doctype": "Doctor",
                "doctor_id": frappe.generate_hash(length=8),
                "first_name": full_name.split()[0],
                "last_name": " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else "Unknown",
                "email": email,
                "phone_number": "0000000000",
                "profile_photo": "/assets/frappe/images/default-avatar.png",
                "gender": "Prefer not to say",
                "date_of_birth": "1990-01-01",
                "specialization": "General Physician",
                "qualification": "MBBS",
                "medical_license_number": "PENDING",
                "consultation_fee": 500,
                "experience": 1,
                "availability_status": "Available",
                "user": email
            })
            doctor.insert(ignore_permissions=True)
        
    return "Success"

@frappe.whitelist()
def get_available_slots(doctor, date):
    # Fetch doctor details
    doc = frappe.get_doc("Doctor", doctor)
    
    # Simple logic: 9 AM to 5 PM, every 30 mins
    start_time = doc.start_time or "09:00:00"
    end_time = doc.end_time or "17:00:00"
    
    from datetime import datetime, timedelta
    
    dt_start = datetime.strptime(str(start_time), "%H:%M:%S")
    dt_end = datetime.strptime(str(end_time), "%H:%M:%S")
    
    slots = []
    current = dt_start
    while current < dt_end:
        slots.append(current.strftime("%H:%M:%S"))
        current += timedelta(minutes=30)
        
    # Exclude booked slots
    booked = frappe.get_all("Appointment", filters={"doctor": doctor, "appointment_date": date, "status": ["!=", "Cancelled"]}, pluck="appointment_time")
    booked = [str(b) for b in booked]
    
    # Exclude pending requests
    pending = frappe.get_all("Appointment Request", filters={"doctor": doctor, "appointment_date": date, "status": "Pending"}, pluck="appointment_time")
    pending = [str(p) for p in pending]
    
    # Remove booked/pending from slots
    def time_match(t1, list_t):
        for lt in list_t:
            if t1[:5] == lt[:5]:
                return True
        return False
        
    available = [s for s in slots if not time_match(s, booked) and not time_match(s, pending)]
    
    # If date is today, remove past slots
    if getdate(date) == getdate(today()):
        now_time = datetime.now().time()
        available = [s for s in available if datetime.strptime(s, "%H:%M:%S").time() > now_time]
        
    return available

@frappe.whitelist()
def submit_appointment_request(doctor, date, time, reason):
    patient = frappe.db.get_value("Patient", {"user": frappe.session.user}, "name")
    if not patient:
        frappe.throw(_("You must be registered as a Patient to book an appointment."))
        
    # Check if slot is still free
    available = get_available_slots(doctor, date)
    if time not in available:
        frappe.throw(_("This slot is no longer available."))
        
    req = frappe.get_doc({
        "doctype": "Appointment Request",
        "patient": patient,
        "doctor": doctor,
        "appointment_date": date,
        "appointment_time": time,
        "reason": reason,
        "status": "Pending"
    })
    req.insert(ignore_permissions=True)
    return req.name

@frappe.whitelist()
def process_appointment_request(request_id, action):
    req = frappe.get_doc("Appointment Request", request_id)
    
    # Check permissions
    doctor_name = frappe.db.get_value("Doctor", {"user": frappe.session.user}, "name")
    if req.doctor != doctor_name:
        frappe.throw(_("Not authorized."))
        
    if action == "Accept":
        req.db_set("status", "Accepted")
        
        # Create Appointment
        apt = frappe.get_doc({
            "doctype": "Appointment",
            "patient": req.patient,
            "doctor": req.doctor,
            "appointment_date": req.appointment_date,
            "appointment_time": req.appointment_time,
            "status": "Scheduled"
        })
        apt.insert(ignore_permissions=True)
        return {"status": "Accepted", "appointment": apt.name}
    elif action == "Reject":
        req.db_set("status", "Rejected")
        return {"status": "Rejected"}

@frappe.whitelist()
def get_login_redirect():
    if "System Manager" in frappe.get_roles():
        return "/app"
    
    if frappe.db.exists("Doctor", {"user": frappe.session.user}):
        return "/doctor-dashboard"
        
    return "/patient-dashboard"
