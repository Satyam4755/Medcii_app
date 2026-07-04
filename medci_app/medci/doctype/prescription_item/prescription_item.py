# Copyright (c) 2026, Satyam and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PrescriptionItem(Document):

    def validate(self):
        self.validate_medicine()
        self.validate_days()
        self.calculate_total_tablets()

    # -----------------------------------
    # Validation Functions
    # -----------------------------------

    def validate_medicine(self):

        if not self.medicine:
            frappe.throw("Medicine Name is required.")

        self.medicine = self.medicine.strip().title()

    def validate_days(self):

        if self.days is None:
            return

        if self.days <= 0:
            frappe.throw("Days must be greater than 0.")

    def calculate_total_tablets(self):

        if not self.days:
            self.total_tablets = 0
            return

        frequency_map = {
            "Morning": 1,
            "Afternoon": 1,
            "Evening": 1,
            "Night": 1,
            "Twice Daily": 2,
            "Thrice Daily": 3,
        }

        tablets_per_day = frequency_map.get(self.frequency, 1)

        self.total_tablets = tablets_per_day * self.days