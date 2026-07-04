# Copyright (c) 2026, Satyam and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Appointment(Document):
	def validate(self):
		if self.status == "Completed" and self.payment_status != "Done":
			frappe.throw(
    "Payment must be completed before completing the appointment."
    )
