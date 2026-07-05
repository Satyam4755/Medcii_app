import frappe

def get_context(context):
    # Fetch doctors ignoring permissions so that Guests can view the doctors page
    context.doctors = frappe.get_all(
        "Doctor",
        fields=["name", "first_name", "last_name", "specialization", "qualification", "experience", "consultation_fee", "availability_status", "profile_photo"],
        ignore_permissions=True
    )
    
    # Fetch default currency safely
    context.currency = frappe.defaults.get_global_default("currency") or "$"
