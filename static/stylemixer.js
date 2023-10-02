$(document).ready(function () {
    // Handle form submission with AJAX
    $('#upload-form').submit(function (event) {
        event.preventDefault();  // Prevent default form submission
        document.querySelector('.loader').style.display = "block";
        $('#uploaded-style').css('display', 'none');
        $('#uploaded-content').css('display', 'none');
        $('#transformed-image').css('display', 'none');
        $('#image-caption').css('display', 'none');

        var formData = new FormData(this);
        if (formData.get('style_image').size === 0 || formData.get('content_image').size === 0) {
            const missing = formData.get('style_image').size === 0 ? "style" : "content";
            $("#error").text(`Please upload ${missing} image`);
            $("#error").css({
                "width": "100%",
                "text-align": "center",
                "color": "red"
            });
            document.querySelector('.loader').style.display = "none";
        } else {
            $("#error").text("");
            $.ajax({
                url: $(this).attr('action'),
                type: $(this).attr('method'),
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    var reader = new FileReader();
                    reader.onload = function (event) {
                        $('#uploaded-style').attr('src', event.target.result);

                    };
                    reader.readAsDataURL(formData.get('style_image'));

                    var reader1 = new FileReader();
                    reader1.onload = function (event) {
                        $('#uploaded-content').attr('src', event.target.result);

                    };
                    reader1.readAsDataURL(formData.get('content_image'));
                    let img = new Image();
                    img.src = 'data:image/png;base64,' + data.image;

                    img.onload = function () {
                        // Image has loaded, you can now access its dimensions
                        let width = this.width;
                        let height = this.height;

                        // Do something with the width and height
                        console.log('Width:', width);
                        console.log('Height:', height);
                        // Set the dimensions to the transformed image
                        $('#transformed-image').attr('src', 'data:image/png;base64,' + data.image);
                        $('#image-caption').text("Generation Time: " + data.text + "s");
                        $('#image-caption').css('display', 'block');
                        $('#transformed-image').css('width', width);
                        $('#transformed-image').css('height', height);

                        let images = $('.samesize');
                        images.each(function (index, image) {
                            $(image).css("height", height);
                            $(image).css("width", width);
                        });
                    };

                    $('#uploaded-style').css('display', 'block');
                    $('#uploaded-content').css('display', 'block');
                    $('#transformed-image').css('display', 'block');
                    document.querySelector('.loader').style.display = "none";
                }
            });
        }
    });
});
