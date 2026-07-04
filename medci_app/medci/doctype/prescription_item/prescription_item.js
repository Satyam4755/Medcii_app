frappe.ui.form.on("Prescription Item", {

    medicine(frm, cdt, cdn) {

        let row = locals[cdt][cdn];

        if (!row.medicine) return;

        frappe.model.set_value(
            cdt,
            cdn,
            "medicine",
            row.medicine.trim()
        );
    },

    days(frm, cdt, cdn) {

        let row = locals[cdt][cdn];

        if (!row.days) return;

        if (row.days <= 0) {

            frappe.msgprint("Days must be greater than 0.");

            frappe.model.set_value(
                cdt,
                cdn,
                "days",
                1
            );
        }

        calculate_total(cdt, cdn);
    },

    frequency(frm, cdt, cdn) {

        calculate_total(cdt, cdn);
    }

});


function calculate_total(cdt, cdn) {

    let row = locals[cdt][cdn];

    if (!row.days) return;

    let tablets = 1;

    switch (row.frequency) {

        case "Morning":
        case "Afternoon":
        case "Evening":
        case "Night":
            tablets = 1;
            break;

        case "Twice Daily":
            tablets = 2;
            break;

        case "Thrice Daily":
            tablets = 3;
            break;
    }

    frappe.model.set_value(
        cdt,
        cdn,
        "total_tablets",
        tablets * row.days
    );
}