{
    "name": "MyCompany Custom",
    "version": "17.0.1.0.0",
    "summary": "Custom module for MyCompany",
    "category": "Custom",
    "author": "MyCompany",
    "depends": ["base", "sale","web"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property.xml",
        "views/owner.xml",
        "views/enquiry.xml",
        # "security/groups.xml",
        "wizard/property_enquiry.xml",
        "report/qweb_report.xml",
        "report/qweb_inherit.xml",
        "report/qweb_custom_pdf.xml"
    ],
    "installable": True,
    "application": True,
    "license":'LGPL-3',
}



