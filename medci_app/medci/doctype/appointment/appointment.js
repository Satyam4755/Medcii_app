frappe.ui.form.on("Appointment", {

    refresh(frm) {

    },

    appointment_date(frm) {

        if (!frm.doc.appointment_date) return;

        let today = frappe.datetime.get_today();

        if (frm.doc.appointment_date < today) {

            frappe.msgprint("Appointment Date cannot be in the past.");

            frm.set_value("appointment_date", "");
        }
    },

    patient(frm) {

        if (!frm.doc.patient) {

            frappe.msgprint("Please select a Patient.");
        }
    },

    doctor(frm) {

        if (!frm.doc.doctor) {

            frappe.msgprint("Please select a Doctor.");
        }
    },

    payment_status(frm) {

        if (frm.doc.payment_status === "Done") {

            if (!frm.doc.payment_method) {

                frappe.msgprint("Please select Payment Method.");
            }
        }
    },

    consultation_fee(frm) {

        frm.set_value(
            "total_amount",
            frm.doc.consultation_fee || 0
        );
    },

    status(frm) {

        if (
            frm.doc.status === "Completed" &&
            frm.doc.payment_status !== "Done"
        ) {

            frappe.msgprint(
                "Complete the payment before marking appointment as Completed."
            );

            frm.set_value("status", "Scheduled");
        }
    }

});