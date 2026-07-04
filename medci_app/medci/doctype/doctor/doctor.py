import frappe
from frappe.model.document import Document


class Doctor(Document):

    def validate(self):
        self.validate_name()
        self.validate_email()
        self.validate_phone()
        self.validate_fee()
        self.validate_experience()

    def before_insert(self):
        # Future: Generate Doctor ID
        pass

    def before_save(self):
        # Future: Additional preprocessing
        pass

    def after_insert(self):
        frappe.logger().info(f"Doctor Created: {self.name}")

    def on_update(self):
        frappe.logger().info(f"Doctor Updated: {self.name}")

    def before_delete(self):
        frappe.logger().info(f"Doctor Deleted: {self.name}")

    # Validation Functions

    def validate_name(self):
        if not self.first_name:
            frappe.throw("First Name is required.")

        self.first_name = self.first_name.strip().title()

        if self.last_name:
            self.last_name = self.last_name.strip().title()

    def validate_email(self):

        if not self.email:
            return

        self.email = self.email.strip().lower()

        exists = frappe.db.exists(
            "Doctor",
            {
                "email": self.email,
                "name": ["!=", self.name]
            }
        )

        if exists:
            frappe.throw("Email already exists.")

    def validate_phone(self):

        if not self.phone_number:
            return

        self.phone_number = self.phone_number.strip()

        if not self.phone_number.isdigit():
            frappe.throw("Phone Number must contain only digits.")

        if len(self.phone_number) != 10:
            frappe.throw("Phone Number must contain exactly 10 digits.")

        exists = frappe.db.exists(
            "Doctor",
            {
                "phone_number": self.phone_number,
                "name": ["!=", self.name]
            }
        )

        if exists:
            frappe.throw("Phone Number already exists.")

    def validate_fee(self):

        if self.consultation_fee is None:
            return

        if self.consultation_fee < 0:
            frappe.throw("Consultation Fee cannot be negative.")

    def validate_experience(self):

        if self.experience is None:
            return

        if self.experience < 0:
            frappe.throw("Experience cannot be negative.")