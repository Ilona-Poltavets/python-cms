$(document).ready(function () {
    var json = {};
    var arr = []
    var i = 0
    if ($('#add-field').length) {
        $('#add-field').click(function () {
            var container = $('#fields-container');
            $('#add-field-form').modal("show");
            $('#add-field-form .btn.btn-primary').click(function () {
                var fieldName = $('#field-name').val();
                var fieldType = $('#field-type').val();
                arr[i] = { fieldName: fieldName, fieldType: fieldType };
                i++
                container.append('<tr><td>' + i + '<td>' + fieldName + '</td><td>' + fieldType + '</td><td></td></tr>');
                $('#add-field-form').modal("hide");
            });
        });
        $('#create').click(function () {
            if($('#entity-name').val() == '') {
                alert('Please enter entity name')
                return
            }
            json = JSON.stringify(arr);
            var data= new FormData();
            data.append('entityName', $('#entity-name').val());
            data.append('fields', json);
            console.log(json);
            $.ajax({
                url: '/create-entity',
                type: 'POST',
                data: data,
                processData: false,
                contentType: false,
                success: function (response) {
                    console.log(response);
                    window.location.href = '/';
                },
                error: function (xhr, status, error) {
                    console.error(xhr.responseText);
                }
            });
        })
    }
});