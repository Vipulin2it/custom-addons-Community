{
    "name": "MyCompany Custom",
    "version": "17.0.1.0.0",
    "summary": "Custom module for MyCompany",
    "category": "Custom",
    "author": "MyCompany",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property.xml",
        "views/owner.xml",
        "wizard/property_enquiry.xml",
    ],
    "installable": True,
    "application": True,
    "license":'LGPL-3',
}
