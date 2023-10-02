$(document).ready(function () {
    const styleCheckbox = document.getElementById('styleCheckbox');
    const styleInputContainer = document.getElementById('styleInputContainer');

    styleCheckbox.addEventListener('change', function () {
        if (styleCheckbox.checked) {
            styleInputContainer.style.display = 'block';
        } else {
            styleInputContainer.style.display = 'none';
        }
    });
    // Handle form submission with AJAX
    const eList = [
        'uploaded-content',
        'transformed-image-1',
        'transformed-image-2',
        'image-caption-1',
        'image-caption-2',
        'image-caption'
      ];
    $('#upload-form').submit(function (event) {
        event.preventDefault();  // Prevent default form submission
        // document.getElementById('uploaded-content').style.display = 'none';
        // document.getElementById('transformed-image-1').style.display = 'none';
        // document.getElementById('transformed-image-2').style.display = 'none';
        // document.getElementById('image-caption-1').style.display = 'none';
        // document.getElementById('image-caption-2').style.display = 'none';
        // document.getElementById('image-caption').style.display = 'none';
        eList.forEach(e => {
            document.getElementById(e).style.display = 'none';
        });
        document.querySelector('.loader').style.display = "block";
        var formData = new FormData(this);
        if(formData.get('content_image').size === 0){
            $("#error").text("Please upload an image");
            $("#error").css({
                "width": "100%",
                "text-align": "center",
                "color": "red"
            });
            document.querySelector('.loader').style.display = "none";
        }else{
            $("#error").text("");
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {


                var reader1 = new FileReader();
                reader1.onload = function (event) {
                    $('#uploaded-content').attr('src', event.target.result);
                };
                reader1.readAsDataURL(formData.get('content_image'));
                $('#image-caption').text("Content Image");

                // create promises for each image
                var promise = new Promise(function (resolve, reject) {
                    $('#uploaded-content').on('load', function () {
                        resolve();
                    });
                });
                var promise1 = new Promise(function (resolve, reject) {
                    $('#transformed-image-1').on('load', function () {
                        resolve();
                    });
                });

                var promise2 = new Promise(function (resolve, reject) {
                    $('#transformed-image-2').on('load', function () {
                        resolve();
                    });
                });


                Promise.all([promise, promise1, promise2]).then(function () {
                    var images = document.getElementsByClassName('samesize');
                    var minWidth = 800;
                    var aspectR = 1;

                    for (var i = 0; i < images.length; i++) {
                        var width = images[i].naturalWidth;
                        var height = images[i].naturalHeight;
                        aspectR = width / height;
                        if (width < minWidth) {
                            minWidth = width;
                        }
                    }
                    var uniHeight = Math.floor(minWidth / aspectR);
                    for (var i = 0; i < images.length; i++) {
                        images[i].style.width = minWidth + 'px';
                        images[i].style.height = uniHeight + 'px';
                    }

                });

                $('#transformed-image-1').attr('src', 'data:image/png;base64,' + data.image_gan);
                $('#image-caption-1').text("Generation Time for Gated GAN: " + data.text_gan + "s");
                $('#transformed-image-2').attr('src', 'data:image/png;base64,' + data.image_mix);
                $('#image-caption-2').text("Generation Time for Style Mixer: " + data.text_mix + "s");

                // document.getElementById('uploaded-content').style.display = 'block';
                // document.getElementById('transformed-image-1').style.display = 'block';
                // document.getElementById('transformed-image-2').style.display = 'block';
                // document.getElementById('image-caption-1').style.display = 'block';
                // document.getElementById('image-caption-2').style.display = 'block';
                // document.getElementById('image-caption').style.display = 'block';
                eList.forEach(e => {
                    document.getElementById(e).style.display = 'block';
                });
                document.querySelector('.loader').style.display = "none";

            }
        });
    }
    });
});
