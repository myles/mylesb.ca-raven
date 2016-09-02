$(document).ready(function() {
    var form = $('#js-contact-form'),
        error_alert = $('#js-contact-form-error'),
        sucess_alert = $('#js-contact-form-sucess');

    form.on('submit', function(e) {
        e.preventDefault();

        if (form.validate()) {
            $.ajax({
                type: 'POST',
                url: form.attr('action'),
                data: form.serialize(),
                success: function(data) {
                    if (data['sent'] === 'ok') {
                        form.hide();
                        sucess_alert.show();
                    } else {
                        form.hide();
                        error_alert.show();
                    }
                },
                error: function(data) {
                    form.hide();
                    error_alert.show();
                }
            });
        }
    });
});
