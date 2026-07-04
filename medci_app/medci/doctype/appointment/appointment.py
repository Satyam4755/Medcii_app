# Copyright (c) 2026, Satyam and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, get_time


class Appointment(Document):

    # --------------------------
    # Main Validation
    # --------------------------

    def validate(self):
        self.validate_patient()
        self.validate_doctor()
        self.validate_appointment_date()
        self.validate_payment()
        self.calculate_total_amount()

    def before_insert(self):
        pass

    def before_save(self):
        self.validate_doctor_availability()

    def after_insert(self):
        frappe.logger().info(f"Appointment Created: {self.name}")

    def on_update(self):
        frappe.logger().info(f"Appointment Updated: {self.name}")

    def before_delete(self):
        frappe.logger().info(f"Appointment Deleted: {self.name}")

    # --------------------------
    # Validation Functions
    # --------------------------

    def validate_patient(self):

        if not self.patient:
            frappe.throw("Please select a Patient.")

        if not frappe.db.exists("Patient", self.patient):
            frappe.throw("Selected Patient does not exist.")

    def validate_doctor(self):

        if not self.doctor:
            frappe.throw("Please select a Doctor.")

        if not frappe.db.exists("Doctor", self.doctor):
            frappe.throw("Selected Doctor does not exist.")

    def validate_appointment_date(self):

        if not self.appointment_date:
            return

        if getdate(self.appointment_date) < getdate(nowdate()):
            frappe.throw("Appointment Date cannot be in the past.")

    def validate_payment(self):

        if self.status == "Completed" and self.payment_status != "Done":
            frappe.throw(
                "Payment must be completed before completing the appointment."
            )

        if self.payment_status == "Done":

            if not self.payment_method:
                frappe.throw("Please select Payment Method.")

            if not self.payment_date:
                self.payment_date = nowdate()

    def calculate_total_amount(self):

        self.total_amount = self.consultation_fee or 0

    def validate_doctor_availability(self):

        if not self.doctor or not self.appointment_time:
            return

        doctor = frappe.get_doc("Doctor", self.doctor)

        # Replace these field names if your Doctor DocType uses different names
        doctor_start_time = doctor.start_time
        doctor_end_time = doctor.end_time

        if (
            doctor_start_time
            and get_time(self.appointment_time) < get_time(doctor_start_time)
        ):
            frappe.throw(
                f"Doctor OPD starts at {doctor_start_time}. Please select a valid appointment time."
            )

        if (
            doctor_end_time
            and get_time(self.appointment_time) > get_time(doctor_end_time)
        ):
            frappe.throw(
                f"Doctor OPD ends at {doctor_end_time}. Please select a valid appointment time."
            )