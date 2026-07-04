frappe.ui.form.on("Doctor", {
    refresh(frm) {

    },

    phone_number(frm) {

        if (!frm.doc.phone_number) return;

        frm.doc.phone_number = frm.doc.phone_number.replace(/\D/g, "");

        if (frm.doc.phone_number.length > 10) {
            frm.doc.phone_number = frm.doc.phone_number.slice(0, 10);
        }

        frm.refresh_field("phone_number");
    },

    consultation_fee(frm) {

        if (frm.doc.consultation_fee < 0) {
            frappe.msgprint("Consultation Fee cannot be negative.");
            frm.set_value("consultation_fee", 0);
        }
    },

    experience(frm) {

        if (frm.doc.experience < 0) {
            frappe.msgprint("Experience cannot be negative.");
            frm.set_value("experience", 0);
        }
    },

    email(frm) {

        if (!frm.doc.email) return;

        let email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!email_regex.test(frm.doc.email)) {
            frappe.msgprint("Invalid Email Address");
        }
    }
});