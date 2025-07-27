const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

// Panel toggle
sign_up_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
});

// Send OTP
document.getElementById("send-otp").addEventListener("click", function () {
    const email = document.getElementById("signup-email").value;
    const otpGroup = document.getElementById("otp-group");
    const statusDiv = document.getElementById("otp-status");

    if (!email) {
        alert("Please enter your email before requesting OTP.");
        return;
    }

    // Only allow anurag.edu.in emails
    if (!email.endsWith("@anurag.edu.in")) {
        alert("Only college emails (@anurag.edu.in) are allowed.");
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
            otpGroup.style.display = "flex"; // show OTP input and verify button
            statusDiv.textContent = ""; // clear any previous status
        })
        .catch((err) => {
            alert("Failed to send OTP.");
        });
});

// Verify OTP
document.getElementById("verify-otp").addEventListener("click", function () {
    const email = document.getElementById("signup-email").value;
    const otp = document.getElementById("otp-input").value;
    const statusDiv = document.getElementById("otp-status");
    const signupBtn = document.getElementById("signup-submit");

    if (!otp) {
        alert("Please enter the OTP.");
        return;
    }

    fetch("/verify_otp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: email, otp: otp }),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.verified) {
                statusDiv.style.color = "green";
                statusDiv.textContent = "✅ " + data.message;
                signupBtn.disabled = false; // enable sign-up
            } else {
                statusDiv.style.color = "red";
                statusDiv.textContent = "❌ " + data.message;
                signupBtn.disabled = true; // keep disabled
            }
        })
        .catch((err) => {
            alert("OTP verification failed.");
        });
});
