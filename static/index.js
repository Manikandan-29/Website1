$(document).ready(function () {
    // Handle form submission for adding a new student
    $('#student-form').off('submit').on('submit', function (event) {
        event.preventDefault();;
        const studentData = {
            name: $('#name').val(),
            roll_number: $('#roll_number').val(),
            department: $('#department').val(),
            class_: $('#class_').val(),
            date_of_birth: $('#date_of_birth').val(),
            gender: $('#gender').val(),
            address: $('#address').val(),
            phone_number: $('#phone_number').val(),
            mail_id: $('#mail_id').val(),
            marksheet: $('#marksheet').val(),
            certificate: $('#certificate').val()
        };
        $.ajax({
            type: 'POST',
            url: '/students',
            contentType: 'application/json',
            data: JSON.stringify(studentData),
            success: function (response) {
                alert(response.message);
                $('#student-form-container')[0].reset(); // Reset the form after successful submission
            },
            error: function () {
                alert('An error occurred while adding the student.');
            }
        });
    });

    let isStudentDatabaseVisible = false;
    // Handle student database toggle
    $('#show-database').on('click', function () {
        $.get('/students', function (data) {
            const studentList = $('#student-list');
            studentList.empty(); // Clear any existing list items
            if (data.length > 0) {
                data.forEach(student => {
                    studentList.append(`
                    <tr>
                        <td>${student.name || ''}</td>
                        <td>${student.roll_number || ''}</td>
                        <td>${student.department || ''}</td>
                        <td>${student.class_ || ''}</td>
                        <td>${student.date_of_birth || ''}</td>
                        <td>${student.gender || ''}</td>
                        <td>${student.address || ''}</td>
                        <td>${student.phone_number || ''}</td>
                        <td>${student.mail_id || ''}</td>
                        <td>${student.marksheet || ''}</td>
                        <td>${student.certificate || ''}</td>
                        <td>
                            <button class="edit-student" data-roll-number="${student.roll_number}" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-right: 5px;">Edit</button>
                            <button class="delete-student" data-roll-number="${student.roll_number}" style="background-color: #f44336; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Delete</button>
                        </td>
                    </tr>
                `);
                });
            } else {
                studentList.append('<tr><td colspan="11">No students found.</td></tr>');
            }
            // Toggle visibility
            if (isStudentDatabaseVisible) {
                $('#student-database').hide(); // Hide if it was visible
            } else {
                $('#student-database').show(); // Show if it was hidden
            }

            // Update the visibility state
            isStudentDatabaseVisible = !isStudentDatabaseVisible;

        }).fail(function () {
            alert('An error occurred while fetching the student data.');
        });
    });

    // Handle edit student button click
    $('#student-list').on('click', '.edit-student', function () {
        const rollNumber = $(this).data('roll-number');
        $.get(`/students/${rollNumber}`, function (data) {
            $('#edit_name').val(data.name || '');
            $('#edit_roll_number').val(data.roll_number || '');
            $('#edit_department').val(data.department || '');
            $('#edit_class_').val(data.class_ || '');
            $('#edit_date_of_birth').val(data.date_of_birth || '');
            $('#edit_student_gender').val(gender || '');
            $('#edit_address').val(data.address || '');
            $('#edit_student_phone_number').val(data.phone_number || '');
            $('#edit_mail_id').val(data.mail_id || '');
            $('#edit_marksheet').val(data.marksheet || '');
            $('#edit_certificate').val(data.certificate || '');
            $('#edit-form').show(); // Show the edit form
        }).fail(function () {
            alert('An error occurred while fetching student data.');
        });
    });

    // Handle save button click for updating student data
    $('#update-student').on('click', function () {
        const studentData = {
            name: $('#edit_name').val(),
            roll_number: $('#edit_roll_number').val(),
            department: $('#edit_department').val(),
            class_: $('#edit_class_').val(),
            date_of_birth: $('#edit_date_of_birth').val(),
            gender: $('#edit_student_gender').val(),
            address: $('#edit_address').val(),
            phone_number: $('#edit_student_phone_number').val(),
            mail_id: $('#edit_mail_id').val(),
            marksheet: $('#edit_marksheet').val(),
            certificate: $('#edit_certificate').val()
        };
        $.ajax({
            type: 'PUT',
            url: `/students/${studentData.roll_number}`,
            contentType: 'application/json',
            data: JSON.stringify(studentData),
            success: function (response) {
                alert(response.message);

                $('#edit-form').hide(); // Hide the edit form after successful update
                $('#show-database').click(); // Refresh the student list
            },
            error: function () {
                alert('An error occurred while updating the student.');
            }
        });
    });

    // Handle cancel button click for student edit form
    $('#cancel-edit').on('click', function () {
        $('#edit-form').hide(); // Hide the edit form without saving
    });

    // Handle delete student button click
    $('#student-list').off('click', '.delete-student').on('click', '.delete-student', function () {
        const rollNumber = $(this).data('roll-number');
        $.ajax({
            type: 'DELETE',
            url: `/students/${rollNumber}`,
            success: function (response) {
                alert(response.message);
                $('#show-database').click(); // Refresh the student list
            },
            error: function () {
                alert('An error occurred while deleting the student.');
            }
        });
    });
});


// Existing code for students...

// Handle staff form submission
$('#staff-form').submit(function (event) {
    event.preventDefault();

    const staffData = {
        name: $('#staff_name').val(),
        age: $('#age').val(),
        gender: $('#staff_gender').val(),
        date_of_joining: $('#date_of_joining').val(),
        date_of_birth: $('#date_of_birth_staff').val(),
        address: $('#staff_address').val(),
        phone_number: $('#staff_phone_number').val(),
        designation: $('#designation').val(),
        department: $('#staff_department').val()
    };

    $.ajax({
        url: '/staff',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(staffData),
        success: function (response) {
            alert('Staff added successfully');
            $('#staff-form')[0].reset();
        },
        error: function (error) {
            alert('Error adding staff: ' + error.responseText);
        }
    });
});

// Show staff database
$('#show-staff-database').on('click', function () {
    $.get('/staff', function (data) {
        const staffList = $('#staff-list');
        staffList.empty();
        if (data.length > 0) {
            data.forEach(staff => {
                staffList.append(`
    <tr>
      <td>${staff.name || ''}</td>
      <td>${staff.age || ''}</td>
      <td>${staff.gender || ''}</td>
      <td>${staff.date_of_joining || ''}</td>
      <td>${staff.date_of_birth || ''}</td>
      <td>${staff.address || ''}</td>
      <td>${staff.phone_number || ''}</td>
      <td>${staff.designation || ''}</td>
      <td>${staff.department || ''}</td>
      <td>
     <button class="edit-staff" data-id="${staff.id}" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-right: 5px;">
      Edit
     </button>
     <button class="delete-staff" data-id="${staff.id}" style="background-color: #f44336; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
      Delete
     </button>
      </td>
    </tr>
  `);
            });
        } else {
            staffList.append('<tr><td colspan="9">No staff members found.</td></tr>');
        }
        $('#staff-database').toggle();
    }).fail(function () {
        alert('Error fetching staff data.');
    });
});

// Handle edit staff button click
$('#staff-list').on('click', '.edit-staff', function () {
    const staffId = $(this).data('id');
    $.get(`/staff/${staffId}`, function (data) {
        $('#edit_staff_id').val(data.id || '');
        $('#edit_staff_name').val(data.name || '');
        $('#edit_staff_age').val(data.age || '');
        $('#edit_staff_gender').val(data.gender || '');
        $('#edit_staff_date_of_joining').val(data.date_of_joining || '');
        $('#edit_staff_date_of_birth').val(data.date_of_birth || '');
        $('#edit_staff_address').val(data.address || '');
        $('#edit_staff_phone_number').val(data.phone_number || '');
        $('#edit_staff_designation').val(data.designation || '');
        $('#edit_staff_department').val(data.department || '');
        $('#edit-staff-form').show();
    }).fail(function () {
        alert('Error fetching staff data.');
    });
});

// Handle save button click for staff
$('#update-staff').on('click', function () {
    const staffId = $('#edit_staff_id').val();
    const staffData = {
        name: $('#edit_staff_name').val(),
        age: $('#edit_staff_age').val(),
        gender: $('#edit_staff_gender').val(),
        date_of_joining: $('#edit_staff_date_of_joining').val(),
        date_of_birth: $('#edit_staff_date_of_birth').val(),
        address: $('#edit_staff_address').val(),
        phone_number: $('#edit_staff_phone_number').val(),
        designation: $('#edit_staff_designation').val(),
        department: $('#edit_staff_department').val()
    };
    $.ajax({
        type: 'PUT',
        url: `/staff/${staffId}`,
        contentType: 'application/json',
        data: JSON.stringify(staffData),
        success: function (response) {
            alert(response.message);
            $('#edit-staff-form').hide();
            $('#show-staff-database').click();
        },
        error: function () {
            alert('An error occurred while updating the staff member.');
        }
    });
});

// Handle cancel button click for staff
$('#cancel-staff-edit').on('click', function () {
    $('#edit-staff-form').hide();
});

// Handle delete staff button click
$('#staff-list').on('click', '.delete-staff', function () {
    const staffId = $(this).data('id');
    $.ajax({
        type: 'DELETE',
        url: `/staff/${staffId}`,
        success: function (response) {
            alert(response.message);
            $('#show-staff-database').click();
        },
        error: function () {
            alert('An error occurred while deleting the staff member.');
        }
    });
});

/* Set the width of the sidebar to 250px (show it) */
function openNav() {
    document.getElementById("mySidepanel").style.width = "250px";
}

/* Set the width of the sidebar to 0 (hide it) */
function closeNav() {
    document.getElementById("mySidepanel").style.width = "0";
}
