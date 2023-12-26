const usernameField = document.querySelector("#usernameField");
const usernameFeedbackField = document.querySelector(
  ".invalid-username-feedback"
);
const usernameSuccess = document.querySelector(".usernameSuccess");

const emailField = document.querySelector("#emailField");
const emailFeedbackField = document.querySelector(".invalid-email-feedback");
const emailSuccess = document.querySelector(".emailSuccess");

const passwordField = document.querySelector("#passwordField");
const confirmPasswordField = document.querySelector("#confirmPasswordField");

usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;
  usernameSuccess.style.display = "block";

  usernameSuccess.textContent = `Checking ${usernameVal}`;
  usernameField.classList.remove("is-invalid");
  usernameFeedbackField.style.display = "none";

  if (usernameVal.length > 0) {
    fetch("/authentication/validate-username", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        usernameSuccess.style.display = "none";
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          usernameFeedbackField.style.display = "block";
          usernameFeedbackField.innerHTML = `<p>${data.username_error}</p>`;
        }
      });
  }
});

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;
  emailSuccess.style.display = "block";
  emailSuccess.textContent = `Checking ${emailVal}`;

  emailField.classList.remove("is-invalid");
  emailFeedbackField.style.display = "none";

  if (emailVal.length > 0) {
    fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        emailSuccess.style.display = "none";
        if (data.email_error) {
          emailField.classList.add("is-invalid");
          emailFeedbackField.style.display = "block";
          emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
        }
      });
  }
});
