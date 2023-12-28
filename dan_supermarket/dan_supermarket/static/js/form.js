const usernameField = document.querySelector("#usernameField");
const usernameFeedbackField = document.querySelector(
  ".invalid-username-feedback"
);

const emailField = document.querySelector("#emailField");
const emailFeedbackField = document.querySelector(".invalid-email-feedback");

const passwordField = document.querySelector("#passwordField");

const passwordIcon = document.querySelector("#passwordToggle");

const submitBtn = document.querySelector(".submit-btn");

const messages = document.querySelector("#msg");


usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;
  
  usernameField.classList.remove("is-invalid");
  usernameFeedbackField.style.display = "none";

  if (usernameVal.length > 0) {
    fetch("/authentication/validate-username", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        data.username_error
          ? (usernameField.classList.add("is-invalid"),
            (usernameFeedbackField.style.display = "block"),
            (usernameFeedbackField.innerHTML = `<p>${data.username_error}</p>`),
            submitBtn.setAttribute("disabled", "disabled"))
          : submitBtn.removeAttribute("disabled");
      });
  } 
});

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  emailField.classList.remove("is-invalid");
  emailFeedbackField.style.display = "none";

  if (emailVal.length > 0) {
    fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        data.email_error
          ? (emailField.classList.add("is-invalid"),
            (emailFeedbackField.style.display = "block"),
            (emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`),
            submitBtn.setAttribute("disabled", "disabled"))
          : submitBtn.removeAttribute("disabled");
      });
  }
});

passwordIcon.addEventListener("click", function () {
  if (passwordField.type === "password") {
    passwordField.type = "text";
    passwordIcon.classList.add("bi-eye-slash");
    passwordIcon.classList.remove("bi-eye");
  } else {
    passwordField.type = "password";
    passwordIcon.classList.add("bi-eye");
    passwordIcon.classList.remove("bi-eye-slash");
  }
});

setTimeout(function () {
  messages.style.display = "none";
}, 5000);
