$(document).ready(function () {
    const resizeCheckbox = document.getElementById('resizeCheckbox');
    const resizeInputContainer = document.getElementById('resizeInputContainer');

    resizeCheckbox.addEventListener('change', function () {
        if (resizeCheckbox.checked) {
            resizeInputContainer.style.display = 'block';
        } else {
            resizeInputContainer.style.display = 'none';
        }
    });

    var slider1 = document.getElementById("style1");
    var sliderValue1 = document.getElementById("sliderValue1");

    slider1.oninput = function () {
        sliderValue1.textContent = Math.round(this.value * 100) + "%";
    }
    var slider2 = document.getElementById("style2");
    var sliderValue2 = document.getElementById("sliderValue2");

    slider2.oninput = function () {
        sliderValue2.textContent = Math.round(this.value * 100) + "%";
    }
    var slider3 = document.getElementById("style3");
    var sliderValue3 = document.getElementById("sliderValue3");

    slider3.oninput = function () {
        sliderValue3.textContent = Math.round(this.value * 100) + "%";
    }
    // Handle form submission with AJAX
    $('#upload-form').submit(function (event) {
        event.preventDefault();  // Prevent default form submission

        $('#transformed-image').css('display', 'none');
        $('#image-caption').css('display', 'none');
        $('#uploaded-image').css('display', 'none');
        document.querySelector('.loader').style.display = "block";
        var formData = new FormData(this);
        if (formData.get('image').size !== 0) {
            $("#error").text("");
            $.ajax({
                url: $(this).attr('action'),
                type: $(this).attr('method'),
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    $('#uploaded-image').attr('src', 'data:image/png;base64,' + data.orig);
                    $('#uploaded-image').css('display', 'block');
                    $('#transformed-image').attr('src', 'data:image/png;base64,' + data.image);
                    $('#transformed-image').css('display', 'block');
                    $('#image-caption').text("Generation Time: " + data.text + "s");
                    $('#image-caption').css('display', 'block');
                    document.querySelector('.loader').style.display = "none";
                }
            });
        } else{
            $("#error").text("Please upload an image");
            $("#error").css({
                "width": "100%",
                "text-align": "center",
                "color": "red"
            });
            document.querySelector('.loader').style.display = "none";
        }
    });
});
