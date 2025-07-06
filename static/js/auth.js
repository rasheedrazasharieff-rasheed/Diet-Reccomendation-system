document.addEventListener("DOMContentLoaded", () => {
  // Form validation for signup
  const signupForm = document.getElementById("signupForm")
  if (signupForm) {
    signupForm.addEventListener("submit", (e) => {
      const password = document.getElementById("password").value
      const confirmPassword = document.getElementById("confirm_password").value

      if (password !== confirmPassword) {
        e.preventDefault()
        alert("Passwords do not match!")
        return false
      }

      if (password.length < 6) {
        e.preventDefault()
        alert("Password must be at least 6 characters long!")
        return false
      }

      return true
    })
  }

  // Form validation for login
  const loginForm = document.getElementById("loginForm")
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      const email = document.getElementById("email").value
      const password = document.getElementById("password").value

      if (!email || !password) {
        e.preventDefault()
        alert("Please fill in all fields!")
        return false
      }

      return true
    })
  }
})

