function save(id) {
    var quiz = window.prompt("How much would you like to deposit?(Utmost 10000 but more than 0",0);
    if(quiz <=10000 && quiz>=0){
        $(document).ready(function () {
            $.ajax({
                url: '/save',
                type: 'POST',
                data: JSON.stringify({in:quiz,user:id}),
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                success:function () {
                    alert("Successfully save in "+quiz+".")
                },
                error:function () {
                    alert("Error occurs")
                }
            })
        })
    }else{
        alert("The value is invalid");
    }
}

function withdraw(id) {
    var quiz = prompt("How much would you like to withdraw?",0)
    if(quiz <=10000 && quiz>=0){
        $(document).ready(function () {
            $.ajax({
                url: '/withdraw',
                type: 'POST',
                data: JSON.stringify({out:quiz,user:id}),
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                success:function () {
                    alert("Successfully withdraw "+quiz+".")
                },
                error:function () {
                    alert("Error occurs")
                }
            })
        })
    }else{
        alert("The value is invalid");
    }
}

function loan(id) {
    alert("You are going to ask for a loan, the personal finance assistance will help you with the process")
}

function cal(money,score,id,loan) {
    var result = 0;
    if (score >=600){
        result = (money-loan) * 0.4;
        x = "Congratulations! You can ask for a loan of "+result+" for maximum!";
        document.getElementById("result").innerHTML=x;
        run = "<label for=\"send_content\" class='run'>How much would you like to loan：</label>\n" +
            "<input id=\"send_content\" type=\"text\" name=\"send_content\">\n" +
            "<a id=\"send\" class='button button-glow button-rounded button-highlight' type=\"button\" onclick='loan_in("+id+")'>Go</a>";
        document.getElementById("run").innerHTML=run
    }else {
        alert("Your are under credit, turn back some loan first")
    }

}

function loan_in(id){
    var loan = $("#send_content").val()
    $.ajax({
        url: '/loan_in',
        type: 'POST',
        data: JSON.stringify({in:loan,user:id}),
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        success:function () {
            alert("You can check your loan in your account")
        },error:function () {
            alert("Loan Failed")
        }
    })
}

function loan_back(id) {
    var back = $("#back_loan").val()
    $.ajax({
        url: '/loan_back',
        type: 'POST',
        data: JSON.stringify({back:back,user:id}),
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        success:function () {
            alert("Successfully repaid")
        },error:function () {
            alert("Repay failed")
        }
    })
}

function OnInput(event) {
    var input = event.target.value;
    setTimeout(()=>{
        $.ajax({
        url: '/filter',
        type: 'POST',
        data: JSON.stringify({email:input}),
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        success:function (response) {
            console.log(response)
            document.getElementById('result').innerHTML=response.response
        }
    })},1000)
}

function getValue(event){
    var text = event.target.text
    var spl = text.split(" ")
    $("#collector_email").val(spl[2])
}

function send(id) {
    var much = prompt("How much would you like to remit? ",0)
    var email = $("#collector_email").val()
        $.ajax({
            url: '/trans/exchange',
            type: 'POST',
            data: JSON.stringify({email:email,from: id,money:much}),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success:function (response) {
                console.log(response)
                alert("Your operation is successful")
            },
            error:function () {
                alert("Remittance fail")
            }
        })
}