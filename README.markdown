# Celiopatra - Hospital Management System

**Celiopatra** is a comprehensive Odoo module designed for managing hospital operations efficiently. Built for Odoo 17.0, this module provides tools to handle patients, doctors, departments, appointments, rooms, medicines, and reporting, streamlining healthcare workflows.

## Features

- **Patient Management**: Store and manage patient details, including name, age, gender, national ID, blood type, and insurance policy number.
- **Doctor Management**: Track doctor profiles, specializations, availability, and associated departments.
- **Department Management**: Organize hospital departments with responsible doctors and track the number of doctors per department.
- **Appointment Management**: Schedule and manage appointments with states (Draft, Scheduled, In Progress, Done, Cancelled), calculate total fees (appointment, X-ray, chair), and track medicines prescribed.
- **Room Management**: Monitor hospital room status (Available, Full, Maintenance) and bed occupancy.
- **Medicine Management**: Manage medicine inventory with details like name, expiration date, price, and active status.
- **Medicine Lines**: Link medicines to appointments with quantity and dosage information.
- **User Extension**: Extend Odoo user profiles with gender and doctor associations.
- **Reporting**: Generate detailed reports for appointments and patients with customizable layouts.
- **Wizards**: Facilitate quick actions like changing doctors or viewing appointment-related details.
- **Security**: Role-based access control with groups (Super, Manager, General, Doctor) and rules to restrict data access.
- **Automated Code Generation**: Unique codes for patients (PAT), doctors (DOC), departments (DEP), appointments (APP), and medicines (MED) using Odoo sequences.
- **Chatter Integration**: Track changes and communications via Odoo's mail.thread and mail.activity.mixin.

## Dependencies

The module depends on the following Odoo core modules:

- `base`
- `mail`
- `web`

Ensure these modules are installed in your Odoo instance before installing Celiopatra.

## Installation

1. **Download the Module**:

   - Clone or download the `celiopatra` module to your Odoo addons directory.

2. **Update the Addons Path**:

   - Add the module's directory to your Odoo configuration file under `addons_path`.

3. **Install the Module**:

   - Start your Odoo server.
   - Go to the Odoo Apps menu, click "Update Apps List," and search for `celiopatra`.
   - Click "Install" to deploy the module.

4. **Verify Installation**:
   - Ensure all models (Patient, Doctor, Department, Appointment, Room, Medicine, Medicine Line) and views are loaded correctly.
   - Check that the menu items under "Celiopatra System" are visible.

## Configuration

- **Set Up Security Groups**:
  - Assign users to appropriate groups (Super Group, Manager Group, General Group, Doctor Group) via the Odoo Users settings.
  - Super Group: Full access (read, write, create, delete) to all models.
  - Manager Group: Read, write, and create access (no delete) to all models.
  - General Group: Read and create access (no write or delete) to all models.
  - Doctor Group: Used to restrict certain actions for doctor-specific users.

## Usage

1. **Managing Patients**:

   - Navigate to `Celiopatra System > Patients` to create or edit patient records.
   - Fields include name, date of birth (auto-calculates age), gender, national ID, blood type, and insurance details.
   - Default profile images are set based on gender (male: `patient_male_character.png`, female: `patient_female_character.jpeg`).

2. **Managing Doctors**:

   - Access `Celiopatra System > Doctors` to add doctor profiles.
   - Specify specialization, license number, availability, and department.
   - Availability is automatically computed based on `available_from` and `available_to` fields.

3. **Managing Departments**:

   - Go to `Celiopatra System > Departments` to create departments.
   - Assign a responsible doctor and track the number of doctors in each department.
   - Department images are inherited from the responsible doctor's profile or set to default based on gender.

4. **Scheduling Appointments**:

   - Use `Celiopatra System > Appointments` to schedule appointments.
   - Select patient, doctor, department, and set appointment fees, X-ray fees, and chair fees (total price is auto-calculated).
   - Track appointment states and add medicine lines for prescriptions.

5. **Room Management**:

   - Manage rooms under `Celiopatra System > Rooms`.
   - Update bed counts and occupancy, with automatic state updates (Available, Full, Maintenance).

6. **Medicine Management**:

   - Add medicines via `Celiopatra System > Medicines`.
   - Track medicine details and link them to appointments via medicine lines.

7. **Using Wizards**:

   - **Appointment Wizard**: Change the doctor assigned to an appointment (`hospitalme.appointment.wizard`).
   - **Appointment Wizard Details**: View doctor or patient details and print appointment reports (`hospitalme.appointment.wizard.details`).

8. **Generating Reports**:
   - Access reports from the respective models:
     - **Appointment Report**: Details appointment information and prescribed medicines.
     - **Patient Report**: Displays patient personal and medical information.

## Security and Access Control

- **Groups**:
  - **Super Group**: Full access to all models.
  - **Manager Group**: Read, write, and create access (no deletion).
  - **General Group**: Read and create access only.
  - **Doctor Group**: Restricts certain actions for doctor users (e.g., visibility of fields based on group membership).
- **Rules**:
  - **Patient Records**: Restricted to the creator (`create_uid`) for Manager and General groups.
  - **Departments**: Accessible only to users linked to the responsible doctor.
  - A commented gender-based rule for patients is available but not active.
- **Access Rights**:
  - Defined in `ir.model.access.csv` for each model, ensuring role-based permissions.

## Reports

- **Appointment Report**:
  - Displays appointment details (name, date, doctor, patient, state, total price) and medicine lines.
  - Styled with `appointment_report.css`.
- **Patient Report**:
  - Shows patient personal (name, gender, country, state, age, national ID) and medical (blood type, insurance, doctor) information.
  - Uses a custom A4 paper format (`paperformat_patientclient_report`) and styled with `patient_report.css`.

## Wizards

- **Appointment Wizard (`hospitalme.appointment.wizard`)**:
  - Allows changing the doctor for an existing appointment.
  - Displays the current department and doctor, with a notification upon successful change.
- **Appointment Wizard Details (`hospitalme.appointment.wizard.details`)**:
  - Provides quick access to doctor and patient details.
  - Includes an option to print the appointment report.

---

## 👤 Author

**Abdelrahman Naser Muhammed**
Front-End & Python Odoo Developer | Cairo, Egypt
📍 [LinkedIn](https://www.linkedin.com/in/abdelrahman-naser-muhammed)
📂 [GitHub](https://github.com/abdonaser)
📧 Email: [abdonaser4223@gmail.com](mailto:abdonaser4223@gmail.com)
