$(document).ready(function () {
   $("#send").click(function () {
        var message = $("#send_content").val()

        $.ajax({
            // Specify the endpoint URL the request should be sent to.
            url: '/respond',
            // The request type
            type: 'POST',
            // The data, which is now most commonly formatted using JSON because of its
            // simplicity and is native to JavaScript.
            data: JSON.stringify({response:message}),
            // Specify the format of the data which will be sent.
            contentType: "application/json; charset=utf-8",
            // The data type itself.
            dataType: "json",
            // Define the function which will be triggered if the request is received and
            // a response successfully returned.
            success: function (response) {
                console.log(response);
                document.getElementById('p').innerHTML=response.response
            },
            // The function which will be triggered if any error occurs.
            error: function (error) {
                console.log(error);
            }
        })
    })
})
