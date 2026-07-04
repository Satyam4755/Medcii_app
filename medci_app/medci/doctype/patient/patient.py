import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class Patient(Document):

    def validate(self):
        self.validate_name()
        self.validate_email()
        self.validate_phone()
        self.validate_date_of_birth()

    def before_insert(self):
        pass

    def before_save(self):
        pass

    def after_insert(self):
        frappe.logger().info(f"Patient Created: {self.name}")

    def on_update(self):
        frappe.logger().info(f"Patient Updated: {self.name}")

    def before_delete(self):
        frappe.logger().info(f"Patient Deleted: {self.name}")

    # -------------------------------------
    # Validation Functions
    # -------------------------------------

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
            "Patient",
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
            "Patient",
            {
                "phone_number": self.phone_number,
                "name": ["!=", self.name]
            }
        )

        if exists:
            frappe.throw("Phone Number already exists.")

    def validate_date_of_birth(self):

        if not self.date_of_birth:
            return

        if getdate(self.date_of_birth) > getdate():
            frappe.throw("Date of Birth cannot be in the future.")