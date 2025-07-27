const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener('click', () =>{
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener('click', () =>{
    container.classList.remove("sign-up-mode");
});

document.getElementById("send-otp").addEventListener("click", function () {
    const email = document.getElementById("signup-email").value;

    if (!email) {
        alert("Please enter an email before sending OTP.");
        return;
    }

    fetch("/send_otp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: email }),
    })
        .then((res) => res.json())
        .then((data) => {
            alert(data.message);
        })
        .catch((err) => {
            alert("Failed to send OTP.");
        });
});
