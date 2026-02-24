{
    "name": "MyCompany Custom",
    "version": "17.0.1.0.0",
    "summary": "Custom module for MyCompany",
    "category": "Custom",
    "author": "MyCompany",
    "license": "LGPL-3",
    "depends": ["base", "sale", "web", "mail", "report_xlsx", "point_of_sale",'project'],
    "data": [
        "security/security_access.xml",
        "security/ir.model.access.csv",
        "data/owner.csv",
        "data/estate.property.xml",
        "data/owner.xml",
        "data/delete_id.xml",
        "views/estate_property.xml",
        "views/owner.xml",
        "views/enquiry.xml",
        "views/email_temp.xml",
        "views/extended_model_owner.xml",
        # "views/extended_offer.xml",
        "views/custom.xml",
        "wizard/property_enquiry.xml",
        "wizard/email_wizard.xml",
        "report/qweb_report.xml",
        "report/qweb_custom_pdf.xml",
        "Email_template/email.xml",
        "report/report_action_xslx.xml"
    ],
    "demo": [
        "demo/demo_data_xml.xml"
    ],

     'assets': {
        'web.assets_backend': [
            '/mycompany_custom/static/src/js/button_pos.js',
            '/mycompany_custom/static/src/xml/pos_button.xml',
            '/mycompany_custom/static/src/js/dashboard.js',
            '/mycompany_custom/static/src/xml/dashboard.xml',
            '/mycompany_custom/static/src/js/card.js',
            # '/mycompany_custom/static/src/js/systray_icon.js',
            # '/mycompany_custom/static/src/xml/systray_icon.xml',
            '/mycompany_custom/static/src/js/offer_state_selection.js',
            '/mycompany_custom/static/src/scss/offer_state_selection.scss',
            '/mycompany_custom/static/src/xml/offer_state_selection.xml',
             '/mycompany_custom/static/src/js/custom_trial.js',
             '/mycompany_custom/static/src/scss/custom_trial.scss',
             '/mycompany_custom/static/src/xml/custom_trial.xml',
        ],
    },


    "installable": True,
    "application": False,
}
