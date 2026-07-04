frappe.ui.form.on("Patient", {

    refresh(frm) {

    },

    phone_number(frm) {

        if (!frm.doc.phone_number) return;

        let cleaned = frm.doc.phone_number.replace(/\D/g, "").slice(0, 10);

        if (cleaned !== frm.doc.phone_number) {
            frm.set_value("phone_number", cleaned);
        }
    },

    email(frm) {

        if (!frm.doc.email) return;

        let regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!regex.test(frm.doc.email)) {
            frappe.msgprint("Invalid Email Address");
        }
    },

    date_of_birth(frm) {

        if (!frm.doc.date_of_birth) return;

        let today = frappe.datetime.get_today();

        if (frm.doc.date_of_birth > today) {
            frappe.msgprint("Date of Birth cannot be in the future.");
            frm.set_value("date_of_birth", "");
        }
    }

});