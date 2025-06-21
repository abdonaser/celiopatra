{
    'name': "celiopatra",
    'summary': "Hospital Management System",
    'description': "A comprehensive hospital management system",
    'author': "Abdelrahman Naser",
    'maintainer': "Abdelrahman Naser",
    'category': "Healthcare",
    'version': "17.0.1.0.0",
    'license': "LGPL-3",
    'depends': [
        'base',
        'mail',
        'web',
    ],
    'data': [
        # security
        'security/groups.xml',
        'security/rules.xml',
        'security/ir.model.access.csv',
        # data
        'data/sequences.xml',
        # wizzard
        'wizzard/wizard_views/appointment_wizard_view.xml',
        'wizzard/wizard_views/appointment_wizard_details.xml',
        # views
        'views/menus.xml',
        'views/patients_view.xml',
        'views/doctor.xml',
        'views/department.xml',
        'views/appointment.xml',
        'views/room.xml',
        'views/medicine.xml',
        'views/medicine_line_ids_view.xml',
        'views/res_users_view.xml',
        # reports
        'reports/appointment_report.xml',
        'reports/patient_report.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'celiopatra_system/static/src/css/style.css',
            'celiopatra_system/static/src/css/appointment_report.css',



        ],
        'web.report_assets_common': [
            'celiopatra_system/static/src/css/patient_report.css',
            'celiopatra_system/static/src/img/hospital.png',

    ],
    }
}
